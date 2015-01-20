#-*- encoding: utf-8 -*-

import urllib.request
import json

maximURL = "http://api.hitokoto.us/rand?charset=utf-8"

def reply(string):
    try:
        response = urllib.request.urlopen(maximURL)
        data = response.read()
        result = json.loads(data.decode("utf8"))
        finalResult = result['hitokoto'] + " ——  " + result['author']
        if result['source']:
            finalResult += "，" + result['source']
        return finalResult
    except:
        return "玩坏掉了。"