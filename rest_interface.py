from flask import request, Flask, render_template
from party_generator import Client

app = Flask(__name__)
SERVERNAME = "http://localhost:5000"

CLIENT = Client()

# url_for('static', filename='style.css')

def vote_song(song_id, ip_addr, weight):
    CLIENT.vote_song(song_id, ip_addr, int(weight))
    return str(weight)

def search_song(term):
    return term

def get_song_list():
    # Magic begins here
    return [elem for elem in CLIENT.queue]

@app.route('/', methods=['POST', 'GET'])
def index():
    error = None
    if request.method == 'POST':
        return vote_song(request.form['song_id'],
                         request.environ['REMOTE_ADDR'],
                         request.form['weight'])
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('index.html',
        ERROR=error,
        SONGS=get_song_list(),
        SERVERNAME=SERVERNAME)

@app.route('/search')
def search():
    searchterm = request.args.get('term', '')
    return search_song(searchterm)

if __name__ == "__main__":
    app.run()
