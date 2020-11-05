import tweepy
import random
import itertools
from tmdbv3api import TMDb, Movie, Discover
import collections
import time
import re
from config import create_api, create_tmdb

# Genre ID cache
dict = {'28':'Action' , '12':'Adventure' , '16':'Animation' , '35':'Comedy' , '80':'Crime' , '99':'Documentary' , '18':'Drama' , '10751':'Family' , \
    '14':'Fantasy' , '36':'History' , '27':'Horror' , '10402':'Music' , '9648':'Mystery' , '10749':'Romance' , '878':'Science Fiction' , \
    '10770':'TV Movie' , '53':'Thriller' , '10752':'War' , '37':'Western'}

def post_movie(api, cgi = '27'):
    # Choose Genre
    cgi = random.choice(list(dict.keys()))
        
    # Create recommendation
    discover = Discover()
    movie = discover.discover_movies({'with_genres': cgi, 'with_original_language': 'en', 'release_date.lte': '2020-02-02', \
        'vote_average.gte': '7', 'vote_count.gte': '100', 'page': str(random.randint(1, 5))})
    rec = random.choice(movie)
        
    # Get IMDB ID
    movieimd = Movie()
    imd = movieimd.details(rec.id)
        
    # Create hashtags
    namehash = '#' + re.sub(r'\W+', '', rec.title)
    genhash = '#' + re.sub(r'\W+', '', dict[str(rec.genre_ids[0])])
        
    # Create post string
    tweet = '𝗧𝗶𝘁𝗹𝗲: ' + rec.title + '\n𝗚𝗲𝗻𝗿𝗲: ' + dict[str(rec.genre_ids[0])] + '\n𝗬𝗲𝗮𝗿: ' + rec.release_date[0:4] + \
        '\n𝗦𝗰𝗼𝗿𝗲: ' + str(int(rec.vote_average*10)) + "%" + '\n\nWas it worth the watch? ' + namehash + ' ' + genhash + \
        '\nhttps://www.imdb.com/title/' + imd.imdb_id 
    
    return tweet

def main():
    # Create tmdb object
    tmdb = create_tmdb()
    # Create API object
    api = create_api()
    while True:
        # Post tweet
        api.update_status(post_movie(api))
        # Wait for next post
        time.sleep(10800)

if __name__ == "__main__":
    main()