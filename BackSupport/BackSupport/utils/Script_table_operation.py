# 该py文件负责MYSQL数据库中数据表的生成。不同的函数创建不同的表
import random
import pymysql



# 连接数据库 —— 这里的连接数据库的操作，是在本地数据库中进行的，没有上数据库连接池
db = pymysql.connect(host='localhost',
                     user='root',
                     password='123456',
                     db='graduate')

cursor = db.cursor()

# 向指定的数据表格中，插入伪造数据
def def_insert_data():
    # 定义要插入数据的数量
    num_rows = 500
    # 生成并插入随机数据
    for i in range(num_rows):
        info_type = 1
        device_node_id = 'node1'
        device_name = 'device_fk'
        user_id = 'user1'
        collect_time = '2023-07-01 08:31'

        # 生成随机值
        voltage_values = []
        for j in range(1, 17):
            if j % 2 == 1:
                # 表征输入电流，生成这个区间中的随机数，保留两位小数
                voltage = random.uniform(12.43, 399.56)
            else:
                # 表征输出电流
                voltage = random.uniform(301.01, 332.99)
            voltage_values.append(round(voltage, 2))


        # 构建SQL语句
        sql = """
        INSERT INTO device_fk (InfoType, DeviceNodeID, DeviceName, UserID, CollectTime, Voltage1, Voltage2, Voltage3, Voltage4, Voltage5, Voltage6, Voltage7, Voltage8, Voltage9, Voltage10, Voltage11, Voltage12, Voltage13, Voltage14, Voltage15, Voltage16)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        cursor.execute(sql, (info_type, device_node_id, device_name, user_id, collect_time) + tuple(voltage_values))

    # 提交更改并关闭数据库连接
    db.commit()
    db.close()

# 调用函数
def_insert_data()



