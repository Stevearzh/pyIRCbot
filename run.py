#!/usr/bin/env python3

import irc

irc_host = "irc.freenode.net"
irc_port = 8000
bot_name = "wesync"
bot_pass = ""
irc_chan = "#archlinux-cn"
we_id    = "@@295a3f310a4d15b5bc964fea1b33e1e13e2aa7797f2b31a4dca5fdeb7e1428c1"
we_send  = "http://127.0.0.1:3000/openwx/send_group_message?id=" + we_id + "&content="


bot = irc.irc_bot(irc_host, irc_port, bot_name, bot_pass, irc_chan, we_send)
bot.start()
