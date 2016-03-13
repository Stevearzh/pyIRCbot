pyIRCbot
========
Python 版 IRC 机器人，使用环境 Python 3.x。Python 2 版本请前往：https://github.com/Stevearzh/pyIRCbot/tree/py2


## wesync ##
连通微信群和 IRC 频道，基于 [Mojo-Weixin](https://github.com/sjdy521/Mojo-Weixin) 提供的 API 完成。


## 使用方法 ##
1. 参照 [Mojo-Weixin 的安装说明](https://github.com/sjdy521/Mojo-Weixin#安装方法) 安装 Mojo::Weixin 模块；

2. 在终端环境下运行 wechat.pl 并通过手机扫描二维码登录微信；

3. 运行 group.pl 查询所要连通的微信群 id；

4. 编辑 irc.py，将相应的 IRC 参数以及上一步获取的微信群 id 写入文件；

5. 运行 irc.py
