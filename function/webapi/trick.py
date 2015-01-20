#-*- encoding: utf-8 -*-

import urllib.request
import json

trickURL = "http://www.tuling123.com/openapi/api?key=b1833040534a6bfd761215154069ea58&info="

def reply(string):
    try:
        if len(string.strip()) < 9:
            response = urllib.request.urlopen(trickURL + urllib.request.quote(("笑话 大基佬" + string).encode("utf8")))
        else:
            response = urllib.request.urlopen(trickURL + urllib.request.quote(("笑话 " + string).encode("utf8")))
        data = response.read()
        result = json.loads(data.decode("utf8"))
        finalResult = result['text']
        return finalResult
    except:
        return "玩坏掉了。"