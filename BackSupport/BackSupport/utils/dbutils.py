import pandas as pd
from BackSupport.utils.sqlhelper import SqlHelper

# 使用数据库连接池，保存Excel文件到数据库
def save_excel_to_database(file_path, table_name):
    # 读取Excel文件
    df = pd.read_excel(file_path, engine='openpyxl')
    # 实例化数据库帮助类
    db = SqlHelper()
    # 获取数据库连接和游标
    conn, cursor = db.open()
    try:
        # 准备pandas的数据以供插入，应确保列名和数据库中的表列名一致
        # 先转换日期时间格式，别放到循环里去循环转换，转着转着，回到原本格式了
        # 于MySQL数据库来说，日期时间值应该采用YYYY-MM-DD HH:MM:SS的格式，而提供的值'3/11/2019 21:15:41'似乎不符合这个要求。
        df['CollectTime'] = pd.to_datetime(df['CollectTime']).dt.strftime('%Y-%m-%d %H:%M:%S')
        print("输出：", df['CollectTime'])
        # 将DataFrame转换为包含插入语句的迭代器，然后迭代DataFrame来构造和执行SQL插入语句
        for index, row in df.iterrows():
            # 构造INSERT语句，这里需要根据实际的表结构来
            sql = f"INSERT INTO {table_name} (InfoType, DeviceNodeID,DeviceName,UserID,CollectTime,Voltage1,Voltage2,Voltage3,Voltage4,Voltage5,Voltage6,Voltage7,Voltage8,Voltage9,Voltage10,Voltage11,Voltage12,Voltage13,Voltage14,Voltage15,Voltage16) VALUES (%s, %s,%s, %s, %s,%s, %s,%s, %s, %s,%s, %s,%s, %s, %s,%s, %s,%s, %s, %s,%s)"
            values = tuple(row[1:])  # 从索引1开始取，跳过索引0（假设row[0]是ID列）

            # 在游标上执行每行的插入语句
            cursor.execute(sql, values)

        # 执行完成后提交事务
        conn.commit()
        print("数据成功存入数据库")
    except Exception as e:
        # 如果发生错误就回滚
        conn.rollback()
        print("处理文件或数据库操作时出错:", e)
        raise
    finally:
        # 最后不管有没有异常都要关闭连接
        db.close(conn, cursor)

# 读取数据库中的数据
def read_data_from_database(table_name):
    # 实例化数据库帮助类
    db = SqlHelper()
    # 获取数据库连接和游标
    conn, cursor = db.open()
    try:
        # 查询数据库中的数据
        sql = f"SELECT * FROM {table_name}"
        cursor.execute(sql)
        # 获取所有数据
        result = cursor.fetchall()
        return result
    except Exception as e:
        print("读取数据库时出错:", e)
        raise
    finally:
        # 最后不管有没有异常都要关闭连接
        db.close(conn, cursor)

    '''
    读取数据库的数据结果：
    {'ID': 1, 'InfoType': 1, 'DeviceNodeID': 'node1', 'DeviceName': 'device_fk', 'UserID': 'user1', 'CollectTime': '2023-07-01T08:31:00', 'Voltage1': 117.57, 'Voltage2': 304.94, 'Voltage3': 232.47, 'Voltage4': 322.6, 'Voltage5': 297.72, 'Voltage6': 329.14, 'Voltage7': 188.24, 'Voltage8': 328.66, 'Voltage9': 362.1, 'Voltage10': 315.87, 'Voltage11': 33.83, 'Voltage12': 319.05, 'Voltage13': 207.17, 'Voltage14': 306.31, 'Voltage15': 131.8, 'Voltage16': 304.1}
    '''

