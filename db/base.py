#encoding=utf-8
import MySQLdb
import time
import sys

class MysqlBase:
    def __init__(self):
        self._conn()

    def _conn (self):
        try:
            self.conn = MySQLdb.connect(host='localhost', user='dabao', passwd='123456', charset="utf8")
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
