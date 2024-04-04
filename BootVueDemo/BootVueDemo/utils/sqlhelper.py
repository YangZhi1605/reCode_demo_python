import pymysql
from DBUtils.PooledDB import PooledDB
from threading import Thread

# 创建数据库连接池
POOL = PooledDB(
    creator=pymysql,  # 使用链接数据库的模块
    maxconnections=6,  # 连接池允许的最大连接数，0和None表示不限制连接数。注意这里说的是允许最大连接数，而不是当前连接数。 # 6个线程
    mincached=2,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
    blocking=True,# 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
    #了解一个ping参数
    ping=0,# ping MySQL服务端，检查是否服务可用。
    host='127.0.0.1',
    port=3306,
    user='root',
    password='123456',
    database='bootvue',
    charset='utf8'
)


def def_fetchall(sql,*args):
    '''
    获取所有数据
    :return: result
    '''
    # 去数据库中获取一个链接
    conn = POOL.connection()
    # 创建游标对象，帮助执行SQL语句
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    # 执行sql语句
    cursor.execute(sql,args)
    # 获取执行数据
    reslut = cursor.fetchall()
    # 关闭游标对象
    cursor.close()
    # 关闭链接 —— 实际是将链接放回到连接池中
    conn.close()
    # 返回结果
    return reslut

def def_fetchone(sql,*args):
    '''
    获取单条数据
    :return:
    '''
    # 去数据库中获取一个链接
    conn = POOL.connection()
    # 创建游标对象，帮助执行SQL语句
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    # 执行sql语句
    cursor.execute(sql, args)
    # 获取执行的单条数据
    reslut = cursor.fetchone()
    # 关闭游标对象
    cursor.close()
    # 关闭链接 —— 实际是将链接放回到连接池中
    conn.close()
    # 返回结果
    return reslut