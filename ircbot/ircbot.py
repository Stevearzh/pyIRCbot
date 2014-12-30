#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import sys
reload(sys).setdefaultencoding("utf8")

import socket
import re
import time

import chat
import weather
import joke
import jokeuser
import helpcmd
#import story

irc_host = "irc.freenode.net"
irc_chan = "#linuxba"
bot_name = "bzzzt"
irc_port = 6666
irc_leng = 120

filter_map = [
    (chat,      lambda s: re.search(R"PRIVMSG(.+?):\>b (.+)", s).group(2)),
    (joke,      lambda s: re.search(R"PRIVMSG(.+?):\>j(.+)", s).group(2)),
    (jokeuser,  lambda s: re.search(R"PRIVMSG(.+?):\>u (.+)", s).group(2)),
    (weather,   lambda s: re.search(R"PRIVMSG(.+?):\>w (.+)", s).group(2)),
    (helpcmd,   lambda s: re.search(R"PRIVMSG(.+?):\>h(.+)", s).group(2)),
#    (story,     lambda s: re.search(R"PRIVMSG(.+?):\>s(.+)", s).group(2)),
]

# Creating socket 
irc_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connecting to the server
irc_sock.connect((irc_host, irc_port))

# Communicating with server
irc_sock.send("NICK " + bot_name + "\r\n")
irc_sock.send("USER bzt bzt bzt :bot\r\n")
irc_sock.send("JOIN " + irc_chan + "\r\n")

while True:
    data = irc_sock.makefile() ### what the fvck?

    for line in data:
        if line.lower().startswith("ping"): ### playing ping-pong
            send_back = line.lower().replace("ping", "pong")
            irc_sock.send(send_back)
            print "!!! playing PING-PONG"
            continue
        else:
            print line.strip()

        for (filter_mod, filter_fun) in filter_map: ### try matching with each filter
            try:
                nickname = re.match(r"^:([^!]+)", line).group(1)
                content = filter_fun(line)
                replies = filter_mod.reply(content)

                print "<<< " + nickname + ": " + content
                if len(replies) > irc_leng:
                    head = 0;
                    tail = irc_leng;
                    while (replies[tail]):
                        while(ord(replies[tail]) & 0xc0 != 0x80):
                            tail = tail + 1

                        irc_sock.send("PRIVMSG " + irc_chan + " :"  + "%s: %s\r\n" % (nickname, replies[head:tail]))
                        print ">>> " + replies[head:tail]
                        time.sleep(1)
                        head = tail
                        tail = tail + irc_leng
                        if tail > len(replies):
                            irc_sock.send("PRIVMSG " + irc_chan + " :"  + "%s: %s\r\n" % (nickname, replies[head:len(replies)]))
                            print ">>> " + replies[head:len(replies)]

                else:
                    for reply in replies.strip().split("\n"):
                        irc_sock.send("PRIVMSG " + irc_chan + " :"  + "%s: %s\r\n" % (nickname, reply))
                        print ">>> " + reply

            except Exception as e:
                pass

