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
botName = "bzzzt"
botPass = ""
ircChan = "#linuxba"
ircLeng = 180

# Change API here
tulingURL = "http://www.tuling123.com/openapi/api?key=b1833040534a6bfd761215154069ea58&info="
chatURL = tulingURL
jokeURL = tulingURL
maximURL = "http://api.hitokoto.us/rand?charset=utf-8"
smURL = "http://xiaofengrobot.sinaapp.com/web.php?para="
trickURL = tulingURL
weatherURL = tulingURL
ipURL = "http://ip.taobao.com/service/getIpInfo.php?ip="
py3URL = "http://www.pythontutor.com/web_exec_py3-1.py?raw_input_json=&options_json=%7B%22cumulative_mode%22%3Afalse%2C%22heap_primitives%22%3Afalse%2C%22show_only_outputs%22%3Afalse%2C%22py_crazy_mode%22%3Afalse%2C%22origin%22%3A%22opt-frontend.js%22%2C%22survey%22%3A%7B%22ver%22%3A%22v4%22%2C%22testing_group%22%3A%22a%22%7D%7D&diffs_json=&user_script="

filterMap = [
	(helpcmd,                   " ",        lambda s: re.search(R"PRIVMSG(.+?):\>h$", s.strip())),
	(function.webapi.chat,      chatURL,    lambda s: re.search(R"PRIVMSG(.+?):\>b (.+)", s).group(2).strip()),
	(function.webapi.joke,      jokeURL,    lambda s: re.search(R"PRIVMSG(.+?):\>j$", s.strip())),
	(function.webapi.maxim,     maximURL,   lambda s: re.search(R"PRIVMSG(.+?):\>m$", s.strip())),
	(function.webapi.sm,        smURL,      lambda s: re.search(R"PRIVMSG(.+?):\>s (.+)", s).group(2).strip()),
	(function.webapi.trick,     trickURL,   lambda s: re.search(R"PRIVMSG(.+?):\>u (.+)", s).group(2).strip()),
	(function.webapi.weather,   weatherURL, lambda s: re.search(R"PRIVMSG(.+?):\>w (.+)", s).group(2).strip()),
	(function.fenci,            " ",        lambda s: re.search(R"PRIVMSG(.+?):\>f (.+)", s).group(2).strip()),
	(function.webapi.ping,      " ",        lambda s: re.search(R"privmsg(.+?):ping\!$", s.strip().lower())),
	(function.webapi.ip,        ipURL,      lambda s: re.search(R"PRIVMSG(.+?):\>i (.+)", s).group(2).strip())
]

filterMap2 = [
	(function.webapi.py3exec,   py3URL,     lambda s: re.search(R"PRIVMSG(.+?):\>\>\> (.+)", s).group(2).strip())
]

bot = ircbot.ircBot(ircHost, ircPort, botName, botPass, ircChan)
# check_the_water_meter = ircbot.ip_once()
bot.createConnection()

while True:
	for message in bot.receiveData():
		print message
		bot.responsePingfromServer(message)
#		bot.searchUserLocation(message, ipURL, check_the_water_meter)
		bot.searchUserLocation(message, ipURL)

		for (filterMod, filterUrl, filterFun) in filterMap:
			try:
				if filterFun(message):
					fromnick = re.match(r"^:([^!]+)", message).group(1)
					channel = re.search(R"PRIVMSG(.+?):", message).group(1).strip()
					content = filterFun(message)
					replies = filterMod.reply(filterUrl, content)
					print "<<< " + fromnick
					bot.replyMessage(fromnick, replies, channel, fromnick, ircLeng)
			except Exception as e:
				pass

		for (filterMod, filterUrl, filterFun) in filterMap2:
			try:
				if filterFun(message):
					fromnick = re.match(r"^:([^!]+)", message).group(1)
					channel = re.search(R"PRIVMSG(.+?):", message).group(1).strip()
					content = filterFun(message)
					replies = filterMod.reply(filterUrl, content)
					print "<<< " + fromnick
					bot.replyMessage(fromnick, replies, channel)
			except Exception as e:
				pass
