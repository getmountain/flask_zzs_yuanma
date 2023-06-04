import pymysql
from DBUtils.PooledDB import PooledDB

POOL = PooledDB(
    creator=pymysql,  # 使用链接数据库的模块
    maxconnections=6,  # 连接池允许的最大连接数，0和None表示不限制连接数
    mincached=2,  # 初始化时，链接池中至少创建的链接，0表示不创建
    blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
    ping=0, # ping MySQL服务端，检查是否服务可用。# 如：0 = None = never, 1 = default = whenever it is requested, 2 = when a cursor is created, 4 = when a query is executed, 7 = always

    host='127.0.0.1',
    port=3306,
    user='root',
    password='222',
    database='cmdb',
    charset='utf8'
)



def task(num):
    # 去连接池中获取一个连接
    conn = POOL.connection()
    cursor = conn.cursor()
    # cursor.execute('select * from web_models_disk')
    cursor.execute('select sleep(3)')
    result = cursor.fetchall()
    cursor.close()
    # 将连接放会到连接池
    conn.close()
    print(num,'------------>',result)


from threading import Thread
for i in range(57):
    t = Thread(target=task,args=(i,))
    t.start()