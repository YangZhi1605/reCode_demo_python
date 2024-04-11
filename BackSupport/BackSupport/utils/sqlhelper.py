from DBUtils.PooledDB import PooledDB
# 这个错误是因为你试图调用一个模块，而不是模块中的一个类或者函数。在你的代码中，你试图调用 PooledDB，但是 PooledDB 是一个模块，而不是一个可调用的对象。
import pymysql

class SqlHelper(object):
    # 编写初始化函数
    def __init__(self):
        # 构建数据库连接池
        self.__pool = PooledDB(
            creator=pymysql,  # 使用链接数据库的模块
            maxconnections=6,  # 连接池允许的最大连接数，0和None表示不限制连接数。注意这里说的是允许最大连接数，而不是当前连接数。 # 6个线程
            mincached=2,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
            blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
            # 了解一个ping参数
            ping=0,  # ping MySQL服务端，检查是否服务可用。
            host='127.0.0.1',
            port=3306,
            user='root',
            password='123456',
            database='graduate',
            charset='utf8'
        )

    # 编写实现链接的函数
    def open(self):
        # 获取链接
        conn = self.__pool.connection()
        # 创建游标对象
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        return conn, cursor

    # 编写关闭链接的函数
    def close(self,conn,cursor):
        # 关闭游标对象
        cursor.close()
        # 关闭链接
        conn.close()

    # 编写获取所有数据的函数
    def def_fetchall(self,sql,*args):
        conn, cursor = self.open()
        # 执行sql语句
        cursor.execute(sql,args)
        # 获取执行数据
        reslut = cursor.fetchall()
        self.close(conn,cursor)
        # 返回结果
        return reslut

    # 编写获取单条数据的函数
    def def_fetchone(self,sql,*args):
        conn, cursor = self.open()
        # 执行sql语句
        cursor.execute(sql,args)
        # 获取执行数据
        reslut = cursor.fetchone()
        self.close(conn,cursor)
        # 返回结果
        return reslut

    # 编写删除信息的函数
    def def_delete(self,sql,*args):
        conn, cursor = self.open()
        # 执行sql语句
        cursor.execute(sql,args)
        # 提交
        conn.commit()
        self.close(conn,cursor)

    # 编写添加信息的函数
    def def_insert(self,sql,*args):
        conn, cursor = self.open()
        # 执行sql语句
        cursor.execute(sql,args)
        # 提交
        conn.commit()
        self.close(conn,cursor)

    # 更新信息的函数
    def def_update(self,sql,*args):
        conn, cursor = self.open()
        # 执行sql语句
        cursor.execute(sql,args)
        # 提交
        conn.commit()
        self.close(conn,cursor)


# 实例化对象
db = SqlHelper()