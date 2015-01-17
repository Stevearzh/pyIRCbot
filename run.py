#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import sys
reload(sys).setdefaultencoding("utf8")

import re
import ircbot
import function
import helpcmd
import socket

# Change IRC configuration here
ircHost = "irc.freenode.net"
ircPort = 8000
botName = "bzzzt"
botPass = "ynuhgv5987"
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


bot = ircbot.ircBot(ircHost, ircPort, botName, botPass, ircChan)
bot.createConnection()

while True:
	for message in bot.receiveData():
		print message
		bot.responsePingfromServer(message)

		replies = []
		if re.search(R"PRIVMSG(.+?):\>h$", message.strip()):
			replies = helpcmd.reply()
		elif re.search(R"PRIVMSG(.+?):\>b (.+)", message):
			replies = function.webapi.chat.reply(chatURL, re.search(R"PRIVMSG(.+?):\>b (.+)", message).group(2))
		elif re.search(R"PRIVMSG(.+?):\>j$", message.strip()):
			replies = function.webapi.joke.reply(jokeURL)
		elif re.search(R"PRIVMSG(.+?):\>m$", message.strip()):
			replies = function.webapi.maxim.reply(maximURL)
		elif re.search(R"PRIVMSG(.+?):\>s (.+)", message):
			replies = function.webapi.sm.reply(smURL, re.search(R"PRIVMSG(.+?):\>s (.+)", message).group(2))
		elif re.search(R"PRIVMSG(.+?):\>u (.+)", message):
			replies = function.webapi.trick.reply(trickURL, re.search(R"PRIVMSG(.+?):\>u (.+)", message).group(2))
		elif re.search(R"PRIVMSG(.+?):\>w (.+)", message):
			replies = function.webapi.weather.reply(weatherURL, re.search(R"PRIVMSG(.+?):\>w (.+)", message).group(2))
		elif re.search(R"PRIVMSG(.+?):\>f (.+)", message):
			replies = function.fenci.reply(re.search(R"PRIVMSG(.+?):\>f (.+)", message).group(2))
		elif re.search(R"privmsg(.+?):ping\!$", message.strip().lower()):
			replies = "Pong!"
		elif re.search(R"PRIVMSG(.+?):\>i (.+)", message):
			replies = function.webapi.ip.reply(ipURL, re.search(R"PRIVMSG(.+?):\>i (.+)", message).group(2).strip())
		elif re.search(R"JOIN", message.strip()):
			if re.search(R"PRIVMSG", message.strip()):
				pass
			elif re.match(r"^:([^!]+)", message).group(1) == botName:
				pass
			else:
				nickname = re.match(r"^:([^!]+)", message).group(1)
				print "<<< " + nickname
				origin_ip = re.search(R"^:([^ ]+)", message).group(1).split('@')[1]
				if re.search(R"((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){1,3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])", origin_ip):
					ip = re.search(R"((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){1,3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])", origin_ip).group(0)
					bot.Sock.send("PRIVMSG " + ircChan + " :" + nickname + " " + ip + " " + function.webapi.ip.reply(ipURL, ip) + "\r\n")
				elif re.search(R"\s*((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?\s", origin_ip):
					ip = re.search(R"\s*((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?\s", origin_ip).group(0)
					bot.Sock.send("PRIVMSG " + ircChan + " :" + nickname + " " + ip + " " + function.webapi.ip.reply(ipURL, ip) + "\r\n")
				elif re.search(R"([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}", origin_ip):
					ip = re.search(R"([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}", origin_ip).group(0)
					bot.Sock.send("PRIVMSG " + ircChan + " :" + nickname + " " + ip + " " + function.webapi.ip.reply(ipURL, ip) + "\r\n")

		if len(replies) > 0:
			nickname = re.match(r"^:([^!]+)", message).group(1)
			print "<<< " + nickname
			bot.replyMessage(replies, nickname, ircLeng)
