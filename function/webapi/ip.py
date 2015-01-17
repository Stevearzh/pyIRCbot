#-*- encoding: utf-8 -*-

import sys
reload(sys).setdefaultencoding("utf8")

import urllib
import urllib2
import socket
import json
import re

def reply(url, s):
    try:
        response = urllib2.urlopen(url + s)
        data = response.read()
        result = json.loads(data)
        if result['code'] == 0:
            result = result['data']
            replies = result['country'] + result['region'] + result['city'] + result['county'] + result['isp']
            return replies
        elif socket.gethostbyname(s):
            ip = socket.gethostbyname(s)
            response = urllib2.urlopen(url + ip)
            data = response.read()
            result = json.loads(data)
            if result['code'] == 0:
                result = result['data']
                replies = result['country'] + result['region'] + result['city'] + result['county'] + result['isp']
                return replies

        return "地址错误，请重新输入！"
    except:
        return "玩坏掉了。"
