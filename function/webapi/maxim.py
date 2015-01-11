#-*- encoding: utf-8 -*-

import sys
reload(sys).setdefaultencoding("utf8")

import urllib
import urllib2
import json

def reply(url):
    try:
        response = urllib2.urlopen(url)
        data = response.read()
        result = json.loads(data.decode("utf8"))
        if result['source']:
        	re = result['hitokoto'] + " ——  " + result['author'] + "，" + result['source']
        else:
        	re = result['hitokoto'] + " ——  " + result['author']
        return re.decode("utf8")
    except:
        return "玩坏掉了。"