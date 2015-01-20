#-*- encoding: utf-8 -*-

import sys
reload(sys).setdefaultencoding("utf8")

import urllib
import urllib2
import json

maximURL = "http://api.hitokoto.us/rand?charset=utf-8"

def reply(string):
    try:
        response = urllib2.urlopen(maximURL)
        data = response.read()
        result = json.loads(data.decode("utf8"))
        finalResult = result['hitokoto'] + " ——  " + result['author']
        if result['source']:
            finalResult += "，" + result['source']
        return finalResult.decode("utf8")
    except:
        return "玩坏掉了。"