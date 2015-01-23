import queue
import re
import socket
import threading
import time

import function
import helpcmd

from function.webapi.ip import reIPv4
from function.webapi.ip import reIPv6
from function.webapi.ip import reURL

lengthLimit = 120
timesLimit = 15

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

def replyMessage(Queue, bot, fromnick, replies, channel = None, tonick = ""):
	channel = channel or bot.Chan
	if channel == bot.Nick:
		channel = fromnick
	times = 0
	if len(replies) > lengthLimit:
		for reply in replies.strip().split("\n"):
			if times < timesLimit:
				if len(reply) > lengthLimit:
					head = 0
					tail = lengthLimit
					while tail < len(reply):
						while ord(reply[tail]) & 0xc0 != 0x80:
							if tail + 1 < len(reply):
								tail +=  1
							else:
								tail = head + lengthLimit
								break
						if tonick:
							Queue.put(("PRIVMSG " + channel + " :"  + "%s: %s\r\n" % (tonick, reply[head:tail])).encode())
						else:
							Queue.put(("PRIVMSG " + channel + " :"  + "%s\r\n" % reply[head:tail]).encode())
						print("<<< " + reply[head:tail]  + "\n")
						times += 1
						head = tail
						tail = tail + lengthLimit
						if tail > len(reply):
							if tonick:
								Queue.put(("PRIVMSG " + channel + " :"  + "%s: %s\r\n" % (tonick, reply[head:len(reply)])).encode())
							else:
								Queue.put(("PRIVMSG " + channel + " :"  + "%s\r\n" % reply[head:len(reply)]).encode())
							print("<<< " + reply[head:len(reply)] + "\n")
							times += 1
				else:
					if tonick:
						Queue.put(("PRIVMSG " + channel + " :"  + "%s: %s\r\n" % (tonick, reply)).encode())
					else:
						Queue.put(("PRIVMSG " + channel + " :"  + "%s\r\n" % reply).encode())
					print("<<< " + reply  + "\n")
					times += 1

	else:
		for reply in replies.strip().split("\n"):
			if times < timesLimit:
				if tonick:
					Queue.put(("PRIVMSG " + channel + " :"  + "%s: %s\r\n" % (tonick, reply)).encode())
				else:
					Queue.put(("PRIVMSG " + channel + " :"  + "%s\r\n" % reply).encode())
				print("<<< " + reply  + "\n")
				times += 1


def searchUserLocation(bot, Queue, message, check_the_water_meter = ""):
	if re.search(R"JOIN", message.strip()):
		if re.search(R"PRIVMSG", message.strip()):
			pass
		elif re.match(R"^:([^!]+)", message).group(1) == bot.Nick:
			pass
		else:
			tonick = re.match(R"^:([^!]+)", message).group(1)
			origin_ip = re.search(R"^:([^ ]+)", message).group(1).split('@')[1]
			if re.search(reIPv4, origin_ip):
				print(">>> " + tonick)
				ip = re.search(reIPv4, origin_ip).group(0)
				if check_the_water_meter:
					check_the_water_meter(lambda nick, ip: replyMessage(Queue, bot, "", tonick + " " + ip + " " + function.webapi.ip.reply(ip)), tonick, ip)
				else:
					replyMessage(Queue, bot, "", tonick + " " + ip + " " + function.webapi.ip.reply(ip))
			elif re.search(reIPv6, origin_ip):
				print(">>> " + tonick)
				ip = re.search(reIPv6, origin_ip).group(0)
				if check_the_water_meter:
					check_the_water_meter(lambda nick, ip: replyMessage(Queue, bot, "", tonick + " " + ip + " " + function.webapi.ip.reply(ip)), tonick, ip)
				else:
					replyMessage(Queue, bot, "", tonick + " " + ip + " " + function.webapi.ip.reply(ip))
			elif re.search(reURL, origin_ip):
				print(">>> " + tonick)
				ip = re.search(reURL, origin_ip).group(0)
				if check_the_water_meter:
					check_the_water_meter(lambda nick, ip: replyMessage(Queue, bot, "", tonick + " " + ip + " " + function.webapi.ip.reply(ip)), tonick, ip)
				else:
					replyMessage(Queue, bot, "", tonick + " " + ip + " " + function.webapi.ip.reply(ip))


class filterFun(threading.Thread):
	def __init__(self, Queue, bot, string):
		threading.Thread.__init__(self)
		self.Queue = Queue
		self.Bot = bot
		self.String = string
		self.Map = [
			(helpcmd,                   lambda string: re.search(R"PRIVMSG(.+?):\>h$", string.strip()).group(0)),
			(function.webapi.chat,      lambda string: re.search(R"PRIVMSG(.+?):\>b (.+)", string).group(2).strip()),
			(function.webapi.joke,      lambda string: re.search(R"PRIVMSG(.+?):\>j$", string.strip()).group(0)),
			(function.webapi.maxim,     lambda string: re.search(R"PRIVMSG(.+?):\>m$", string.strip()).group(0)),
			(function.webapi.sm,        lambda string: re.search(R"PRIVMSG(.+?):\>s (.+)", string).group(2).strip()),
			(function.webapi.trick,     lambda string: re.search(R"PRIVMSG(.+?):\>u (.+)", string).group(2).strip()),
			(function.webapi.weather,   lambda string: re.search(R"PRIVMSG(.+?):\>w (.+)", string).group(2).strip()),
			(function.fenci,            lambda string: re.search(R"PRIVMSG(.+?):\>f (.+)", string).group(2).strip()),
			(function.webapi.ping,      lambda string: re.search(R"privmsg(.+?):ping\!$", string.strip().lower()).group(0)),
			(function.webapi.ip,        lambda string: re.search(R"PRIVMSG(.+?):\>i (.+)", string).group(2).strip())
		]
		self.Map2 = [
			(function.webapi.py3exec,   lambda string: re.search(R"PRIVMSG(.+?):\>\>\> (.+)", string).group(2).strip())
		]

	def run(self):
		for (filterMod, filterFun) in self.Map:
			try:
				if filterFun(self.String):
					fromnick = re.match(R"^:([^!]+)", self.String).group(1)
					channel = re.search(R"PRIVMSG(.+?):", self.String).group(1).strip()
					content = filterFun(self.String)
					replies = filterMod.reply(content)
					print(">>> " + fromnick + ": " + content + "\n")
					replyMessage(self.Queue, self.Bot, fromnick, replies, channel, fromnick)
			except Exception as e:
				pass
		for (filterMod, filterFun) in self.Map2:
			try:
				if filterFun(self.String):
					fromnick = re.match(r"^:([^!]+)", self.String).group(1)
					channel = re.search(R"PRIVMSG(.+?):", self.String).group(1).strip()
					content = filterFun(self.String)
					replies = filterMod.reply(content)
					print(">>> " + fromnick + ": " + content + "\n")
					replyMessage(self.Queue, self.Bot, fromnick, replies, channel)
			except Exception as e:
				pass


class sendQueue(threading.Thread):
	def __init__(self, Queue, Sock):
		threading.Thread.__init__(self)
		self.Queue = Queue
		self.Sock = Sock

	def run(self):
		while True:
			message = self.Queue.get()
			self.Sock.send(message)
			time.sleep(0.8)
			self.Queue.task_done()


class responsePing(threading.Thread):
	def __init__(self, Queue, string):
		threading.Thread.__init__(self)
		self.Queue = Queue
		self.String = string

	def run(self):
		if self.String.startswith("PING"):
			sendBack = self.String.replace("PING", "PONG").encode()
			self.Queue.put(sendBack)
			print("<<< " + sendBack.decode().strip() + "\n")


class ircBot(threading.Thread):

	def __init__(self, host, port, nick, password, channel):
		threading.Thread.__init__(self)
		self.Host = host
		self.Port = port
		self.Nick = nick
		self.Password = password
		self.Chan = channel
		self.Sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def run(self):

		self.Sock.connect((self.Host, self.Port))
		self.Sock.send(("NICK " + self.Nick + "\r\n").encode())
		self.Sock.send(("PASS " + self.Nick + ":" + self.Password + "\r\n").encode())
		self.Sock.send(("USER " + self.Nick + " " + self.Nick + " " + self.Nick + " :" + self.Nick + "\r\n").encode())
		self.Sock.send(("JOIN " + self.Chan + "\r\n").encode())

		messageQueue = queue.Queue()
		chileQueue = sendQueue(messageQueue, self.Sock)
		chileQueue.daemon = True
		chileQueue.start()

		check_the_water_meter = ip_once()

		while True:
			try:
				for line in self.Sock.makefile():
					print(line)
					childPing = responsePing(messageQueue, line)
					childPing.start()
					childSearh = threading.Thread(target = searchUserLocation, args = (self, messageQueue, line, check_the_water_meter))
					childSearh.start()
					childMatch = filterFun(messageQueue, self, line)
					childMatch.start()
			except Exception as e:
				pass
