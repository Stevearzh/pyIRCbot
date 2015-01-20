#-*- encoding: utf-8 -*-

import function.jieba

def reply(string):
	try:
		result = "/".join(function.jieba.cut(string.rstrip()))
		return result
	except:
		return "玩坏掉了。"