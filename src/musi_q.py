from mpd import MPDClient, ConnectionError
from time import time, sleep
from threading import Thread, Semaphore

class Client:
    '''
    MPDClient wrapper class to create a Client that is sensible for
    a collaborative playlist generation. Basically a PartyGenerator
    '''

    def __init__(self, host='localhost', port=6600, default_playlist=None):
        self.client = MPDClient()
        self.client.timeout = 10
        self.client.connect(host, port)
        self.queue = []
        self.recent = []
        self.recent_users = []
        self.lock = Semaphore()
        self.user_lock = Semaphore()
        if default_playlist:
            self.__init_queue(default_playlist)
        if self.client.status()['state'] != 'play' and self.queue != []:
            self.client.clear()
            self.__mpd_add()
            self.client.play(0)
        self.run = Thread(target=self.__check_loop)
        self.run.start()

    def __init_queue(self, playlist_name):
        try:
            init = self.client.listplaylistinfo(playlist_name)
            for elem in init:
                self.add_song(elem, 'admin')
        except ConnectionError:
            self.client.connect('localhost', port=6600)
            self.client.clear()
            init = self.client.listplaylistinfo(playlist_name)[:5]
            for elem in init:
                try:
                    song = self.client.find('title', elem['title'])[0]
                    self.add_song(song, 'admin')
                except IndexError:
                    continue
        self.__sort_rankings()



    def query_song(self, **query):
        '''
        This method takes a dictionary for a MPD-Search query.
        Valid keys are:
            any, artist, title, album
        '''
        mpd_compliant_query = []
        for key in query:
            mpd_compliant_query.append(key)
            mpd_compliant_query.append(query.get(key))
        try:
            query_result = self.client.find(*mpd_compliant_query)
        except ConnectionError:
            self.client.connect('localhost', port=6600)
            query_result = self.client.find(*mpd_compliant_query)
        return query_result


    def __sort_rankings(self):
        self.queue.sort(key=song_key)

    def __check_loop(self):
        while True:
            if self.client.status()['state'] != 'play' and len(self.queue) > 0:
                self.client.clear()
                self.__mpd_add()
                self.client.play(0)
            sleep(0.01)


    def add_song(self, song, ip_addr):
        '''
        This method takes a song-filehandle and an IP (or any other string)
        as arguments. It will add the song (given the filehandle is valid)
        to the queue if it was not in the queue before and then directly
        upvote the song. Otherwise it will only upvote the song.'''
        self.__pop_recent()
        user_list = [x for x in self.recent_users if ip_addr in x]
        if user_list != []:
            return 'You already added a Song in the last 15 Minutes'
        song_list = [x[0] for x in self.queue]
        if song in song_list:
            self.vote_song(song, ip_addr, True)
            return 'The song is already in the queue. It has been upvoted if you haven\'t voted for it yet'
        else:
            self.lock.acquire()
            self.queue.append((song, time(), set()))
            self.lock.release()
            self.vote_song(song, ip_addr, True)
            self.user_lock.acquire()
            self.recent_users.append((ip_addr, time()))
            self.user_lock.release()
            return 'Successfully added the song into the queue'

    def vote_song(self, song, ip_addr, vote):
        '''
        Takes a song-filehandle(str), IP(str) and a vote(bool) as arguments.
        Will vote for the song if the song is in the queue.
        '''
        to_vote = None
        for elem in self.queue:
            if song == elem[0].get('file'):
                to_vote = elem
                break
        if not to_vote:
            return False
        if (ip_addr, 1) in to_vote[2] or (ip_addr, -1) in to_vote[2]:
            return False
        self.lock.acquire()
        to_vote[2].add((ip_addr, vote))
        self.__sort_rankings()
        self.lock.release()
        return True

    def __mpd_add(self):
        self.__sort_rankings()
        self.lock.acquire()
        song = self.queue.pop()[0]
        self.recent.append((song, time()))
        self.queue = [x for x in self.queue if calculate_karma(x) > -5]
        self.lock.release()
        try:
            self.client.add(song['file'])
        except ConnectionError:
            self.client.connect('localhost', port=6600)
            self.client.add(song['file'])
        self.recent.append((song, time()))

    def __pop_recent(self):
        self.user_lock.acquire()
        self.recent = [x for x in self.recent if time() - x[1] > 600]
        self.recent_users = [x for x in self.recent_users if time() - x[1] > 900]
        self.user_lock.release()

def song_key(song):
    return (calculate_karma(song), -1 * song[1])

def calculate_karma(song):
    karma = 0
    for elem in song[2]:
        karma = karma + elem[1]
    return karma
