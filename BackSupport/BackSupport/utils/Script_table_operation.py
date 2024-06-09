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
    num_rows = 1200
    # 生成并插入随机数据
    for i in range(num_rows):
        info_type = 1
        device_node_id = 'node4'
        device_name = '蓄电池'
        user_id = '1004'
        collect_time = '2023-10-11 11:53'

        # # 生成随机值——原版
        # voltage_values = []
        # for j in range(1, 17):
        #
        #     if j % 2 == 1:
        #         # 表征输入电流，生成这个区间中的随机数，保留两位小数
        #         voltage = random.uniform(12.43, 399.56)
        #     else:
        #         # 表征输出电流
        #         voltage = random.uniform(301.01, 332.99)
        #     voltage_values.append(round(voltage, 2))

        # 生成随机值
        # 注入随机数——新版
        # 在每次生成输入电流后立刻生成输出电流，并将输入电流的随机值作为输出电流生成的下限
        voltage_values = []
        # 将输入电流和输出电流作为先放置在一个变量中，下面的循环中，对其进行更新
        input_voltage = 137
        output_voltage = 499
        for j in range(1, 17):
            if j % 2 == 1:
                # 表征输入电流，生成这个区间中的随机数，保留两位小数
                input_voltage = random.uniform(137, 467)  # 输入电流随机数生成 —— 正常数据
                # input_voltage = random.uniform(14, 489)  # 输入电流随机数生成 —— 噪声数据
            else:
                # 表征输出电流，生成大于输入电流的随机数，且小于500，保留两位小数,我将是奇数时候的输入电流存储了，这里就可以直接拿着用了
                output_voltage = random.uniform(input_voltage, 500) # 输出电流随机数生成 —— 正常数据
                # output_voltage = random.uniform(input_voltage, 680) # 输出电流随机数生成 —— 噪声数据
            # 每当j是奇数时，生成一个输入电流的随机值存储在input_voltage变量中。接下来的偶数迭代会使用这个input_voltage的值作为uniform函数的下限参数
            voltage = round(output_voltage if j % 2 == 0 else input_voltage, 2)
            voltage_values.append(voltage)
        # 输出voltage_values列表将包含交替的"表征输入电流"和"表征输出电流"的值，输出电流值大于对应的输入电流值且小于500



        # 构建SQL语句——指定插入哪个数据表
        sql = """
        INSERT INTO device_upload (InfoType, DeviceNodeID, DeviceName, UserID, CollectTime, Voltage1, Voltage2, Voltage3, Voltage4, Voltage5, Voltage6, Voltage7, Voltage8, Voltage9, Voltage10, Voltage11, Voltage12, Voltage13, Voltage14, Voltage15, Voltage16)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        cursor.execute(sql, (info_type, device_node_id, device_name, user_id, collect_time) + tuple(voltage_values))

    # 提交更改并关闭数据库连接
    db.commit()
    db.close()

# 向指定的数据表格中。附带健康状态，插入伪造数据
def def_insert_data_and_health():
    # 定义要插入数据的数量
    num_rows = 5000
    # 生成并插入随机数据
    for i in range(num_rows):
        info_type = 4
        device_node_id = 'node4'
        device_name = '增压机'
        user_id = '0303'
        collect_time = '2023-09-06 12:48'
        health_level = ''

        # 生成随机值
        # 在每次生成输入电流后立刻生成输出电流，并将输入电流的随机值作为输出电流生成的下限
        voltage_values = []
        # 将输入电流和输出电流作为先放置在一个变量中，下面的循环中，对其进行更新
        input_voltage = 137
        output_voltage = 499
        for j in range(1, 17):
            if j % 2 == 1:
                # 表征输入电流，生成这个区间中的随机数，保留两位小数
                input_voltage = random.uniform(137, 467)  # 输入电流随机数生成 —— 正常数据
                # input_voltage = random.uniform(14, 489)  # 输入电流随机数生成 —— 噪声数据
            else:
                # 表征输出电流，生成大于输入电流的随机数，且小于500，保留两位小数,我将是奇数时候的输入电流存储了，这里就可以直接拿着用了
                output_voltage = random.uniform(input_voltage, 500) # 输出电流随机数生成 —— 正常数据
                # output_voltage = random.uniform(input_voltage, 680) # 输出电流随机数生成 —— 噪声数据
            # 每当j是奇数时，生成一个输入电流的随机值存储在input_voltage变量中。接下来的偶数迭代会使用这个input_voltage的值作为uniform函数的下限参数
            voltage = round(output_voltage if j % 2 == 0 else input_voltage, 2)
            # 输出voltage_values列表将包含交替的"表征输入电流"和"表征输出电流"的值，输出电流值大于对应的输入电流值且小于500
            voltage_values.append(voltage)




        # 构建SQL语句——指定插入哪个数据表
        sql = """
        INSERT INTO device_analysis (InfoType, DeviceNodeID, DeviceName, UserID, CollectTime, Voltage1, Voltage2, Voltage3, Voltage4, Voltage5, Voltage6, Voltage7, Voltage8, Voltage9, Voltage10, Voltage11, Voltage12, Voltage13, Voltage14, Voltage15, Voltage16,HealthLevel)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        cursor.execute(sql, (info_type, device_node_id, device_name, user_id, collect_time) + tuple(voltage_values)+ (health_level,))

    # 提交更改并关闭数据库连接
    db.commit()
    db.close()

# 调用函数
def_insert_data()
# def_insert_data_and_health()



