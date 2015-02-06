#!/usr/local/bin/python
# -*- coding: utf-8 -*-
#
# Lyrics Crawler Library
#
#############################################
#author:        vanita5
#license:       MIT
#website:       https://vanita5.de
#contact:       mail@vanita5.de
#twitter:       https://twitter.com/_vanita5
#############################################

import re
import requests
import bs4
from bs4 import BeautifulSoup, Comment
from lyricfetch import LyricClient

def get_lyrics(artist, song):
    lyrics = ''

    #Wikia
    #lyrics = get_wikia_lyrics(artist, song)
    if lyrics is not None and len(lyrics) > 0:
        return lyrics

    #Wikia Manual
    lyrics = get_wikia_lyrics_2(artist, song)
    if lyrics is not None and len(lyrics) > 0:
        return lyrics

    #azlytics
    lyrics = get_azlyrics_lyrics(artist, song)
    if lyrics is not None and len(lyrics) > 0:
        return lyrics


    #songtexte
    lyrics = get_songtexte_lyrics(artist, song)
    if lyrics is not None and len(lyrics) > 0:
        return lyrics

    #None
    return lyrics
    

def get_wikia_lyrics(artist, song):
    client = LyricClient()
    return client.get_lyrics(artist, song)

def get_wikia_lyrics_2(artist, song):
    url = 'http://lyrics.wikia.com/%s:%s' % (artist, song)
    r = requests.get(url)

    if r.status_code is not 200:
        return None

    soup = BeautifulSoup(r.text)

    lyricbox = soup.find(class_='lyricbox')

    if not lyricbox:
        return None

    # Remove "NewPP limit report" from wiki sites and other HTML comments
    [s.extract() for s in lyricbox(text=lambda text: isinstance(text, Comment))]

    # Remove all script elements
    [s.extract() for s in lyricbox('script')]

    # Extract and store lyrics
    lyrics = ''

    for content in lyricbox.contents:
        tag = content.name

        # Append content if there is no tag (ie. the element is plain text)
        if not tag:
            # Skip line if it's contained in brackets
            if re.match('\[.+\]', content):
                continue
                
            lyrics += content + '\n'

    return lyrics

def get_azlyrics_lyrics(artist, song):
    url = "http://www.azlyrics.com/lyrics/{}/{}.html".format(artist.lower(), song.lower())
    page = requests.get(url)
    lyrics = re.search(b'<!-- start of lyrics -->(?:\r\n)+(.+)(?:\r\n)+<!-- end of lyrics -->', page.content, re.DOTALL)
    if lyrics:
        # Strip html tags from decoded lyrics
        return re.sub(r'<.+>', '', lyrics.group(1).decode('utf8'))
    else:
        return None

def get_songtexte_lyrics(artist, song):
    url = 'http://www.songtexte.com/search?c=all&q=%s+%s' % (artist, song)
    url = url.replace(' ', '+')

    r = requests.get(url)
    
    if r.status_code is not 200:
        return None
    
    soup = BeautifulSoup(r.text)

    tophit_c = soup.find(class_='topHitLink')

    if tophit_c is None:
        return None

    tophitlink = 'http://www.songtexte.com/' + tophit_c['href']

    r = requests.get(tophitlink)

    if r.status_code is not 200:
            return None

    soup = BeautifulSoup(r.text)

    lyrics_div = soup.find(id='lyrics')
    
    lyrics = ''
    for content in lyrics_div.contents:
        if type(content) is bs4.element.Tag:
            lyrics += '\n'
        else:
            lyrics += content            

    if lyrics == 'Leider kein Songtext vorhanden.':
        return None

    return lyrics
