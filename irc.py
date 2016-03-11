#!/usr/bin/env python3

import json
import queue
import re
import socket
import threading
import time
import urllib.request

from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn


IRC_HOST   = "irc.freenode.net"
IRC_PORT   = 8000
BOT_NAME   = "wesync"
BOT_PASS   = ""
IRC_CHAN   = "#archlinux-cn"
GROUP_ID   = "@@5c26b71b5a4a41e7db9ad0ee536444acc875a247cfd96ceb5d68bfaf3a953bd1"
WE_SEND    = "http://127.0.0.1:3000/openwx/send_group_message?id=" + GROUP_ID + "&content="
WE_RECV    = ('127.0.0.1', 4000)   # address, port
MSG_QUEUE  = queue.Queue()


LENGTH_MAX = 120
TIME_LIMIT = 15


def reply_msg(queue, message, channel):
    times = 0
    
    if len(message) > LENGTH_MAX:
        for reply in message.strip().split("\n"):
            if times < TIME_LIMIT:
                if len(reply) > LENGTH_MAX:
                    head, tail = 0, LENGTH_MAX
                    while tail < len(replay):
                        while ord(reply[tail]) & 0xc0 != 0x80:
                            if tail + 1 < len(reply):
                                tail +=  1
                            else:
                                tail = head + LENGTH_MAX
                                break
                        queue.put(("PRIVMSG " + channel + " :"  + "reply[head:tail]" + "\r\n").encode())
                        print("<<< PRIVMSG " + channel + " :"  + "reply[head:tail]" + "\r\n")
                        times += 1
                        head = tail
                        tail = tail + LENGTH_MAX
                        if tail > len(reply):
                            queue.put(("PRIVMSG " + channel + " :"  + "reply[head:len(reply)]" + "\r\n").encode())
                            print("<<< PRIVMSG " + channel + " :"  + "reply[head:len(reply)]" + "\r\n")
                            times += 1
                else:
                    queue.put(("PRIVMSG " + channel + " :"  + "reply" + "\r\n").encode())
                    print("<<< PRIVMSG " + channel + " :"  + "reply" + "\r\n")
                    times += 1
    else:
        for reply in message.strip().split("\n"):
            if times < TIME_LIMIT:
                queue.put(("PRIVMSG " + channel + " :"  + "%s\r\n" % reply).encode())
                print("<<< PRIVMSG " + channel + " :"  + "%s\r\n" % reply)
                times += 1

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
            print(">>> " + self.string + "\n")
            send_back = self.string.replace("PING", "PONG").encode()
            self.queue.put(send_back)
            print("<<< " + send_back.decode().strip() + "\n")
            
class deal_irc_msg(threading.Thread):
    def __init__(self, bot, string):
        threading.Thread.__init__(self)
        self.bot    = bot
        self.string = string
    
    def start(self):
        if re.search(R"PRIVMSG(.+?):(.+)", self.string).group(2).strip():
            from_nick = re.match(R"^:([^!]+)", self.string).group(1)
            channel   = re.search(R"PRIVMSG(.+?):", self.string).group(1).strip() or self.bot.chan
            message   = re.search(R"PRIVMSG(.+?):(.+)", self.string).group(2).strip()
            replies   = "[" + from_nick + "] " + message
            
            if channel == self.bot.nick:
                channel = from_nick
            else:
                print(">>> " + from_nick + ": " + message + "\n")
                urllib.request.urlopen(self.bot.we_send + urllib.request.quote(replies.encode("utf8")))
        
class base_handler(BaseHTTPRequestHandler): 
    def do_GET(self):
        # Send response status code
        self.send_response(200)
     
        # Send headers
        self.send_header('Content-type','text/html')
        self.end_headers()
     
        # Send message back to client
        message = "This server is used for wesync!"
            
        # Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))
        return
           
    def do_POST(self):
        content_len = int(self.headers["Content-Length"])
        post_data   = self.rfile.read(content_len)
        result      = json.loads(post_data.decode("utf8"))
            
        try:
            if result["group_id"] == GROUP_ID:
                print("<<< " + result["sender"] + ": " + result["content"] + "\r\n")
                message = "[" + result["sender"] + "] " + result["content"]
                reply_msg(MSG_QUEUE, message, IRC_CHAN)
            
        except Exception as e:
            pass
            
class threaded_http_server(ThreadingMixIn, HTTPServer):
    pass

class irc_bot(threading.Thread):
    def __init__(self, host, port, nick, password, channel, we_send, we_recv):
        threading.Thread.__init__(self)
        self.host     = host
        self.port     = port
        self.nick     = nick
        self.password = password
        self.chan     = channel
        self.we_send  = we_send
        self.we_recv  = we_recv
        self.sock     = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def login(self):
        self.sock.connect((self.host, self.port))
        self.sock.send(("NICK " + self.nick + "\r\n").encode())
        self.sock.send(("PASS " + self.nick + ":" + self.password + "\r\n").encode())
        self.sock.send((("USER " + self.nick + " " + self.nick + " " + self.nick + " :" + self.nick + "\r\n").encode()))
        self.sock.send(("JOIN " + self.chan + "\r\n").encode())    

    def run(self):        
        cld_queue     = send_queue(MSG_QUEUE, self.sock)                
        listen_server = threaded_http_server(self.we_recv, base_handler)
        server_thread = threading.Thread(target = listen_server.serve_forever)
        
        cld_queue.daemon = True
        cld_queue.start()
        
        server_thread.daemon = True
        server_thread.start()

        self.login()                
        
        while True:
            try:                
                for line in self.sock.makefile():
                    (resp_ping(MSG_QUEUE, line)).start()
                    (deal_irc_msg(self, line)).start()
            except Exception as e:
                pass

(irc_bot(IRC_HOST, IRC_PORT, BOT_NAME, BOT_PASS, IRC_CHAN, WE_SEND, WE_RECV)).run()