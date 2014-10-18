#!/usr/bin/env python2
#-*- encoding: utf-8 -*-

import sys
reload(sys).setdefaultencoding("utf8")

import urllib
import urllib2
import json

def reply(s):
    try:
        response = urllib2.urlopen("http://www.tuling123.com/openapi/apikey=b1833040534a6bfd761215154069ea58&info=笑话")
        data = response.read()
        result = json.loads(data.decode("utf8"))
        re = result['text']
        return re.decode("utf8")
    except:
        return "玩坏掉了。"