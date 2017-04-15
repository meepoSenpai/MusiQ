from flask import *
from party_generator import Client

app = Flask(__name__)
SERVERNAME = "http://localhost:5000"

CLIENT = Client()
CLIENT.init_query()

# url_for('static', filename='style.css')

def vote_song(song_id, weight):
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
        CLIENT.vote_song(request.form['song_id'],
                         request.environ['REMOTE_ADDR'],
                         int(request.form['weight']))
        for elem in CLIENT.queue:
            print('{},{}'.format(elem[0].get('title'), elem[2]))
        return vote_song(request.form['song_id'], request.form['weight'])
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
