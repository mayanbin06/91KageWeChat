#encoding=utf-8
import tornado.web
import urllib2
import json
import base
import time

# local module
from wxapi import wx_oauth
from db import daos
from utils.log import logger

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

class LoginHandler(base.BaseHandler):
    expiresTime = 720
    #@tornado.web.asynchronous
    def get(self):

        #if self.current_user:
        #    self.redirect('index.html')
        #    return
        #else:
        #    print 'login ....'

        # 无current_user, 此处暂时只有微信登录
        code = self.get_argument('code', default=None)
        # 没有code，还未授权，跳转授权页
        if not code:
            url = self.request.protocol + '://' + self.request.host + self.request.uri
            redirect_url = wx_oauth.GetUserOauth(url, 'first-redirect')
            self.redirect(redirect_url)
            return

        if self.wx_login(code):
            self.redirect('index.html')
            logger.debug('登录成功，有效时间 ' + str(expires))
        else:
            self.redirect('error.html')
            logger.debug('登录失败')

    def wx_login(self, code):
	
        '''是否每次都要获取用户信息'''
        ret = wx_oauth.GetUserInfo(code)
        if (ret['state'] != 0):
            self.write(str(ret))
	    return False

   	userInfo = json.loads(ret['userinfo'])
	tokenInfo = json.loads(ret['token_data'])
        userId = daos.userDao.QueryWeChat(userInfo['openid'])
        if not userId:
            parentUserId = self.get_argument('userid', default=None)
            logger.debug('new user login, super user id %s' % parentUserId)
            # 没有用户绑定, 生成绑定用户, 此时应该把头像存到本地服务器, 目前先不做，暂时用微信的，如果失效再更新吧
            userId = daos.userDao.GenerateUserByWeChat(userInfo, tokenInfo, parentId=parentUserId)
        else:
            '''更新用户信息 .....'''
            logger.debug('update wechat info to user. %s' % str(userInfo))

        expires = int(time.time()) + self.expiresTime
        self.set_secure_cookie(self.secure_username, userId, expires_days=None, expires=expires)
        #self.set_secure_cookie(self.secure_username, userId)
        return True

class LogoutHandler(base.BaseHandler):
    def get(self):
        self.clear_cookie(self.secure_username)
        self.redirect("/")
