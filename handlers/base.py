import tornado.web  

class BaseHandler(tornado.web.RequestHandler):
    secure_username = 'wxuserid'
    def get_current_user(self):
        return self.get_secure_cookie(self.secure_username)
