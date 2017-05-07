from flask import request, Flask, render_template
from musi_q import Client, calculate_karma

app = Flask(__name__)

CLIENT = Client(host="192.168.178.48",default_playlist="Dank Musics")

# url_for('static', filename='style.css')

def vote_song(song_id, ip_addr, weight):
    CLIENT.vote_song(song_id, ip_addr, int(weight))

def search_song(term):
    return term

def get_song_list():
    # Magic begins here
    return [elem for elem in CLIENT.queue][::-1]

@app.route('/', methods=['POST', 'GET'])
def index():
    error = None
    if request.method == 'POST':
        return "test"
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('index.html',
        ERROR=error,
        SONGS=get_song_list(),
        F_KARMA=calculate_karma)

@app.route('/vote', methods=['POST'])
def vote():
    CLIENT.vote_song(
        request.form['song_id'], 
        request.environ['REMOTE_ADDR'], 
        int(request.form['weight']))
    return "You will never see this"

@app.route('/search')
def search():
    searchterm = request.args.get('term', '')
    return search_song(searchterm)

if __name__ == "__main__":
    app.run()
