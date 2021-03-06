#!/usr/bin/env python

'''get twitter OAuth api and config option'''


import configparser as ConfigParser
import os
import sys
sys.path.append('../python-twitter/')
import twitter


class TweetRc(object):
    def __init__(self):
        self._config = None

    def GetConsumerKey(self):
        return self._GetOption('consumer_key')

    def GetConsumerSecret(self):
        return self._GetOption('consumer_secret')

    def GetAccessKey(self):
        return self._GetOption('access_key')

    def GetAccessSecret(self):
        return self._GetOption('access_secret')

    def GetScreenName(self):
        return self._GetOption('screen_name')

    def GetSinceId(self):
        return self._GetOption('since_id')

    def _GetOption(self, option):
        try:
            return self._GetConfig().get('Tweet', option)
        except:
            return None

    def _GetConfig(self):
        if not self._config:
            self._config = ConfigParser.ConfigParser()
            self._config.read(os.path.expanduser('~/.tweetrc'))
        return self._config


def getAPI():
    rc = TweetRc()
    consumer_key = rc.GetConsumerKey()
    consumer_secret = rc.GetConsumerSecret()
    access_key = rc.GetAccessKey()
    access_secret = rc.GetAccessSecret()
    if not consumer_key or \
            not consumer_secret or not access_key or not access_secret:
        sys.exit(0)
    api = twitter.Api(
        consumer_key=consumer_key, consumer_secret=consumer_secret,
        access_token_key=access_key, access_token_secret=access_secret,
        timeout=20)
    return api


def get_screen_name():
    rc = TweetRc()
    return rc.GetScreenName()


def get_since_id():
    rc = TweetRc()
    return int(rc.GetSinceId())
