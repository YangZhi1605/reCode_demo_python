from BackSupport import create_app
from BackSupport.model_logic.VoltageModel import db, Device,Device_Circuit_Weight  # 确保导入Device模型
from BackSupport.utils.dbutils import read_data_from_database
import datetime

from BackSupport.utils.wrben2_utils import get_input_voltages, cal_diff_voltages, count_diff_voltages_all, \
    count_diff_voltages_single, format_terminal_data, single_count_dict_in_list, get_top_five_values, \
    get_output_voltages, cal_statistics, standardize_statistics_func


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

# 测试get_output_voltages函数的返回值
def test_get_output_voltages():
    app = create_app()
    with app.app_context():
        vol_output_lists = get_output_voltages()
        print(vol_output_lists)

# 测试cal_statistics函数计算结果
def test_cal_statistics():
    app = create_app()
    with app.app_context():
        vol_output_lists = get_output_voltages()
        statistics = cal_statistics(vol_output_lists)
        print(statistics)

# 测试standardized_statistics标准化的结果
def test_standardized_statistics():
    app = create_app()
    with app.app_context():
        vol_output_lists = get_output_voltages()
        statistics = cal_statistics(vol_output_lists)
        standardized_statistics = standardize_statistics_func(statistics)
        print(standardized_statistics)

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
    # test_get_200_300()
    # test_get_output_voltages()
    # test_cal_statistics()
    test_standardized_statistics()