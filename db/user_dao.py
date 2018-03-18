#encoding=utf-8
import uuid
import time
import base
import MySQLdb

'''保持一个连接?，应该改为连接池'''
class UserDao(base.MysqlBase):
    UserTableName = 'User'
    WeChatTableName = 'WeChat'
    FieldOpenId = 'OpenId'
    FieldUserId = 'UserId'
    FieldParentId = 'ParentId'
    FieldGrandParentId = 'GrandParentId'
    FieldGreatGrandParentId = 'GreatGrandParentId'

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
            if self.logger:
                self.logger.error("%s SQL error: %s" % (__file__, str(e)))
            return False

    def GetParentUser(self, userId):
        if userId == None or userId == '':
            return None
        parentUser = self.QueryUser(userId)
        return parentUser

    def GenerateUserByWeChat(self, userInfo, tokenInfo, parentId=None):

        userId = str(uuid.uuid1())
        user = {'UserId': userId, 'UserName':userInfo['nickname'], 'UserSex':userInfo['sex'], 'UserArea':userInfo['city'], 'UserPosterUrl': userInfo['headimgurl']}

        parentUser = self.GetParentUser(parentId)
        # 有上级用户
        if parentUser:
            user[self.FieldParentId] = parentUser[self.FieldUserId]
            user[self.FieldGrandParentId] = parentUser[self.FieldParentId]
            user[self.FieldGreatGrandParentId] = parentUser[self.FieldGrandParentId]

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
            if self.logger:
                self.logger.error("%s SQL error: %s" % (__file__, str(e)))
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
            if self.logger:
                self.logger.error("%s SQL error: %s" % (__file__, str(e)))
            return False

    def QueryUser(self, userId):
        try:
            self._reConn()
            cursor = self.conn.cursor(MySQLdb.cursors.DictCursor)
            sql = "select * from %s where %s = '%s'" % (self.UserTableName, self.FieldUserId, userId)
            cursor.execute(sql)
            ret = cursor.fetchall()
            cursor.close()
            if len(ret) > 0:
                return ret[0]
            return None
        except Exception, e:
            if self.logger:
                self.logger.error("%s SQL error: %s" % (__file__, str(e)))
            return None

    def UpdateUser(self, user):
        return

    def DeleteUser(self, user):
        return

if __name__ == '__main__':
    # 测试用例
    tokenInfo = {
        "access_token":"ACCESS_TOKEN",
        "expires_in":7200,
        "refresh_token":"REFRESH_TOKEN",
        "openid":"OPENID-1",
        "scope":"SCOPE"
    }
    userInfo = {
        "openid": "OPENID-1",
        "nickname": 'hhh',
        "sex": "1",
        "province": "PROVINCE",
        "city": "CITY",
        "country": "COUNTRY",
        "headimgurl": "",
        "privilege": [ "PRIVILEGE1" "PRIVILEGE2" ],
        "unionid": "o6_bmasdasdsad6_2sgVt7hMZOPfL"
    }

    userDao = UserDao()
    # 添加用户 Openid-1
    uid1 = userDao.GenerateUserByWeChat(userInfo, tokenInfo)

    # 添加用户 Openid-2
    userInfo['openid'] = 'OPENID-2'
    tokenInfo['openid'] = 'OPENID-2'
    uid2 = userDao.GenerateUserByWeChat(userInfo, tokenInfo, parentId=uid1)

    # 添加用户 Openid-3
    userInfo['openid'] = 'OPENID-3'
    tokenInfo['openid'] = 'OPENID-3'
    uid3 = userDao.GenerateUserByWeChat(userInfo, tokenInfo, parentId=uid1)

    # 添加用户 Openid-4
    userInfo['openid'] = 'OPENID-4'
    tokenInfo['openid'] = 'OPENID-4'
    uid4 = userDao.GenerateUserByWeChat(userInfo, tokenInfo, parentId = uid3)

    # 添加用户 Openid-5
    userInfo['openid'] = 'OPENID-5'
    tokenInfo['openid'] = 'OPENID-5'
    uid5 = userDao.GenerateUserByWeChat(userInfo, tokenInfo, parentId = uid2)

    # 添加用户 Openid-6
    userInfo['openid'] = 'OPENID-6'
    tokenInfo['openid'] = 'OPENID-6'
    uid6 = userDao.GenerateUserByWeChat(userInfo, tokenInfo, parentId = uid4)

    # 添加用户 Openid-7
    userInfo['openid'] = 'OPENID-7'
    tokenInfo['openid'] = 'OPENID-7'
    uid7 = userDao.GenerateUserByWeChat(userInfo, tokenInfo, parentId = uid6)
