 #!/usr/bin/env python2
#-*- encoding: utf-8 -*-

import sys
reload(sys).setdefaultencoding("utf8")

import jieba

def reply(s):
	try:
		result = "/".join(jieba.cut(s.rstrip()))
		return result
	except:
		return "玩坏掉了。"