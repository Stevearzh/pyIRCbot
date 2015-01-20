#-*- encoding: utf-8 -*-

import sys
reload(sys).setdefaultencoding("utf8")

import urllib
import urllib2
import socket
import json
import re

reIPv4 = "((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){1,3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])"
reIPv6 = "((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?"
reURL  = "([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}"

taobaoURL = "http://ip.taobao.com/service/getIpInfo.php?ip="
GeoIPURL = "http://ip-api.com/json/"

def ipv4Search(ip):
    response = urllib2.urlopen(taobaoURL + urllib.quote(ip.encode("utf8")))
    data = response.read()
    result = json.loads(data)
    if result['code'] == 0:
        result = result['data']
        replies = result['country'] + result['region'] + result['city'] + result['county'] + result['isp']
    else:
        replies = "玩坏掉了。"

    return replies

def ipv6Search(ip):
    response = urllib2.urlopen(GeoIPURL + urllib.quote(ip.encode("utf8")))
    data = response.read()
    result = json.loads(data.strip())
    if result['status'] == "success":
        replies = result['country'] + ", " + result['regionName'] + ", " + result['city'] + ", " + result['isp']
    else:
        replies = "玩坏掉了。"

    return replies

def reply(string):
    try:
        if re.match(reIPv4, string):
            finalResult = ipv4Search(string)
        elif re.match(reIPv6, string):
            finalResult = ipv6Search(string)
        elif re.match(reURL, string):
            finalResult = ipv4Search(socket.gethostbyname(string))
        else:
            finalResult = "玩坏掉了。"

        return finalResult
    except:
        return "玩坏掉了。"
