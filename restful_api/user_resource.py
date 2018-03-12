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
    #@tornado.web.authenticated
    @get(_path="/api/user/json/{userId}", _types=[str], _produces=mediatypes.APPLICATION_JSON)
    def getUser(self, userId):
        # get 方法使用 authenticated会跳转登录页。这里我们自己判断, 参考 tornado web.py -- def authenticated(method):
        if not self.current_user:
            raise tornado.web.HTTPError(403)
        return {'userId':'123456', 'name':'3241'}
