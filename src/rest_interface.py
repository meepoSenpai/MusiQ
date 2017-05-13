from flask import request, Flask, render_template
from musi_q import Client, calculate_karma

app = Flask(__name__)

CLIENT = Client(host="localhost", default_playlist="Dank Musics")

# url_for('static', filename='style.css')

# def vote_song(song_id, ip_addr, weight):
#     return CLIENT.vote_song(song_id, ip_addr, int(weight))

def get_song_list():
    # Magic begins here
    return [elem for elem in CLIENT.queue][::-1]

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    if request.method == 'POST':
        title = request.form["title"]
        artist = request.form["artist"]
        album = request.form["album"]

        if title == "" and artist == "" and album == "":
            return "What am i supposed to do without anything"
        d = {"title": title, "artist": artist, "album": album}
        return CLIENT.query_song(**d)

    return render_template('index.html',
        ERROR=error,
        SONGS=get_song_list(),
        F_KARMA=calculate_karma)

@app.route('/getKarma', methods=['GET'])
def getKarma():
    song = request.args.get("song", "")
    print(song)
    return CLIENT.get_karma_of_song(song)

@app.route('/vote', methods=['POST'])
def vote():
    return str(CLIENT.vote_song(
            request.form['song_id'], 
            request.environ['REMOTE_ADDR'], 
            int(request.form['weight'])))

@app.route('/search', methods=['POST'])
def search():
    title = request.form["title"]
    artist = request.form["artist"]
    album = request.form["album"]
    if title == "" and artist == "" and album == "":
        return "What am i supposed to do without anything"
    d = {"title": title, "artist": artist, "album": album}
    print(CLIENT.query_song(**d))
    return 'Hello'

if __name__ == "__main__":
    app.run()
