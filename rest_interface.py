from flask import *

app = Flask(__name__)

# url_for('static', filename='style.css')

def vote_song(song_id, weight):
    print(song_id, weight)
    return str(0)

def search_song(term):
    return term

@app.route('/', methods=['POST', 'GET'])
def index():
    error = None
    if request.method == 'POST':
        return vote_song(request.form['song_id'], request.form['weight'])
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('index.html', error=error)

@app.route('/search')
def search():
    searchterm = request.args.get('term', '')
    return search_song(searchterm)

if __name__ == "__main__":
    app.run()