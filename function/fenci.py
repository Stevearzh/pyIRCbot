#-*- encoding: utf-8 -*-

import sys
reload(sys).setdefaultencoding("utf8")

import jieba

def reply(string):
	try:
		result = "/".join(jieba.cut(string.rstrip()))
		return result
	except:
		return "玩坏掉了。"