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
import twitter_to_md

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

def main():
    screen_name = get_config.get_screen_name()
    since_id = get_config.get_since_id()
    api = get_config.getAPI()
    logger.debug(api)
    max_id = 731001512252465153
    twitter_to_md.get_many_statuses(api, screen_name, max_id = max_id, since_id = since_id)


if __name__ == "__main__":
    main()
