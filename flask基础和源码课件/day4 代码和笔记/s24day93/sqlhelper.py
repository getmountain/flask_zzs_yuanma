import pymysql
import threading
from DBUtils.PooledDB import PooledDB

"""
storage = {
    1111:{'stack':[]}
}
"""

class SqlHelper(object):
    def __init__(self):
        self.pool = PooledDB(
            creator=pymysql,  # 使用链接数据库的模块
            maxconnections=6,  # 连接池允许的最大连接数，0和None表示不限制连接数
            mincached=2,  # 初始化时，链接池中至少创建的链接，0表示不创建
            blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
            ping=0,
            # ping MySQL服务端，检查是否服务可用。# 如：0 = None = never, 1 = default = whenever it is requested, 2 = when a cursor is created, 4 = when a query is executed, 7 = always
            host='127.0.0.1',
            port=3306,
            user='root',
            password='222',
            database='cmdb',
            charset='utf8'
        )
        self.local = threading.local()

    def open(self):
        conn = self.pool.connection()
        cursor = conn.cursor()
        return conn, cursor

    def close(self, cursor, conn):
        cursor.close()
        conn.close()

    def fetchall(self, sql, *args):
        """ 获取所有数据 """
        conn, cursor = self.open()
        cursor.execute(sql, args)
        result = cursor.fetchall()
        self.close(conn, cursor)
        return result

    def fetchone(self, sql, *args):
        """ 获取所有数据 """
        conn, cursor = self.open()
        cursor.execute(sql, args)
        result = cursor.fetchone()
        self.close(conn, cursor)
        return result

    def __enter__(self):
        conn,cursor = self.open()
        rv = getattr(self.local,'stack',None)
        if not rv:
            self.local.stack = [(conn,cursor),]
        else:
            rv.append((conn,cursor))
            self.local.stack = rv
        return cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        rv = getattr(self.local,'stack',None)
        if not rv:
            # del self.local.stack
            return
        conn,cursor = self.local.stack.pop()
        cursor.close()
        conn.close()

db = SqlHelper()



