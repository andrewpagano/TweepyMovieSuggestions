#!/usr/bin/env python
# tweepy-bots/bots/replydm.py

import tweepy
import logging
from config import create_api
import time
from postmovie import post_movie
import collections
import itertools

# Genre ID cache
dict = {'28':'Action' , '12':'Adventure' , '16':'Animation' , '35':'Comedy' , '80':'Crime' , '99':'Documentary' , '18':'Drama' , '10751':'Family' , \
    '14':'Fantasy' , '36':'History' , '27':'Horror' , '10402':'Music' , '9648':'Mystery' , '10749':'Romance' , '878':'Science Fiction' , \
    '10770':'TV Movie' , '53':'Thriller' , '10752':'War' , '37':'Western'}


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def reply_dm(api):
    logger.info("Retrieving latest dm")
    #Get newest dm
    last_dms = api.list_direct_messages()
    
    
    for messages in last_dms:
        logger.info("#of DMs: " + str(len(last_dms)))
        logger.info("MY ID " + str(api.get_user("_What_to_watch_").id))
        logger.info(str("SENDER ID " + messages.message_create['sender_id']))
        if int(messages.message_create['sender_id']) != api.get_user("_What_to_watch_").id:
            logger.info("Checking lastest dm")
            #Look up sent genre
            txt = messages.message_create['message_data']['text']
            txt = txt.lower().capitalize()
            
            #Genre not found
            if not txt in list(dict.values()):
                logger.info("Could not find genre " + txt)
                genlist = ''
                for g in list(dict.values()):
                    genlist+=g
                    genlist+='\n'
                api.send_direct_message(messages.message_create['sender_id'], "Hello! Please reply to a tweet with a movie genre " + \
                    "and I will give you a recommendation!\nAccpeted genres: " + genlist)
                return
            
            #Send reply recommendation
            
            gen = list(dict.keys())[list(dict.values()).index(txt)]
            logger.info("Sending " + gen)
            api.send_direct_message(messages.message_create['sender_id'], str(post_movie(api, gen)))
        else:
            logger.info("I SENT LAST MSG-----------")
            return
    logger.info("No More Dms!!!!!")

def main():
    api = create_api()
    while True:
        reply_dm(api)
        logger.info("Waiting...")
        time.sleep(65)

if __name__ == "__main__":
    main()