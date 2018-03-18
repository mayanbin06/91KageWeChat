#encoding=utf-8
import tornado.web

#local module
from login import LoginHandler

url_patterns = [
    (r'/login', LoginHandler), # 同下
    (r'/', LoginHandler), # 默认进入主页需要获取微信名
   ]
