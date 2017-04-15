import json
from mpd import MPDClient
from time import time

MPC = MPDClient()
MPC.timeout = 10
MPC.connect('localhost', 6600)

class Client:
    '''
    MPDClient wrapper class to create a Client that is sensible for
    a collaborative playlist generation. Basically a PartyGenerator
    '''

    def __init__(self, host='localhost', port=6600):
        self.client = MPDClient()
        self.client.timeout = 10
        self.client.connect(host, port)
        self.queue = []
        self.recent = []
        self.__init_query()

    def __init_query(self):
        init = self.client.listplaylistinfo('Awesome Music')[:5]
        for elem in init:
            song = self.client.find('title', elem['title'])[0]
            self.add_song(song, 'SOMEDUDE')
        print('\n\n\n\n')



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
        print(mpd_compliant_query)
        return self.client.find(*mpd_compliant_query)

    def __sort_rankings(self):
        self.queue.sort(key=__song_key)

    def add_song(self, song, ip_addr):
        '''
        This method takes a song-filehandle and an IP (or any other string)
        as arguments. It will add the song (given the filehandle is valid)
        to the queue if it was not in the queue before and then directly
        upvote the song. Otherwise it will only upvote the song.'''
        song_list = [x[0] for x in self.queue]
        if song in song_list:
            self.vote_song(song, ip_addr, True)
        else:
            self.queue.append((song, time(), set()))
            self.vote_song(song, ip_addr, True)

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
        to_vote[2].add((ip_addr, vote))
        self.__sort_rankings()
        return True

    def __mpd_add(self):
        self.__sort_rankings()
        song = self.queue.pop()[0]
        MPC.add(song['file'])

def __song_key(song):
    song_set = song[2]
    karma = 0
    for elem in song_set:
        karma = karma + elem[1]
    return (karma, -1 * song[1])
