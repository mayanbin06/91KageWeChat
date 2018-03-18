#encoding=utf-8
import tornado.web
import urllib2
import json

# local module
from db import daos

from restful import mediatypes
from restful.rest import get, post, put, delete
from restful.rest import RestHandler

#GET     # Read  
#POST    # Create  
#PUT     # Update  
#DELETE  # Delete

# /api/user/json/{userid}, default is current user

class UserResource(RestHandler):
    # get 方法使用 authenticated会跳转登录页。这里我们自己判断.
    # 参考 tornado web.py -- def authenticated(method):
    #@tornado.web.authenticated
    @get(_path="/api/user/json/other/{userId}", _types=[str], _produces=mediatypes.APPLICATION_JSON)
    def GetUser(self, userId):
        if not self.current_user:
            ret = {'code': 2, 'msg': 'permision denied', 'data': ''}
            return ret
        return {'userId':'123456', 'name':'3241'}

    @get(_path="/api/user/json/current", _produces=mediatypes.APPLICATION_JSON)
    def GetCurrentUser(self):
        userId = self.current_user
        if not userId:
            ret = {'code': 2, 'msg': 'permision denied', 'data': ''}
            return ret
        user = daos.userDao.QueryUser(userId)
        if not user:
            ret = {'code': 1, 'msg': 'no user', 'data': ''}
        else:
            ret = {'code': 0, 'msg': '', 'data': user}
        return ret
