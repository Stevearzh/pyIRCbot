#-*- encoding: utf-8 -*-

import socket
import time
import re
import function
from function.webapi.ip import reIPv4
from function.webapi.ip import reIPv6
from function.webapi.ip import reURL


class ircBot:

	def __init__(self, host, port, nick, password, channel):
		self.Host = host
		self.Port = port
		self.Nick = nick
		self.Password = password
		self.Chan = channel
		self.Sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def createConnection(self):
		self.Sock.connect((self.Host, self.Port))
		self.Sock.send(("NICK " + self.Nick + "\r\n").encode())
		self.Sock.send(("PASS " + self.Nick + ":" + self.Password + "\r\n").encode())
		self.Sock.send(("USER " + self.Nick + " " + self.Nick + " " + self.Nick + " :" + self.Nick + "\r\n").encode())
		self.Sock.send(("JOIN " + self.Chan + "\r\n").encode())

	def receiveData(self):
		return self.Sock.makefile()

	def responsePingfromServer(self, message):
		if message.startswith("PING"):
			self.Sock.send(message.replace("PING", "PONG").encode())

	def replyMessage(self, fromnick, replies, channel = None, tonick = "", limit = 120):
		channel = channel or self.Chan
		if channel == self.Nick:
			channel = fromnick
		if len(replies) > limit:
			head = 0;
			tail = limit;
			times = 0
			while tail < len(replies):
				while ord(replies[tail]) & 0xc0 != 0x80:
					if tail + 1 < len(replies):
						tail = tail + 1
					else:
						tail = head + limit
						break
				for reply in replies[head:tail].strip().split("\n"):
					if times < 15:
						if tonick:
							self.Sock.send(("PRIVMSG " + channel + " :"  + "%s: %s\r\n" % (tonick, reply)).encode())
						else:
							self.Sock.send(("PRIVMSG " + channel + " :"  + "%s\r\n" % reply).encode())
						time.sleep(1)
						print(">>> " + reply)
						times += 1
					else:
						self.Sock.send(("PRIVMSG " + channel + " :"  + "%s\r\n" % "....").encode())
						break
				head = tail
				tail = tail + limit
				if tail > len(replies):
					for reply in replies[head:len(replies)].strip().split("\n"):
						if tonick:
							self.Sock.send(("PRIVMSG " + channel + " :"  + "%s: %s\r\n" % (tonick, reply)).encode())
						else:
							self.Sock.send(("PRIVMSG " + channel + " :"  + "%s\r\n" % reply).encode())
						time.sleep(1)
						print(">>> " + reply)
		else:
			for reply in replies.strip().split("\n"):
				if tonick:
					self.Sock.send(("PRIVMSG " + channel + " :"  + "%s: %s\r\n" % (tonick, reply)).encode())
				else:
					self.Sock.send(("PRIVMSG " + channel + " :"  + "%s\r\n" % reply).encode())
				time.sleep(1)
				print(">>> " + reply)

	def searchUserLocation(self, message, check_the_water_meter = ""):
		if re.search(R"JOIN", message.strip()):
			if re.search(R"PRIVMSG", message.strip()):
				pass
			elif re.match(R"^:([^!]+)", message).group(1) == self.Nick:
				pass
			else:
				tonick = re.match(R"^:([^!]+)", message).group(1)
				origin_ip = re.search(R"^:([^ ]+)", message).group(1).split('@')[1]
				if re.search(reIPv4, origin_ip):
					print("<<< " + tonick)
					ip = re.search(reIPv4, origin_ip).group(0)
					if check_the_water_meter:
						check_the_water_meter(lambda nick, ip: self.replyMessage("", tonick + " " + ip + " " + function.webapi.ip.reply(ip)), tonick, ip)
					else:
						self.replyMessage("", tonick + " " + ip + " " + function.webapi.ip.reply(ip))
				elif re.search(reIPv6, origin_ip):
					print("<<< " + tonick)
					ip = re.search(reIPv6, origin_ip).group(0)
					if check_the_water_meter:
						check_the_water_meter(lambda nick, ip: self.replyMessage("", tonick + " " + ip + " " + function.webapi.ip.reply(ip)), tonick, ip)
					else:
						self.replyMessage("", tonick + " " + ip + " " + function.webapi.ip.reply(ip))
				elif re.search(reURL, origin_ip):
					print("<<< " + tonick)
					ip = re.search(reURL, origin_ip).group(0)
					if check_the_water_meter:
						check_the_water_meter(lambda nick, ip: self.replyMessage("", tonick + " " + ip + " " + function.webapi.ip.reply(ip)), tonick, ip)
					else:
						self.replyMessage("", tonick + " " + ip + " " + function.webapi.ip.reply(ip))


class ip_once(object):

	class helper(object):
		def __init__(self):
			self.prev_hour = time.localtime().tm_hour
			self.ip_info_set = set()

		def __call__(self, cur_hour, fn, pr):
			if self.prev_hour != cur_hour:
				self.ip_info_set.clear()
				self.prev_hour = cur_hour

			if pr not in self.ip_info_set:
				fn(*pr)
				self.ip_info_set.add(pr)

	def __init__(self):
		self.aux = self.helper()

	def __call__(self, fn, nick, ip):
		self.aux(time.localtime().tm_mday, fn, (nick, ip))
