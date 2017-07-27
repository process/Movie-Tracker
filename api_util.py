import os
import re

import tmdbsimple as tmdb

tmdb.API_KEY = os.environ.get('TMDB_API_KEY')

def get_movie_info_from_link(link):
    movie_num = re.search('movie\/([0-9]+)', link).group(1)
    movie_info = tmdb.Movies(int(movie_num)).info()
    return movie_info
