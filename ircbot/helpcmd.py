#!/usr/bin/env python2
#-*- encoding: utf-8 -*-

import sys
reload(sys).setdefaultencoding("utf8")

def reply(s):
    rets = str()
    rets += """ ============================================================\n"""
    rets += """  >b(空格)内容 和我聊天。\n"""
    rets += """  >j[(空格)用户名(可选)] 收听精选笑话 \n"""
    rets += """  >w(空格)[地名] 查询天气预报。\n"""
    rets += """  ?b      查看使用说明。\n"""
    rets += """ ============================================================\n"""
    return rets
