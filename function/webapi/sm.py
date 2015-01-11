#-*- encoding: utf-8 -*-

import sys
reload(sys).setdefaultencoding("utf8")

import urllib
import urllib2
import json

def reply(url, s):
    try:
        response = urllib2.urlopen(url + urllib.quote(s.encode("utf8")))
        data = response.read()
        re = data[6:-2]
        return re.decode("unicode-escape")
    except:
        return "玩坏掉了。"