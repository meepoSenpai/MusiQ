from flask import *

app = Flask(__name__)
SERVERNAME = "http://localhost:5000"

# url_for('static', filename='style.css')

def vote_song(song_id, weight):
    print(song_id, weight)
    return str(weight)

def search_song(term):
    return term

def get_song_list():
    return [("song1_id", "Song 1", "5"), ("song2_id", "Song 2", "3")]

@app.route('/', methods=['POST', 'GET'])
def index():
    error = None
    if request.method == 'POST':
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