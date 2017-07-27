import os

from dateutil import parser
from flask import Flask, render_template, request

from api_util import get_movie_info_from_link
from db_util import _db, get_movies_in_list, add_new_movie, add_movie_link
from file_util import get_temp_files, get_ripping_group, \
    move_temp_file_to_collection, check_tmp_filename, get_file_info_temp

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

@app.route('/temp')
def list_temp():
    temp_files = get_temp_files()
    return render_template('list_temp.html', file_list=temp_files)

@app.route('/add_movie/<file_name>')
def add_movie_form(file_name):
    ripping_group = get_ripping_group(file_name)
    return render_template('add_movie.html', file_name=file_name, ripping_group=ripping_group)

@app.route('/add_movie_from_temp', methods=['POST'])
def add_movie_from_temp():
    required_fields = ['media-source', 'file-source', 'tmdb-link']
    for field in required_fields:
        if not request.form[field]:
            return "Missing required field. Please go back."
    if not check_tmp_filename(request.form['file-name']):
        return "File not found?"
    extra_info = {}

    file_info = get_file_info_temp(request.form['file-name'])
    extra_info['codec'] = file_info.codec
    extra_info['container'] = file_info.container
    extra_info['size'] = file_info.size

    movie_info = get_movie_info_from_link(request.form['tmdb-link'])
    year = parser.parse(movie_info['release_date']).year
    extra_info['tags'] = request.form['release-tags']
    extra_info['source'] = request.form['media-source']
    extra_info['ripping_group'] = request.form['ripping-group']
    extra_info['file_source'] = request.form['file-source']

    file_name = request.form['file-name']
    file_extension = file_name.rsplit('.', 1)[-1]
    keep_characters = (' ','.','_')
    new_file_name = "".join(c for c in movie_info['title'] if c.isalnum() or c in keep_characters).rstrip()
    new_file_name += '.' + file_extension
    move_temp_file_to_collection(file_name, new_file_name)

    movie_id = add_new_movie(new_file_name, movie_info['title'], year, **extra_info)
    add_movie_link(movie_id, 'TMDb', request.form['tmdb-link'])
    return "OK"

app.run()
