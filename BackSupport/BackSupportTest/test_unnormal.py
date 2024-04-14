from BackSupport import create_app
from BackSupport.model_logic.VoltageModel import db, Device,Device_Circuit_Weight  # 确保导入Device模型
from BackSupport.utils.dbutils import read_data_from_database
import datetime

from BackSupport.utils.wrben2_utils import get_input_voltages, cal_diff_voltages, count_diff_voltages_all, \
    count_diff_voltages_single, format_terminal_data, single_count_dict_in_list, get_top_five_values


# 你可以把这部分代码放到一个函数中，而不是在模块层级执行
def print_odd_voltages():
    app = create_app()
    with app.app_context():
        odd_voltages = Device.get_odd_voltages()
        for voltages in odd_voltages:
            print(voltages)


# 测试dbutils.py中的read_data_from_database方法返回值
def print_data_device():
    data_list = read_data_from_database('device_fk')
    for data in data_list:
        if isinstance(data['CollectTime'], datetime.datetime):
            data['CollectTime'] = data[
                'CollectTime'].isoformat()  # 输出的日期时间格式是 "YYYY-MM-DDTHH:MM:SS" 形式的 ISO 标准字符串

    print(data_list)
    # 在列表中，以字典的形式存储了数据库中的数据
    # [{'ID': 1, 'InfoType': 2, 'DeviceNodeID': 'node1', 'DeviceName': '电动机', 'UserID': '1001', 'CollectTime': datetime.datetime(2019, 3, 13, 21, 15, 41), 'Voltage1': 2.21, 'Voltage2': 1.89, 'Voltage3': 3.45, 'Voltage4': 2.78, 'Voltage5': 3.67, 'Voltage6': 1.45, 'Voltage7': 2.9, 'Voltage8': 2.22, 'Voltage9': 1.78, 'Voltage10': 2.67, 'Voltage11': 1.34, 'Voltage12': 2.89, 'Voltage13': 2.24, 'Voltage14': 1.92, 'Voltage15': 5.91, 'Voltage16': 4.32}, {'ID': 2, 'InfoType': 2, 'DeviceNodeID': 'node1', 'DeviceName': '电动机', 'UserID': '1001', 'CollectTime': datetime.datetime(2019, 3, 13, 21, 15, 41), 'Voltage1': 2.21, 'Voltage2': 1.89, 'Voltage3': 3.45, 'Voltage4': 2.78, 'Voltage5': 3.67, 'Voltage6': 1.45, 'Voltage7': 2.9, 'Voltage8': 2.22, 'Voltage9': 1.78, 'Voltage10': 2.67, 'Voltage11': 1.34, 'Voltage12': 2.89, 'Voltage13': 2.24, 'Voltage14': 1.92, 'Voltage15': 5.91, 'Voltage16': 4.32}, {'ID': 3, 'InfoType': 2, 'DeviceNodeID': 'node1', 'DeviceName': '电动机', 'UserID': '1001', 'CollectTime': datetime.datetime(2019, 3, 13, 21, 15, 41), 'Voltage1': 2.21, 'Voltage2': 1.89, 'Voltage3': 3.45, 'Voltage4': 2.78, 'Voltage5': 3.67, 'Voltage6': 1.45, 'Voltage7': 2.9, 'Voltage8': 2.22, 'Voltage9': 1.78, 'Voltage10': 2.67, 'Voltage11': 1.34, 'Voltage12': 2.89, 'Voltage13': 2.24, 'Voltage14': 1.92, 'Voltage15': 5.91, 'Voltage16': 4.32}, {'ID': 4, 'InfoType': 2, 'DeviceNodeID': 'node2', 'DeviceName': '电动机', 'UserID': '1001', 'CollectTime': datetime.datetime(2019, 3, 13, 21, 15, 41), 'Voltage1': 2.21, 'Voltage2': 1.89, 'Voltage3': 3.45, 'Voltage4': 2.78, 'Voltage5': 3.67, 'Voltage6': 1.45, 'Voltage7': 2.9, 'Voltage8': 2.22, 'Voltage9': 1.78, 'Voltage10': 2.67, 'Voltage11': 1.34, 'Voltage12': 2.89, 'Voltage13': 2.24, 'Voltage14': 1.92, 'Voltage15': 5.91, 'Voltage16': 4.32}, {'ID': 5, 'InfoType': 2, 'DeviceNodeID': 'node1', 'DeviceName': '电动机', 'UserID': '1001', 'CollectTime': datetime.datetime(2019, 3, 13, 21, 15, 41), 'Voltage1': 2.21, 'Voltage2': 1.89, 'Voltage3': 3.45, 'Voltage4': 2.78, 'Voltage5': 3.67, 'Voltage6': 1.45, 'Voltage7': 2.9, 'Voltage8': 2.22, 'Voltage9': 1.78, 'Voltage10': 2.67, 'Voltage11': 1.34, 'Voltage12': 2.89, 'Voltage13': 2.24, 'Voltage14': 1.92, 'Voltage15': 5.91, 'Voltage16': 4.32}, {'ID': 6, 'InfoType': 2, 'DeviceNodeID': 'node2', 'DeviceName': '电动机', 'UserID': '1001', 'CollectTime': datetime.datetime(2019, 3, 13, 21, 15, 41), 'Voltage1': 2.21, 'Voltage2': 1.89, 'Voltage3': 3.45, 'Voltage4': 2.78, 'Voltage5': 3.67, 'Voltage6': 1.45, 'Voltage7': 2.9, 'Voltage8': 2.22, 'Voltage9': 1.78, 'Voltage10': 2.67, 'Voltage11': 1.34, 'Voltage12': 2.89, 'Voltage13': 2.24, 'Voltage14': 1.92, 'Voltage15': 5.91, 'Voltage16': 4.32}, {'ID': 7, 'InfoType': 2, 'DeviceNodeID': 'node1', 'DeviceName': '电动机', 'UserID': '1001', 'CollectTime': datetime.datetime(2019, 3, 13, 21, 15, 41), 'Voltage1': 2.21, 'Voltage2': 1.89, 'Voltage3': 3.45, 'Voltage4': 2.78, 'Voltage5': 3.67, 'Voltage6': 1.45, 'Voltage7': 2.9, 'Voltage8': 2.22, 'Voltage9': 1.78, 'Voltage10': 2.67, 'Voltage11': 1.34, 'Voltage12': 2.89, 'Voltage13': 2.24, 'Voltage14': 1.92, 'Voltage15': 5.91, 'Voltage16': 4.32}, {'ID': 8, 'InfoType': 2, 'DeviceNodeID': 'node2', 'DeviceName': '电动机', 'UserID': '1001', 'CollectTime': datetime.datetime(2019, 3, 13, 21, 15, 41), 'Voltage1': 2.21, 'Voltage2': 1.89, 'Voltage3': 3.45, 'Voltage4': 2.78, 'Voltage5': 3.67, 'Voltage6': 1.45, 'Voltage7': 2.9, 'Voltage8': 2.22, 'Voltage9': 1.78, 'Voltage10': 2.67, 'Voltage11': 1.34, 'Voltage12': 2.89, 'Voltage13': 2.24, 'Voltage14': 1.92, 'Voltage15': 5.91, 'Voltage16': 4.32}, {'ID': 9, 'InfoType': 2, 'DeviceNodeID': 'node1', 'DeviceName': '电动机', 'UserID': '1001', 'CollectTime': datetime.datetime(2019, 3, 13, 21, 15, 41), 'Voltage1': 2.21, 'Voltage2': 1.89, 'Voltage3': 3.45, 'Voltage4': 2.78, 'Voltage5': 3.67, 'Voltage6': 1.45, 'Voltage7': 2.9, 'Voltage8': 2.22, 'Voltage9': 1.78, 'Voltage10': 2.67, 'Voltage11': 1.34, 'Voltage12': 2.89, 'Voltage13': 2.24, 'Voltage14': 1.92, 'Voltage15': 5.91, 'Voltage16': 4.32}, {'ID': 10, 'InfoType': 2, 'DeviceNodeID': 'node2', 'DeviceName': '电动机', 'UserID': '1001', 'CollectTime': datetime.datetime(2019, 3, 13, 21, 15, 41), 'Voltage1': 2.21, 'Voltage2': 1.89, 'Voltage3': 3.45, 'Voltage4': 2.78, 'Voltage5': 3.67, 'Voltage6': 1.45, 'Voltage7': 2.9, 'Voltage8': 2.22, 'Voltage9': 1.78, 'Voltage10': 2.67, 'Voltage11': 1.34, 'Voltage12': 2.89, 'Voltage13': 2.24, 'Voltage14': 1.92, 'Voltage15': 5.91, 'Voltage16': 4.32}, {'ID': 11, 'InfoType': 2, 'DeviceNodeID': 'node1', 'DeviceName': '电动机', 'UserID': '1001', 'CollectTime': datetime.datetime(2019, 3, 13, 21, 15, 41), 'Voltage1': 2.21, 'Voltage2': 1.89, 'Voltage3': 3.45, 'Voltage4': 2.78, 'Voltage5': 3.67, 'Voltage6': 1.45, 'Voltage7': 2.9, 'Voltage8': 2.22, 'Voltage9': 1.78, 'Voltage10': 2.67, 'Voltage11': 1.34, 'Voltage12': 2.89, 'Voltage13': 2.24, 'Voltage14': 1.92, 'Voltage15': 5.91, 'Voltage16': 4.32}, {'ID': 12, 'InfoType': 2, 'DeviceNodeID': 'node2', 'DeviceName': '电动机', 'UserID': '1001', 'CollectTime': datetime.datetime(2019, 3, 13, 21, 15, 41), 'Voltage1': 2.21, 'Voltage2': 1.89, 'Voltage3': 3.45, 'Voltage4': 2.78, 'Voltage5': 3.67, 'Voltage6': 1.45, 'Voltage7': 2.9, 'Voltage8': 2.22, 'Voltage9': 1.78, 'Voltage10': 2.67, 'Voltage11': 1.34, 'Voltage12': 2.89, 'Voltage13': 2.24, 'Voltage14': 1.92, 'Voltage15': 5.91, 'Voltage16': 4.32}, {'ID': 13, 'InfoType': 2, 'DeviceNodeID': 'node1', 'DeviceName': '电动机', 'UserID': '1001', 'CollectTime': datetime.datetime(2019, 3, 13, 21, 15, 41), 'Voltage1': 2.21, 'Voltage2': 1.89, 'Voltage3': 3.45, 'Voltage4': 2.78, 'Voltage5': 3.67, 'Voltage6': 1.45, 'Voltage7': 2.9, 'Voltage8': 2.22, 'Voltage9': 1.78, 'Voltage10': 2.67, 'Voltage11': 1.34, 'Voltage12': 2.89, 'Voltage13': 2.24, 'Voltage14': 1.92, 'Voltage15': 5.91, 'Voltage16': 4.32}, {'ID': 14, 'InfoType': 2, 'DeviceNodeID': 'node1', 'DeviceName': '电动机', 'UserID': '1001', 'CollectTime': datetime.datetime(2019, 3, 13, 21, 15, 41), 'Voltage1': 2.21, 'Voltage2': 1.89, 'Voltage3': 3.45, 'Voltage4': 2.78, 'Voltage5': 3.67, 'Voltage6': 1.45, 'Voltage7': 2.9, 'Voltage8': 2.22, 'Voltage9': 1.78, 'Voltage10': 2.67, 'Voltage11': 1.34, 'Voltage12': 2.89, 'Voltage13': 2.24, 'Voltage14': 1.92, 'Voltage15': 5.91, 'Voltage16': 4.32}, {'ID': 15, 'InfoType': 2, 'DeviceNodeID': 'node1', 'DeviceName': '电动机', 'UserID': '1001', 'CollectTime': datetime.datetime(2019, 3, 13, 21, 15, 41), 'Voltage1': 2.21, 'Voltage2': 1.89, 'Voltage3': 3.45, 'Voltage4': 2.78, 'Voltage5': 3.67, 'Voltage6': 1.45, 'Voltage7': 2.9, 'Voltage8': 2.22, 'Voltage9': 1.78, 'Voltage10': 2.67, 'Voltage11': 1.34, 'Voltage12': 2.89, 'Voltage13': 2.24, 'Voltage14': 1.92, 'Voltage15': 5.91, 'Voltage16': 4.32}, {'ID': 16, 'InfoType': 2, 'DeviceNodeID': 'node1', 'DeviceName': '电动机', 'UserID': '1001', 'CollectTime': datetime.datetime(2019, 3, 13, 21, 15, 41), 'Voltage1': 2.21, 'Voltage2': 1.89, 'Voltage3': 3.45, 'Voltage4': 2.78, 'Voltage5': 3.67, 'Voltage6': 1.45, 'Voltage7': 2.9, 'Voltage8': 2.22, 'Voltage9': 1.78, 'Voltage10': 2.67, 'Voltage11': 1.34, 'Voltage12': 2.89, 'Voltage13': 2.24, 'Voltage14': 1.92, 'Voltage15': 5.91, 'Voltage16': 4.32}]


# 测试Device_Circuit_Weight模型中，获取所有数据的方法
def print_weight():
    app = create_app()
    with app.app_context():
        results = Device_Circuit_Weight.get_all()
        for result in results:
            print(result)

# 测试wrben2_utils.py文件中，get_input_voltages方法能够获取到奇数位的电压值
def test_get_input_voltages():
    app = create_app()
    with app.app_context():
        input_voltages = get_input_voltages()
        for voltages in input_voltages:
            print(voltages)

# 测试wrben2_utils文件中，计算相邻两个输入电压之间的差值
def test_cal_diff_voltage():
    app = create_app()
    with app.app_context():
        # 统计差值个数
        cnt = 0
        input_voltages = get_input_voltages()
        res_total = cal_diff_voltages(input_voltages)
        for item in res_total:
            print(item)
            cnt += len(item)
        print('被作差的个数有',cnt)

# 测试count_diff_voltages函数
def test_count_diff_voltages_all():
    app = create_app()
    with app.app_context():
        input_voltages = get_input_voltages()
        diff_voltages = cal_diff_voltages(input_voltages)
        print('八条路全部计算，各个阶段结果：',count_diff_voltages_all(diff_voltages))

# 测试count_diff_voltages_single函数
def test_count_diff_voltages_single():
    app = create_app()
    with app.app_context():
        input_voltages = get_input_voltages()
        diff_voltages = cal_diff_voltages(input_voltages)
        for i in range(0,len(diff_voltages)):
            print(f'第{i+1}路，各个阶段结果：',count_diff_voltages_single(diff_voltages[i]))

# 测试获得每条路的'200-300'的数据字典
def test_get_200_300():
    app = create_app()
    with app.app_context():
        # 获得统计过每一列数据的各个阶段数量的字典列表
        count_diffs_dict_in_list = single_count_dict_in_list()
        formatted_results = format_terminal_data(count_diffs_dict_in_list)
        print(formatted_results)
        # 获取Top5
        top_five = get_top_five_values(formatted_results)
        for item in top_five:
            print('得到的结果：',item)


# 测试single_count_dict_in_list函数的返回值
def test_single_count_dict_in_list():
    app = create_app()
    with app.app_context():
        count_diffs_dict_in_list = single_count_dict_in_list()
        print(count_diffs_dict_in_list)


# 然后在你想打印变量的时候调用这个函数
if __name__ == '__main__':
    # print_odd_voltages()
    # print_data_device()
    # print_weight()
    # test_get_input_voltages()
    # test_cal_diff_voltage()
    # test_count_diff_voltages_all()
    # test_count_diff_voltages_single()
    # test_single_count_dict_in_list()
    test_get_200_300()
