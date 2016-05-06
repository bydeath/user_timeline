#!/usr/bin/env python

'''Post a message to twitter'''

__author__ = 'dewitt@google.com'

import ConfigParser
import getopt
import os
import sys
sys.path.append('../python-twitter/')
import twitter


USAGE = '''Usage: tweet [options] message

  This script posts a message to Twitter.

  Options:

    -h --help : print this help
    --encoding : the character set encoding used in input strings, e.g. "utf-8". [optional]

  Documentation:

  If either of the command line flags are not present, the environment
  variables TWEETUSERNAME and TWEETPASSWORD will then be checked for your
  consumer_key or consumer_secret, respectively.

  If neither the command line flags nor the environment variables are
  present, the .tweetrc file, if it exists, can be used to set the
  default consumer_key and consumer_secret.  The file should contain the
  following three lines, replacing *consumer_key* with your consumer key, and
  *consumer_secret* with your consumer secret:

  A skeletal .tweetrc file:

    [Tweet]
    consumer_key: *consumer_key*
    consumer_secret: *consumer_password*
    access_key: *access_key*
    access_secret: *access_password*

'''


def PrintUsageAndExit():
    print USAGE
    sys.exit(2)


def GetConsumerKeyEnv():
    return os.environ.get("TWEETUSERNAME", None)


def GetConsumerSecretEnv():
    return os.environ.get("TWEETPASSWORD", None)


def GetAccessKeyEnv():
    return os.environ.get("TWEETACCESSKEY", None)


def GetAccessSecretEnv():
    return os.environ.get("TWEETACCESSSECRET", None)


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
    if not consumer_key or not consumer_secret or not access_key or not access_secret:
        PrintUsageAndExit()
    api = twitter.Api(consumer_key=consumer_key, consumer_secret=consumer_secret,
                      access_token_key=access_key, access_token_secret=access_secret, timeout=20)
    return api

def main():
    try:
        shortflags = 'h'
        longflags = ['help', 'consumer-key=', 'consumer-secret=',
                     'access-key=', 'access-secret=', 'encoding=']
        opts, args = getopt.gnu_getopt(sys.argv[1:], shortflags, longflags)
    except getopt.GetoptError:
        PrintUsageAndExit()
    for o, a in opts:
        if o in ("-h", "--help"):
            PrintUsageAndExit()
        if o in ("--encoding"):
            encoding = a
    message = ' '.join(args)
    if not message:
        PrintUsageAndExit()
    api = getAPI()
    try:
        status = api.PostUpdate(message)
    except UnicodeDecodeError:
        print "Your message could not be encoded.  Perhaps it contains non-ASCII characters? "
        print "Try explicitly specifying the encoding with the --encoding flag"
        sys.exit(2)
    print "%s just posted: %s" % (status.user.name, status.text)


if __name__ == "__main__":
    main()
