# Lastfm-Twitter-Lyrics-Bot
Twitter bot that posts random lyrics parts of the song you are currently scrobbling on last.fm

## Requirements
* Last.fm account
* Last.fm API Keys
* Twitter Account for the bot
* Twitter API Keys


* Python 2.7
* tweepy
* requests
* BeautifulSoup
* Lyricfetch

### Installation

    pip install tweepy
    pip install requests
    pip install beautifulsoup4
    pip install git+git://github.com/cbelden/lyricfetch.git@master
    pip install git+git://github.com/boyska/lyricseek.git@master

* Edit the config.py

Congratulations, you're ready to go. Just let *lyrics.py* run in the background somewhere.
**Note**: Python 3.x will probably not work. Make sure to run the script with version 2.7.


## Example Bot
[The last.fm account](http://www.lastfm.de/user/3liah)

[The Twitter Bot](https://twitter.com/lyrics_vanita5)

I additionally connected the bot to last.fm with [IFTTT](https://ifttt.com/) to automatically change the 
profile picture to the album cover of the last track and to post a tweet when I favorite a song.
