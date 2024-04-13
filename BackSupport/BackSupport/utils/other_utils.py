# Description: 一些其他的工具函数
import datetime
from BackSupport.utils.dbutils import read_data_from_database

# 计算传递进去的输入电压和输出电压的电压比率
def cal_voltage_ratio(Vin, Vout):
    return (Vin-Vout) / Vin

# 计算所有电路的电压比率并拿着计算出来的电压比率乘以权重
def cal_all_voltage_ratios():
    # 读取存储电压数据的数据表
    data = read_data_from_database('device_upload')
    # 读取存储电路权重数据的数据表
    data_weight = read_data_from_database('device_circuit_weight')
    # 结果列表，将包含每行数据的所有电压比率
    all_voltage_ratios = []
    # 为每行数据计算电压比率
    for item in data:
        # 存储单行数据的电压比率
        voltage_ratios = []
        # 按对计算电压比率，从Voltage1/Voltage2 到 Voltage15/Voltage16
        for i in range(1, 16, 2):
            Vin = item[f'Voltage{i}']
            Vout = item[f'Voltage{i + 1}']
            ratio = cal_voltage_ratio(Vin, Vout)
            # 保留四位小数
            ratio = round(ratio, 4)
            voltage_ratios.append(ratio)
        all_voltage_ratios.append(voltage_ratios)


    return all_voltage_ratios

ress=cal_all_voltage_ratios()
for res in ress:
    print('总数量：',len(ress))
    print('每行的数量:',len(res))
    print(res)
