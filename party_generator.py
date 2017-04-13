from mpd import MPDClient
from time import time

MPC = MPDClient()
MPC.timeout = 10
MPC.connect('localhost', 6600)

class Client:

    def __init__(self, host='localhost', port=6600):
        self.client = MPDClient()
        self.client.timeout = 10
        self.client.connect(host, port)
        self.queue = []
        self.recent = []

    def init_query(self):
        init = self.client.listplaylistinfo('Awesome Music')[:5]
        for elem in init:
            song = self.client.find('title', elem['title'])[0]
            self.add_song(song, 'localhost')



    def query_song(self, **query):
        mpd_compliant_query = []
        for key in query:
            mpd_compliant_query.append(key)
            mpd_compliant_query.append(query.get(key))
        print(mpd_compliant_query)
        return self.client.find(*mpd_compliant_query)

    def sort_rankings(self):
        self.queue.sort(key=song_key)

    def add_song(self, song, ip):
        song_list = [x[0] for x in self.queue]
        if song in song_list:
            self.vote_song(song, ip, True)
        else:
            self.queue.append((song, time(), set()))
            self.vote_song(song, ip, True)

    def vote_song(self, song, ip, vote):
        to_vote = None
        for elem in self.queue:
            if song == elem[0]:
                to_vote = elem
                break
        if (ip, True) in to_vote[2] or (ip, False) in to_vote[2]:
            return False
        to_vote[2].add((ip, vote))
        self.sort_rankings()
        return True

    def mpd_add(self):
        self.sort_rankings()
        song = self.queue.pop()[0]
        MPC.add(song['file'])

def song_key(song):
    song_set = song[2]
    karma = 0
    for elem in song_set:
        if elem[1]:
            karma = karma + 1
        else:
            karma = karma - 1
    return (karma, -1 * song[1])
