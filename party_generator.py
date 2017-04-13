from mpd import MPDClient

MPC = MPDClient()
MPC.timeout = 10
MPC.connect('localhost', 6600)

def query_song(**query):
    mpd_compliant_query = []
    for key in query:
        mpd_compliant_query.append(key)
        mpd_compliant_query.append(query.get(key))
    print(mpd_compliant_query)
    return MPC.find(*mpd_compliant_query)

a = (query_song(**{'artist':"gorillaz", 'title':'melancholy'}))
for elem in a:
    print(elem)
