from flask import request, Flask, render_template
from musi_q import Client, calculate_karma

app = Flask(__name__)

CLIENT = Client(host="192.168.0.15", default_playlist="Dank Musics")

# url_for('static', filename='style.css')

# def vote_song(song_id, ip_addr, weight):
#     return CLIENT.vote_song(song_id, ip_addr, int(weight))

def search_song(term):
    return term

def get_song_list():
    # Magic begins here
    return [elem for elem in CLIENT.queue][::-1]

@app.route('/', methods=['GET'])
def index():
    error = None
    return render_template('index.html',
        ERROR=error,
        SONGS=get_song_list(),
        F_KARMA=calculate_karma)

@app.route('/getKarma', methods=['GET'])
def getKarma():
    song_id = request.args.get("song", "")
    print(song_id)
    # return "5"
    return calculate_karma(song_id)

@app.route('/vote', methods=['POST'])
def vote():
    return str(CLIENT.vote_song(
            request.form['song_id'], 
            request.environ['REMOTE_ADDR'], 
            int(request.form['weight'])))

@app.route('/search')
def search():
    searchterm = request.args.get('term', '')
    return search_song(searchterm)

if __name__ == "__main__":
    app.run()
