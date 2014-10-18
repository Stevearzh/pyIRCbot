#!/usr/bin/env python2
#-*- encoding: utf-8 -*-

import sys
reload(sys).setdefaultencoding("utf8")

def reply(s):
    rets = """>b[空格]内容, 和我聊天; >j, 听我讲笑话; >u[空格]用户名, 恶搞用户; >s, 听我讲故事(该功能暂时关闭); >w[空格]城市, 天气预报; >h, 查看帮助。"""
    return rets.decode("utf8")