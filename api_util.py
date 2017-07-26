import os
import re

import tmdbsimple as tmdb
from dateutil import parser

tmdb.API_KEY = os.environ.get('TMDB_API_KEY')

def get_movie_year_from_link(link):
    movie_num = re.search('movie\/([0-9]+)', link).group(1)
    movie_info = tmdb.Movies(int(movie_num)).info()
    release_date = movie_info['release_date']
    return parser.parse(release_date).year
