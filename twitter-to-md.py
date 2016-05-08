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
import getapi
sys.path.append('../python-twitter/')
import twitter
from twitter import Status

# FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig()
logger = logging.getLogger('retweet')
logger.setLevel(logging.DEBUG)


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
    # import urllib2
    # proxy = urllib2.ProxyHandler({'https':'127.0.0.1:8001'})
    # opener = urllib2.build_opener(proxy)
    # urllib2.install_opener(opener)
    import urllib.request
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    logger.debug(url)
    # response = urllib2.urlopen(url, timeout=10)
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
            xhtml = _escape_vertical(xhtml)
            Save(xhtml, output)
            logger.debug("post just saved")
        return statuses[0].id

def _escape_vertical(htmlStr):
    return htmlStr.replace("||", "\|\|")

def FetchStatus(api, id):
    status = api.GetStatus(status_id=id)
    return status

def FetchOembedStatus(api, id):
    data = api.GetStatusOembed(status_id=id)
    return data

def save_json(str, output):
    with open(output, 'w') as out:
        out.write(str)
    
def Save(xhtml, output):
    out = codecs.open(output, mode='w', encoding='utf-8',
                      errors='xmlcharrefreplace')
    out.write(xhtml)
    out.close()

def generate_post_name():
    from time import gmtime, strftime
    date = strftime("%Y-%m-%d-%H-%M-%S", gmtime())
    return "%s-%s.md" % (date, generate_filename())

def main():
    since_id = 727783883920441344
    user = 'fangshimin'
    api = getapi.getAPI()
    logger.debug(api)
    while True:
        since_id = FetchTwitter(api, user, since_id = since_id)
        time.sleep(30)


if __name__ == "__main__":
    main()
    # api = getapi.getAPI()
    # status = FetchStatus(api, 728583447598370816)
    # print(type(status))
    # print(status)
    # data = FetchOembedStatus(api, 728583447598370816)
    # print(data)
    # status = Status.AsJsonString(status)
    # print(type(status))
    # save_json(status, 'a.json')
    # data = FetchOembedStatus(api, 728583447598370816)
    # print(data)
