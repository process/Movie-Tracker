from flask import Flask, render_template

from db_util import _db, get_movies_in_list

app = Flask(__name__)

@app.route('/')
def list_movies():
    return render_template('index.html',
                           movies=_db('SELECT * FROM movie')[0],
                           lists=_db('SELECT * FROM user_list')[0])

@app.route('/releases/<int:movie_id>')
def list_releases(movie_id):
    return render_template('releases.html', releases=_db('SELECT * FROM release WHERE movie_id=?', movie_id)[0])

@app.route('/list/<int:user_list_id>')
def list(user_list_id):
    user_list = _db('SELECT * FROM user_list where id=?', user_list_id)[0][0]
    movies = get_movies_in_list(user_list)
    return render_template('list.html', movies=movies)

app.run()
