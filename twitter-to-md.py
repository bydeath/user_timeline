#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ===================================================================
#     FileName: twitter-to-xhtml.py
#        Email: brucvv@gmail.com
#   CreateTime: 2016-04-29 18:45
# ===================================================================


'''Load the latest update for a Twitter user
and leave it in an markdown fragment'''


import codecs
import sys
import os
import logging
import time
import socket
import get_config
sys.path.append('../python-twitter/')
from twitter import Status

FORMAT = '%(asctime)s %(message)s'
DATEFMT = '%m/%d/%Y %H:%M:%S'
logging.basicConfig(format=FORMAT, datefmt=DATEFMT)
logger = logging.getLogger('user_timeline')
logger.setLevel(logging.INFO)
POST_TEMPLATE = """---
date: %s
imgs: %s
---
%s
"""


def generate_filename(N=8):
    import string
    import random
    identifiers = string.ascii_letters + string.digits
    return ''.join(random.SystemRandom().choice(identifiers) for _ in range(N))


def media_download(url, path):
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
    logger.debug("since_id:%s" % since_id)
    statuses = api.GetUserTimeline(screen_name=user, since_id=since_id)
    logger.info("get %s status" % len(statuses))
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
                    filename = os.path.join(
                            "/assets", ''.join([generate_filename(), '.jpg']))
                    media_download(url, filename)
                    imgs.append(filename)
            logger.debug(imgs)
            wraped_link_text = _wrap_links_intext(s)
            xhtml = POST_TEMPLATE % (s.created_at, imgs, wraped_link_text)
            output = os.path.join('_posts', generate_post_name())
            xhtml = _escape_vertical(xhtml)
            Save(xhtml, output)
            logger.debug("post just saved")
        return statuses[0].id


def _wrap_links_intext(status):
    text = status.text
    for url in status.urls:
        wraped_link = '<a href="%s">%s</a>' % (url.expanded_url, url.url)
        text = text.replace(url.url, wraped_link)
    return text


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
    screen_name = get_config.get_screen_name()
    since_id = get_config.get_since_id()
    api = get_config.getAPI()
    logger.debug(api)
    while True:
        since_id = FetchTwitter(api, screen_name, since_id=since_id)
        time.sleep(30)


if __name__ == "__main__":
    main()
    # api = getapi.getAPI()
    # status = FetchStatus(api, 729184024493576193)
    # print(type(status))
    # print(status)
    # status = FetchStatus(api, 729501254087495681)
    # print(type(status))
    # print(status)
    # status = FetchStatus(api, 728785179053973504)
    # print(status)
    # print(_wrap_links_intext(status))
    # data = FetchOembedStatus(api, 728583447598370816)
    # print(data)
    # status = Status.AsJsonString(status)
    # print(type(status))
    # save_json(status, 'a.json')
    # data = FetchOembedStatus(api, 728583447598370816)
    # print(data)
