#coding=utf-8
import MySQLdb
import time
import sys

AgentInfoTable = 'AgentInfo'

# 数据后期要做成自动生成的，数据表等等
class DBHelper:
    def __init__(self):
        self._conn()

    def _conn (self):
        try:
            self.conn = MySQLdb.connect(host='localhost', user='dabao', passwd='123456')
            self.conn.select_db('91Kage')
            self.conn.set_character_set('utf8')
            return True
        except Exception, e:
            print e
            return False

    def _reConn (self,num = 28800,stime = 3):
        _number = 0
        _status = True
        while _status and _number <= num:
            try:
                self.conn.ping()
                _status = False
            except Exception, e:
                if self._conn()==True:
                    _status = False
                    break
                _number +=1
                time.sleep(stime)
                print e

    def __del__(self):
        self.conn.close()

    def QueryAgent(self, data, page, limit):
        try:
            self._reConn()
            cursor = self.conn.cursor(MySQLdb.cursors.DictCursor)

            where = ""
            for key in data:
                if data[key] != "":
                    where += " and %s = '%s' " % (key, str(data[key]))

            sql = "select * from %s where 1=1 " % AgentInfoTable + where
            # 分页逻辑
            p = int(page) - 1
            l = int(limit)
            s = p * l
            sql += ' limit %s,%s' % (s,l)
            cursor.execute(sql)
            ret = cursor.fetchall()
            result = []
            for r in ret:
                result.append(r) 

            # 查询总记录数
            sql = "select count(*) as total from %s where 1=1 " % AgentInfoTable + where
            cursor.execute(sql)
            ret = cursor.fetchone()
            count = ret['total']

            cursor.close()
            return {'count':count, 'data':result, 'msg': 'success', 'code':0}
            return json.dumps(result, ensure_ascii=False, encoding='UTF-8')
        except Exception, e:
            print 'Query user exception ' + str(e)
            return {'count':0, 'data':[], 'msg': str(e), 'code':1 }
    def AddAgent(self, data):
        try:
            self._reConn()
            cursor = self.conn.cursor()
            qmarks = ', '.join(['%s'] * len(data)) # 用于替换记录值
            cols = ', '.join(data.keys()) # 字段名
            sql = "INSERT INTO %s (%s) VALUES (%s)" % (AgentInfoTable, cols, qmarks)
            cursor.execute(sql, data.values())
            self.conn.commit()
            cursor.close()
            return True
        except Exception, e:
            print e
            print "SQL error:", sys.exc_info()[0]
            return False
    def RemoveUser(self, user, auth):
        try:
            self._reConn()
            cursor = self.conn.cursor()
            if auth:
                sql = "delete from auth_users where name = '%s'"% user
            else:
                sql = "delete from un_auth_users where name = '%s'"% user
            cursor.execute(sql)
            self.conn.commit()
            cursor.close()
            print 'remove user success ' + user
            return True
        except Exception, e:
            print 'remove user exception ' + str(e)
            return False

if __name__ == "__main__":
    print 'start ....'
