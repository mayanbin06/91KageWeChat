#encoding=utf-8
import uuid
import time
import base
import MySQLdb

# local module
from common.common import logger

'''保持一个连接?，应该改为连接池'''
class UserDao(base.MysqlBase):
    UserTableName = 'User'
    WeChatTableName = 'WeChat'
    FieldOpenId = 'OpenId'
    def InsertUser(self, user):
        try:
            self._reConn()
            cursor = self.conn.cursor()
            qmarks = ', '.join(['%s'] * len(user)) # 用于替换记录值
            cols = ', '.join(user.keys()) # 字段名
            sql = "INSERT INTO %s (%s) VALUES (%s)" % (self.UserTableName, cols, qmarks)
            cursor.execute(sql, user.values())
            self.conn.commit()
            cursor.close()
            return True
        except Exception, e:
            logger.error("%s SQL error: %s" % (__file__, str(e)))
            return False

    def GenerateUserByWeChat(self, userInfo, tokenInfo):

        userId = str(uuid.uuid1())
        user = {'UserId': userId, 'UserName':userInfo['nickname'], 'UserSex':userInfo['sex'], 'UserArea':userInfo['city'], 'UserPosterUrl': userInfo['headimgurl']}

        if self.InsertUser(user):
            t = int(time.time()) + tokenInfo['expires_in']
            data = {'UserId': userId, 'OpenId': tokenInfo['openid'], 'AccessToken': tokenInfo['access_token'], 'RefreshToken': tokenInfo['refresh_token'], 'Scope': tokenInfo['scope'], 'ExpiresIn':t}
            if self.InsertWeChat(data):
                return userId
        return None

    def QueryWeChat(self, openId):
        try:
            self._reConn()
            cursor = self.conn.cursor(MySQLdb.cursors.DictCursor)
            sql = "select * from %s where %s = '%s'" % (self.WeChatTableName, self.FieldOpenId, openId)
            cursor.execute(sql)
            ret = cursor.fetchall()
            cursor.close()
            if len(ret) > 0:
                return ret[0]['UserId']
            return None 
        except Exception, e:
            logger.error("%s SQL error: %s" % (__file__, str(e)))
            return None 

    def InsertWeChat(self, data):
        try:
            self._reConn()
            cursor = self.conn.cursor()
            qmarks = ', '.join(['%s'] * len(data)) # 用于替换记录值
            cols = ', '.join(data.keys()) # 字段名
            sql = "INSERT INTO %s (%s) VALUES (%s)" % (self.WeChatTableName, cols, qmarks)
            cursor.execute(sql, data.values())
            self.conn.commit()
            cursor.close()
            return True
        except Exception, e:
            logger.error("%s SQL error: %s" % (__file__, str(e)))
            return False

    def QueryUser(self, userid):
        return

    def UpdateUser(self, user):
        return

    def DeleteUser(self, user):
        return
