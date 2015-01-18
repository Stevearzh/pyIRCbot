#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import sys
reload(sys).setdefaultencoding("utf8")

import re
import ircbot
import function
import helpcmd

# Change IRC configuration here
ircHost = "irc.freenode.net"
ircPort = 8000
botName = "bzzzt_fake_taxi"
botPass = ""
ircChan = "#linuxba"
ircLeng = 130

# Change API here
tulingURL = "http://www.tuling123.com/openapi/api?key=b1833040534a6bfd761215154069ea58&info="
chatURL = tulingURL
jokeURL = tulingURL
maximURL = "http://api.hitokoto.us/rand?charset=utf-8"
smURL = "http://xiaofengrobot.sinaapp.com/web.php?para="
trickURL = tulingURL
weatherURL = tulingURL
ipURL = "http://ip.taobao.com/service/getIpInfo.php?ip="

filterMap = [
	(helpcmd,                   " ",        lambda s: re.search(R"PRIVMSG(.+?):\>h$", s.strip())),
	(function.webapi.chat,      chatURL,    lambda s: re.search(R"PRIVMSG(.+?):\>b (.+)", s).group(2)),
	(function.webapi.joke,      jokeURL,    lambda s: re.search(R"PRIVMSG(.+?):\>j$", s.strip())),
	(function.webapi.maxim,     maximURL,   lambda s: re.search(R"PRIVMSG(.+?):\>m$", s.strip())),
	(function.webapi.sm,        smURL,      lambda s: re.search(R"PRIVMSG(.+?):\>s (.+)", s).group(2)),
	(function.webapi.trick,     trickURL,   lambda s: re.search(R"PRIVMSG(.+?):\>u (.+)", s).group(2)),
	(function.webapi.weather,   weatherURL, lambda s: re.search(R"PRIVMSG(.+?):\>w (.+)", s).group(2)),
	(function.fenci,            " ",        lambda s: re.search(R"PRIVMSG(.+?):\>f (.+)", s).group(2)),
	(function.webapi.ping,      " ",        lambda s: re.search(R"privmsg(.+?):ping\!$", s.strip().lower())),
	(function.webapi.ip,        ipURL,      lambda s: re.search(R"PRIVMSG(.+?):\>i (.+)", s).group(2).strip())
]


bot = ircbot.ircBot(ircHost, ircPort, botName, botPass, ircChan)
check_the_water_meter = ircbot.ip_once()
bot.createConnection()

while True:
	for message in bot.receiveData():
		print message
		bot.responsePingfromServer(message)
		bot.searchUserLocation(message, ipURL, check_the_water_meter)

		for (filterMod, filterUrl, filterFun) in filterMap:
			try:
				if filterFun(message):
					nickname = re.match(r"^:([^!]+)", message).group(1)
					content = filterFun(message)
					replies = filterMod.reply(filterUrl, content)
					print "<<< " + nickname
					bot.replyMessage(replies, nickname, ircLeng)
			except Exception as e:
				pass
