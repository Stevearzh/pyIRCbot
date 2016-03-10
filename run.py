#!/usr/bin/env python3

import irc

irc_host = "irc.freenode.net"
irc_port = 8000
bot_name = "wesync"
bot_pass = ""
irc_chan = "#archlinux-cn"
we_id    = "@@495bc4dfd4d63863c2c0ba225a14195d11d3e7d34fea45b05c988c0602d4bfec"
we_send  = "http://127.0.0.1:3000/openwx/send_group_message?id=" + we_id + "&content="
we_recv  = ('127.0.0.1', 4000)   # address, port



bot = irc.irc_bot(irc_host, irc_port, bot_name, bot_pass, irc_chan, we_send, we_recv)
bot.start()
