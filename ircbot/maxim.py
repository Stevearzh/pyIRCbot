#!/usr/bin/env python2
#-*- encoding: utf-8 -*-

import sys
reload(sys).setdefaultencoding("utf8")

import urllib
import urllib2
import json

def reply(s):
    try:
        response = urllib2.urlopen("http://api.hitokoto.us/rand?charset=utf-8")
        data = response.read()
        result = json.loads(data.decode("utf8"))
        if result['source']:
        	re = result['hitokoto'] + " ——  " + result['author'] + "，" + result['source']
        else:
        	re = result['hitokoto'] + " ——  " + result['author']
        return re.decode("utf8")
    except:
        return "玩坏掉了。"