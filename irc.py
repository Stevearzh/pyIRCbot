import queue
import re
import socket
import threading
import time
import urllib.request

LENGTH_MAX = 120
TIME_LIMIT = 15


class send_queue(threading.Thread):
    def __init__(self, queue, sock):
        threading.Thread.__init__(self)
        self.queue = queue
        self.sock  = sock

    def run(self):
        while True:
            msg = self.queue.get()
            self.sock.send(msg)
            time.sleep(1)
            self.queue.task_done()

class resp_ping(threading.Thread):
    def __init__(self, queue, string):
        threading.Thread.__init__(self)
        self.queue = queue
        self.string = string

    def run(self):
        if self.string.startswith("PING"):
            send_back = self.string.replace("PING", "PONG").encode()
            self.queue.put(send_back)
            print("<<< " + send_back.decode().strip() + "\n")
            
class deal_irc_msg(threading.Thread):
    def __init__(self, queue, bot, string):
        threading.Thread.__init__(self)
        self.queue  = queue
        self.bot    = bot
        self.string = string
    
    def start(self):
        if re.search(R"PRIVMSG(.+?):(.+)", self.string).group(2).strip():
            from_nick = re.match(R"^:([^!]+)", self.string).group(1)
            channel   = re.search(R"PRIVMSG(.+?):", self.string).group(1).strip() or self.bot.chan
            message   = re.search(R"PRIVMSG(.+?):(.+)", self.string).group(2).strip()
            replies   = "[" + from_nick + "]" + message
            
            if channel == self.bot.nick:
                channel = from_nick
            else:
                urllib.request.urlopen(self.bot.we_send + urllib.request.quote(replies.encode("utf8")))

class irc_bot(threading.Thread):
    def __init__(self, host, port, nick, password, channel, we_send):
        threading.Thread.__init__(self)
        self.host     = host
        self.port     = port
        self.nick     = nick
        self.password = password
        self.chan     = channel
        self.we_send  = we_send
        self.sock     = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self):
        self.sock.connect((self.host, self.port))
        self.sock.send(("NICK " + self.nick + "\r\n").encode())
        self.sock.send(("PASS " + self.nick + ":" + self.password + "\r\n").encode())
        self.sock.send((("USER " + self.nick + " " + self.nick + " " + self.nick + " :" + self.nick + "\r\n").encode()))
        self.sock.send(("JOIN " + self.chan + "\r\n").encode())

        msg_queue = queue.Queue()
        cld_queue = send_queue(msg_queue, self.sock)
        cld_queue.daemon = True
        cld_queue.start()

        while True:
            try:
                for line in self.sock.makefile():
                    print(line)
                    (resp_ping(msg_queue, line)).start()
                    (deal_irc_msg(msg_queue, self, line)).start()
            except Exception as e:
                pass
