#!/usr/bin/env python2
#-*- encoding: utf-8 -*-

import sys
reload(sys).setdefaultencoding("utf8")

import socket
import re

import chat
import weather
import joke
import jokeuser
import helpcmd

irc_network = "irc.freenode.net"
irc_chan = "#linuxba"
bot_name = "bzzzt"
irc_port = 6666

filter_map = [
    (chat,      lambda s: re.search(R"PRIVMSG(.+?):\>b (.+)", s).group(2)),
    (joke,      lambda s: re.search(R"PRIVMSG(.+?):\>j(.+)", s).group(2)),   
    (jokeuser,  lambda s: re.search(R"PRIVMSG(.+?):\>j (.+)", s).group(2)),
    (weather,   lambda s: re.search(R"PRIVMSG(.+?):\>w (.+)", s).group(2)),
    (helpcmd,   lambda s: re.search(R"PRIVMSG(.+?):\?b(.+)", s).group(2)),
]

irc_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc_sock.connect( (irc_network, irc_port))

irc_sock.send("NICK " + bot_name + "\r\n")
irc_sock.send("USER bzt bzt bzt :bot\r\n")
irc_sock.send("JOIN " + irc_chan + "\r\n")

while True:
    data = irc_sock.recv(1048576) ### what the fvck?

    if data.lower().startswith("ping"): ### playing ping-pong
        data = data.lower().replace("ping", "pong")
        irc_sock.send(data)
        print "!!! playing PING-PONG"
        continue

    for (filter_mod, filter_fun) in filter_map: ### try matching with each filter
        try:
            nickname = re.search(R"^(.+?)!", data).group(1)
            content = filter_fun(data)
            replies = filter_mod.reply(content)

            print "<<< " + content
            for reply in replies.strip().split("\n"):
                irc_sock.send("PRIVMSG " + irc_chan + " %s: %s\r\n" % (nickname, reply))
                print ">>> " + reply
            break

        except Exception as e:
            pass

    else:
        print ":::" + data.strip()
