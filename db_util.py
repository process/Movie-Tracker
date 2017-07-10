import os
import os.path

import sqlite3

database = sqlite3.connect("database.db")
MOVIE_PATH = "/mnt/z/Videos/Movies"

# Useful queries:
# Get backlog: _db('select name from movie join user_list_mapping on movie.id=user_list_mapping.movie_id where user_list_mapping.user_list_id=4')

# TODO: Make movie directory use symlinks (Symlinks solves renaming problem)
# TODO: Use media reading lib to get proper container/codec info
# TODO: Match up movie data with PtP

class Container(object):
    MKV = 1
    AVI = 2
    MP4 = 3
    Other = 99

class Codec(object):
    x264 = 1
    MPEG4 = 2
    WMV9 = 3
    DivX = 4
    Other = 99

class Source(object):
    DVD = 1
    BluRay = 2
    WEB = 3
    Other = 99

class FileSource(object):
    PtP = 1
    PtP_GP = 2
    Other = 99

def _db(cmd, *args):
    result = database.execute(cmd, args)
    database.commit()
    return list(result), result.lastrowid

def _add_movie(name, year=None, description=None):
    # Returns ID of newly inserted movie
    return _db('INSERT INTO movie (name, year, description) VALUES (?, ?, ?)', name.decode('UTF-8'), year, description)[1]

def check_missing_movie(path=MOVIE_PATH):
    missing = []
    files = os.listdir(path)
    for f in files:
        if os.path.isfile(os.path.join(path, f)):
            name = f.rsplit('.', 1)[0]
            if not _db('SELECT * FROM movie WHERE name=?', name.decode('UTF-8'))[0]:
                missing.append(name)
    return missing

def check_missing_release(path=MOVIE_PATH):
    missing = []
    files = os.listdir(path)
    for f in files:
        if os.path.isfile(os.path.join(path, f)):
            if not _db('SELECT * FROM release WHERE file_path=?', f.decode('UTF-8'))[0]:
                missing.append(f)
    return missing

def add_new_movie(path):
    # TODO: Use temp directory
    # TODO: Scrape from PtP??
    # TODO: Create symlinks
    base_name = os.path.basename(path)
    name = base_name.rsplit('.', 1)[0].decode('utf-8')
    movie_id = _add_movie(name)
    _db('INSERT INTO release (movie_id, file_path) VALUES (?, ?)', movie_id, base_name.decode('utf-8'))

def get_movie_by_name(name):
    return _db('SELECT * FROM movie WHERE name=?', name)[0][0]

def get_user_lists(user_name):
    user_id = _db('SELECT * FROM user WHERE name=?', user_name)[0][0][0]
    return _db('SELECT * FROM user_list WHERE user_id=?', user_id)[0]

def get_movies_in_list(user_list):
    list_items = _db('SELECT * FROM user_list_mapping WHERE user_list_id=?', user_list[0])[0]
    movies = []
    for item in list_items:
        movie_id = item[1]
        movies.append(_db('SELECT * FROM movie WHERE id=?', movie_id)[0][0])
    return movies

def add_movie_to_list(user_list, movie):
    _db('INSERT INTO user_list_mapping (user_list_id, movie_id) VALUES (?, ?)', user_list[0], movie[0])
