#encoding=utf-8

import sys
sys.path.append("..")

import tornado.web
import urllib2
import json

from base import BaseHandler
from wxapi import wx_oauth
from db.daos import userDao 

# tornado 异步的实例，后期要改成异步
#def MainHandler(tornado.web.RequestHandler):
#        @tornado.web.asynchronous
#        def get(self):
#            client = tornado.httpclient.AsyncHTTPClient()
#            def callback(response):
#                self.write("Hello World")
#                self.finish()
#            client.fetch("http://www.google.com/", callback)

#class SleepHandler(tornado.web.RequestHandler):
#    @tornado.web.asynchronous
#    @tornado.gen.coroutine
#    def get(self):
#        a = yield tornado.gen.Task(call_subprocess,self, "sleep 10")
#        print '111',a.read()
#        self.write("when i sleep 5s")

class LoginHandler(BaseHandler):
    AppId = 'wx21512b184ce97f79'
    AppSecret = '3dc1427af974bfe5b34b39408574038b'

    @tornado.web.asynchronous
    def get(self):

        if self.current_user:
            self.render('index.html')
            return

        # 无current_user, 此处暂时只有微信登录
        code = self.get_argument('code', default='0')
        if code == 0:
            self.write('err code 0')
            return

        '''是否每次都要获取用户信息'''
        ret = wx_oauth.GetUserInfo(code)
        if (ret['state'] != 0):
            self.write(str(ret))
	    return

   	userInfo = json.loads(ret['userinfo'])
	tokenInfo = json.loads(ret['token_data'])
        userId = userDao.QueryWeChat(userInfo['openid'])
        if not userId:
            # 没有用户绑定, 生成绑定用户, 此时应该把头像存到本地服务器, 目前先不做，暂时用微信的，如果失效再更新吧
            userId = userDao.GenerateUserByWeChat(userInfo, tokenInfo)

        self.set_secure_cookie(self.secure_username, userId, expires_days=None, expires=7200)
        self.render('main.html', user=userInfo['nickname'])

    def post(self):
        code = self.get_argument('code', default='0')
        self.write('post welcome .... ')
        # -----------------------------------
        # if success.
        self.set_secure_cookie(secure_cookie_name, expires_days=None, expires=7200)
        # else render 'denglu shibai'

class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie(self.secure_username)
        self.redirect("/")
