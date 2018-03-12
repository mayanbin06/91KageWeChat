#encoding=utf-8
import tornado.web

#local module
from wxauthorize import WxSignatureHandler
from login import LoginHandler

url_patterns = [
    (r'/wxsignature', WxSignatureHandler),
    (r'/login', LoginHandler), # 同下
    (r'/', LoginHandler), # 默认进入主页需要获取微信名
    (r'/(MP_verify.*)', tornado.web.StaticFileHandler, dict(path='static')),
   ]
