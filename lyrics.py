#!/usr/local/bin/python
# -*- coding: utf-8 -*-
#
# Lyrics Lastfm Twitter Bot
#
#############################################
#author:        vanita5
#license:       MIT
#website:       https://vanita5.de
#contact:       mail@vanita5.de
#twitter:       https://twitter.com/_vanita5
#############################################

import re
import os
import time
import tweepy
import logging
import sys
import os
import json
import urllib2
import random
from config import *
from lyrics_r import *
from collections import namedtuple

# Track tuple definition
Track = namedtuple('Track', ['artist', 'song', 'now_playing'])

def prnt(string):
    if DEBUG:
        print string

def is_now_playing(item):
    try:
        if item['@attr']['nowplaying'] == 'true':
            return True
    #except KeyError, e:
    except:
        return False

def get_nowplaying():
    url = 'http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=%s&api_key=%s&limit=1&format=json' % (LASTFM_USERNAME, LASTFM_API_KEY)
    
    # load the raw JSON via HTTP GET request
    j = json.load(urllib2.urlopen(url))

    try:
        t = j['recenttracks']['track'][0]
    except:
        return None

    track = Track(
        artist = t['artist']['#text'].encode('utf-8'),
        song = t['name'].encode('utf-8'),
        now_playing = is_now_playing(t)
    )

    if (track.now_playing):
        return track
        
    return None

def get_tweet_from_lyrics(lyrics):
    if len(lyrics) <= 140:
        return lyrics

    tweet = ''
    lines = lyrics.splitlines()
    c = len(lines)
    s = random.randint(0, c - 2)
    r = random.randint(1, 8)
    prnt('Tweet will have ' + str(r) + ' lines!')
    cn = 0

    for i in range(s, c - 1):
        line = lines[i]
        
        if len(tweet + line) <= 140 and cn < r:
            tweet += '\n' + line
            cn+=1
        else:
            return tweet


#Logging
logging.basicConfig(filename= os.path.dirname(os.path.abspath(__file__)) + '/Logfile.log', level=logging.WARNING)
logging.info('Lyrics bot started')
log = logging.getLogger('module')

#OAuth
prnt('[API]:')
try:
    auth = tweepy.OAuthHandler(CKEY, CSECRET)
    auth.set_access_token(AKEY, ASECRET)
    api = tweepy.API(auth)

    ME = api.me()
    prnt('OK\n')
except Exception, e:
    print 'Authentication Failed: ' + str(e)
    exit()


while True:
    time.sleep(INTERVAL)
    try:
        song = get_nowplaying()

        if song is not None:            
            prnt('Song: ' + str(song) + '\n')
            
            lyrics = get_lyrics(song.artist, song.song)
            if lyrics is None or len(lyrics) <= 0:
                continue                
            else:
                lyrics = lyrics.encode('utf-8')
                prnt('Lyrics: ' + str(lyrics) + '\n')
                tweet = get_tweet_from_lyrics(lyrics)
                prnt('Updating Status: ' + str(tweet) + '\n\n')
                
                result = api.update_status(status=tweet)
                prnt('Status: \n' + str(result))

    except Exception, e:
        log.exception('Exception: ')
        continue                    
    
exit()
