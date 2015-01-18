#-*- encoding: utf-8 -*-

import sys
reload(sys).setdefaultencoding("utf8")

def reply(url, s):
    rets = """>b[空格]内容, 和我聊天; >j, 听我讲笑话; >u[空格]用户名, 恶搞用户; >s[空格]内容, 你懂的; >w[空格]城市, 天气预报; >m, 一言; >f[空格]内容, 结巴分词; ping!, Ping-Pong 测试; >i[空格]IP/网址, 查询归属地; >>>[空格]代码, 运行 Python3 代码; >h, 查看帮助。"""
    return rets.decode("utf8")