#!/usr/bin/env python2
#-*- encoding: utf-8 -*-

import sys
reload(sys).setdefaultencoding("utf8")

import urllib
import urllib2
import json

def reply(s):
    try:
        response = urllib2.urlopen("http://www.tuling123.com/openapi/api?key=14fa01eeb5479d7d8c1e8989eeeb0bc3&info=" + urllib.quote(s.encode("utf8")))
        data = response.read()
        result = json.loads(data)
        re = result['text']
        return re.decode("utf8")
    except:
        return "玩坏掉了。"
