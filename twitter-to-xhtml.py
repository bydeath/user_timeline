#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ===================================================================
#     FileName: twitter-to-xhtml.py
#        Email: brucvv@gmail.com
#   CreateTime: 2016-04-29 18:45
# ===================================================================


'''Load the latest update for a Twitter user and leave it in an XHTML fragment'''

__author__ = 'dewitt@google.com'

import codecs
import getopt
import sys
import os
import logging
import time
import socket

# FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig()
logger = logging.getLogger('retweet')
logger.setLevel(logging.DEBUG)

sys.path.append('../python-twitter/')
import twitter

TEMPLATE = """
<div class="twitter">
  <span class="twitter-user"><a href="http://twitter.com/%s">Twitter</a>: </span>
  <span class="twitter-text">%s</span>
  <span class="twitter-relative-created-at"><a href="http://twitter.com/%s/statuses/%s">Posted %s</a></span>
</div>
"""

POST_TEMPLATE = """---
date: %s
imgs: %s
---
%s
"""


def generate_filename(N=8):
    import string
    import random
    return ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(N))

def media_download(url, path):
    import urllib2
    # proxy = urllib2.ProxyHandler({'https':'127.0.0.1:8001'})
    # opener = urllib2.build_opener(proxy)
    # urllib2.install_opener(opener)
    logger.debug(url)
    response = urllib2.urlopen(url, timeout=10)
    with open(path, 'wb') as out:
        try:
            out.write(response.read())
        except socket.timeout as e:
            logger.warning(e)
            out.write(response.read())

def FetchTwitter(api, user, since_id):
    logger.debug("since_id:%s"%since_id)
    statuses = api.GetUserTimeline(screen_name=user, since_id=since_id)
    logger.info("get % status"%len(statuses))
    if len(statuses) == 0:
        return since_id
    else:
        for s in statuses:
            logger.debug(s.id)
            medias = s.media
            imgs = []
            if medias:
                for m in medias:
                    url = m.media_url
                    filename = os.path.join("assets", ''.join([generate_filename(), '.jpg']))
                    media_download(url, filename)
                    imgs.append(filename)
            logger.debug(imgs)
            xhtml = POST_TEMPLATE % (s.created_at, imgs, s.text)
            output = os.path.join('_posts', generate_post_name())
            Save(xhtml, output)
            logger.debug("post just saved")
        return statuses[0].id

def Save(xhtml, output):
    out = codecs.open(output, mode='w', encoding='ascii',
                      errors='xmlcharrefreplace')
    out.write(xhtml)
    out.close()

def generate_post_name():
    from time import gmtime, strftime
    date = strftime("%Y-%m-%d-%H-%M-%S", gmtime())
    return "%s-%s.md" % (date, generate_filename())

def main():
    import getapi
    since_id = 727783883920441344
    user = 'rangxiangzi'
    api = getapi.getAPI()
    logger.debug(api)
    while True:
        since_id = FetchTwitter(api, user, since_id = since_id)
        time.sleep(30)


if __name__ == "__main__":
    main()
    # for i in range(50):
        # media_download('http://pbs.twimg.com/media/ChnbrBAUkAAmttc.jpg', 'a.jpg')
        # time.sleep(5)
