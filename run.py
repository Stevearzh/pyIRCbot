#!/usr/bin/env python3
#-*- encoding: utf-8 -*-

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
ircLeng = 160


filterMap = [
	(helpcmd,                   lambda string: re.search(R"PRIVMSG(.+?):\>h$", string.strip())),
	(function.webapi.chat,      lambda string: re.search(R"PRIVMSG(.+?):\>b (.+)", string).group(2).strip()),
	(function.webapi.joke,      lambda string: re.search(R"PRIVMSG(.+?):\>j$", string.strip())),
	(function.webapi.maxim,     lambda string: re.search(R"PRIVMSG(.+?):\>m$", string.strip())),
	(function.webapi.sm,        lambda string: re.search(R"PRIVMSG(.+?):\>s (.+)", string).group(2).strip()),
	(function.webapi.trick,     lambda string: re.search(R"PRIVMSG(.+?):\>u (.+)", string).group(2).strip()),
	(function.webapi.weather,   lambda string: re.search(R"PRIVMSG(.+?):\>w (.+)", string).group(2).strip()),
	(function.fenci,            lambda string: re.search(R"PRIVMSG(.+?):\>f (.+)", string).group(2).strip()),
	(function.webapi.ping,      lambda string: re.search(R"privmsg(.+?):ping\!$", string.strip().lower())),
	(function.webapi.ip,        lambda string: re.search(R"PRIVMSG(.+?):\>i (.+)", string).group(2).strip())
]

filterMap2 = [
	(function.webapi.py3exec,   lambda string: re.search(R"PRIVMSG(.+?):\>\>\> (.+)", string).group(2).strip())
]

bot = ircbot.ircBot(ircHost, ircPort, botName, botPass, ircChan)
check_the_water_meter = ircbot.ip_once()
bot.createConnection()

while True:
	try:
		for message in bot.receiveData():
			print(message)
			bot.responsePingfromServer(message)
			bot.searchUserLocation(message, check_the_water_meter)

			for (filterMod, filterFun) in filterMap:
				try:
					if filterFun(message):
						fromnick = re.match(r"^:([^!]+)", message).group(1)
						channel = re.search(R"PRIVMSG(.+?):", message).group(1).strip()
						content = filterFun(message)
						replies = filterMod.reply(content)
						print("<<< " + fromnick)
						bot.replyMessage(fromnick, replies, channel, fromnick, ircLeng)
				except Exception as e:
					pass

			for (filterMod, filterFun) in filterMap2:
				try:
					if filterFun(message):
						fromnick = re.match(r"^:([^!]+)", message).group(1)
						channel = re.search(R"PRIVMSG(.+?):", message).group(1).strip()
						content = filterFun(message)
						replies = filterMod.reply(content)
						print("<<< " + fromnick)
						bot.replyMessage(fromnick, replies, channel)
				except Exception as e:
					pass
	except Exception as e:
		pass
