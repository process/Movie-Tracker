import os
import os.path

import sqlite3

database = sqlite3.connect("database.db")

# Useful queries:
# Get backlog: _db('select name from movie join user_list_mapping on movie.id=user_list_mapping.movie_id where user_list_mapping.user_list_id=4')

# TODO: Make movie directory use symlinks
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
    return list(result)

def add_movie(name, year=None, description=None):
    _db('INSERT INTO movie (name, year, description) values (?, ?, ?)', name.decode('UTF-8'), year, description)

def check_missing_movie(path):
    missing = []
    files = os.listdir(path)
    for f in files:
        if os.path.isfile(os.path.join(path, f)):
            name = f.rsplit('.', 1)[0]
            if not _db('SELECT * FROM movie WHERE name=?', name.decode('UTF-8')):
                missing.append(name)
    return missing

def add_releases(path):
    files = os.listdir(path)
    for f in files:
        if os.path.isfile(os.path.join(path, f)):
            if _db('SELECT * FROM release WHERE file_path = ?', f.decode('utf-8')):
                continue
            name = f.rsplit('.', 1)[0].decode('utf-8')
            movie_record = _db('SELECT * FROM movie WHERE name=?', name)[0]
            _db('INSERT INTO release (movie_id, file_path) values (?, ?)', movie_record[0], f.decode('utf-8'))

def add_new_movie(path):
    # TODO: Use temp directory
    # TODO: Scrape from PtP??
    # TODO: Create symlinks
    base_name = os.path.basename(path)
    name = base_name.rsplit('.', 1)[0].decode('utf-8')
    add_movie(name)
    movie_record = _db('SELECT * FROM movie WHERE name=?', name)
    _db('INSERT INTO release (movie_id, file_path) values (?, ?)', movie_record[0], base_name.decode('utf-8'))
