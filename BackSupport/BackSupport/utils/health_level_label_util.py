from BackSupport.utils.dbutils import read_data_from_database
from BackSupport.utils.sqlhelper import SqlHelper


# 计算传递进去的输入电压和输出电压的电压比率
def cal_voltage_ratio(Vin, Vout):
    '''

    Args:
        Vin:
        Vout:

    Returns:
        (Vout-Vin) / Vin

    '''
    return (Vout-Vin) / Vin

# 计算所有数据中每行数据的输入输出电路的电压比率，并且将电路权重乘以电压比率
def cal_all_voltage_ratios(data, data_weight):
    '''
    计算所有数据中每行数据的输入输出电路的电压比率，并且将电路权重乘以电压比率
    Args:
        data:
        data_weight:

    Returns:
        all_voltage_ratios

    '''
    # 读取存储电压数据的数据表
    data = read_data_from_database(data)
    # 读取存储电路权重数据的数据表
    data_weight = read_data_from_database(data_weight)
    # print('输出权重信息',data_weight) # 无误
    # 结果列表，将包含每行数据的所有电压比率
    all_voltage_ratios = []
    # 每行遍历，每次读取出来的列表中的每行数据（是一个字典）计算电压比率，同时读取电路权重数据表，将电路权重乘以电压比率
    for item in data:
        # 存储单行数据的电压比率
        voltage_ratios = []
        # 按对计算电压比率，从Voltage1/Voltage2 到 Voltage15/Voltage16。存储到voltage_ratios列表中，该列表中应该有8个数据
        for i in range(1, 16, 2):
            Vin = item[f'Voltage{i}']
            Vout = item[f'Voltage{i + 1}']
            ratio = cal_voltage_ratio(Vin, Vout)
            # 保留四位小数
            ratio = round(ratio, 4)
            voltage_ratios.append(ratio) #存储好相邻两个输入输出电压的电压比率

        # 遍历电路权重数据表，将电路权重乘以电压比率
        for item in data_weight:
            # print('当前使用的输出权重信息',item) # 无误
          # 如果数据表中的IsSet为1，表示该行数据有效，则进行加权计算
            if item['IsSet'] == 1:
                # 从Circuit1到Circuit8
                for i in range(1, 9):
                    # 拿voltage_ratios列表中的信息，计算加权后的电压比率
                    # print('当前的权重是：',item[f'Circuit{i}']) # 无误
                    voltage_ratios[i - 1] *= item[f'Circuit{i}']
                    # 结果保留四位小数
                    voltage_ratios[i - 1] = round(voltage_ratios[i - 1], 4)

        # 最后将每行计算好的电压比率存储到all_voltage_ratios列表中
        all_voltage_ratios.append(voltage_ratios)
    # 返回所有经过加权计算的电压比率
    return all_voltage_ratios

# 测试
# print('加权后的电压比率为：',cal_all_voltage_ratios('device_analysis', 'device_circuit_weight'))


# 调用函数中计算每行数据中电压比率*权重后的结果进行最后的加权平均数计算，根据计算结果进行健康等级的划分
def cal_weight_voltage_result_for_label():
    # 调用函数计算每行数据中电压比率*权重后的结果
    all_voltage_ratios = cal_all_voltage_ratios('device_analysis', 'device_circuit_weight')
    # print('输出的所有电压比率',all_voltage_ratios) # 无误
    # 结果列表，将包含每行数据的最终加权平均数
    all_weight_voltage_results = []
    # 遍历每行数据，计算每行数据的加权平均数
    for item in all_voltage_ratios:
        # 计算每行数据的加权平均数
        weight_voltage_result = sum(item) / len(item)
        # 结果保留四位小数
        weight_voltage_result = round(weight_voltage_result, 4)
        # 将每行数据的加权平均数存储到all_weight_voltage_results列表中
        all_weight_voltage_results.append(weight_voltage_result)
    # 返回所有数据的加权平均数
    # print('输出的所有加权平均数',all_weight_voltage_results)
    # 此时得到所有数据的加权平均数，根据加权平均数进行健康等级的划分
    '''
        十分健康：如果0.033<=total_voltage_ratio<=0.034之间，标注为十分健康
        健康：如果0.031<=total_voltage_ratio<0.033 & 0.034<total_voltage_ratio<=0.035之间，标注为健康
        正常：如果0.029<=total_voltage_ratio<0.031 & 0.035<total_voltage_ratio<=0.036之间，标注为正常
        轻微严重：如果0.027<=total_voltage_ratio<0.029 & 0.036<total_voltage_ratio<=0.0385之间，标注为轻微严重
        十分严重：其余情况全部生成，标注为十分严重
    '''
    # 存储最后的健康等级
    all_health_levels = []
    # 遍历每行数据，根据加权平均数进行健康等级的划分
    for item in all_weight_voltage_results:
        if 0.033 <= item <= 0.034:
            health_level = '十分健康'
        elif 0.031 <= item < 0.033 or 0.034 < item <= 0.035:
            health_level = '健康'
        elif 0.029 <= item < 0.031 or 0.035 < item <= 0.036:
            health_level = '正常'
        elif 0.027 <= item < 0.029 or 0.036 < item <= 0.0385:
            health_level = '轻微严重'
        else:
            health_level = '十分严重'
        # 将每行数据的健康等级存储到all_health_levels列表中
        all_health_levels.append(health_level)
    # 返回所有数据的健康等级
    return all_health_levels

# 测试
# print(cal_weight_voltage_result_for_label())
# print('加权后的电压比率为：',cal_all_voltage_ratios('device_analysis', 'device_circuit_weight'))
# cal_weight_voltage_result_for_label()

# 将最后的健康等级存储到device_analysis数据表的HealthLevel列中
def save_health_level_to_database():
    # 实例化数据库帮助类
    db = SqlHelper()
    # 获取数据库连接和游标
    conn, cursor = db.open()

    try:
        # 调用函数计算每行数据的健康等级
        all_health_levels = cal_weight_voltage_result_for_label()
        # 遍历每行数据，将健康等级存储到device_analysis数据表的HealthLevel列中
        for i, item in enumerate(all_health_levels):
            # 更新数据表中的HealthLevel列
            update_sql = f"UPDATE device_analysis SET HealthLevel = '{item}' WHERE ID = {i + 1}"
            # print(update_sql) # 无误
            # 在游标上执行更新语句
            cursor.execute(update_sql)
        # 提交事务
        conn.commit()
        # print("数据成功存入数据库")
    except Exception as e:
        # 如果发生错误就回滚
        conn.rollback()
        print("处理文件或数据库操作时出错:", e)
        raise
    finally:
        # 最后不管有没有异常都要关闭连接
        db.close(conn, cursor)

save_health_level_to_database()