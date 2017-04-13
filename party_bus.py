from mpd import MPDClient
from time import time

MPC = MPDClient()
MPC.timeout = 10
MPC.connect('localhost', 6600)

SONG_QUERY = []
RECENT_SONGS = []

def __init_query():
    init = MPC.listplaylistinfo('Awesome Music')[:5]
    for elem in init:
        song = MPC.find('title', elem['title'])[0]
        add_song(song, 'localhost')



def query_song(**query):
    mpd_compliant_query = []
    for key in query:
        mpd_compliant_query.append(key)
        mpd_compliant_query.append(query.get(key))
    print(mpd_compliant_query)
    return MPC.find(*mpd_compliant_query)

def sort_rankings():
    SONG_QUERY.sort(key=song_key)

def song_key(song):
    song_set = song[2]
    karma = 0
    for elem in song_set:
        if elem[1]:
            karma = karma + 1
        else:
            karma = karma - 1
    return (karma, -1 * song[1])

def add_song(song, ip):
    song_list = [x[0] for x in SONG_QUERY]
    if song in song_list:
        vote_song(song, ip, True)
    else:
        SONG_QUERY.append((song, time(), set()))
        vote_song(song, ip, True)

def vote_song(song, ip, vote):
    to_vote = None
    for elem in SONG_QUERY:
        if song == elem[0]:
            to_vote = elem
            break
    if (ip, True) in to_vote[2] or (ip, False) in to_vote[2]:
        return False
    to_vote[2].add((ip, vote))
    sort_rankings()
    return True

def mpd_add():
    sort_rankings()
    song = SONG_QUERY.pop()[0]
    MPC.add(song['file'])

__init_query()
vote_song(SONG_QUERY[3][0], 'spme', True)
mpd_add()
for elem in SONG_QUERY:
    print(elem)
