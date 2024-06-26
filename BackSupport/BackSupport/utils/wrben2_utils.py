# Description: 视图函数wrben2对应的工具函数
import datetime
import random
from BackSupport.utils.dbutils import read_data_from_database
from sklearn.preprocessing import MinMaxScaler
import numpy as np

############## 大多数服务于五档状态评判折线图的函数 ################
# 计算传递进去的输入电压和输出电压的电压比率
def cal_voltage_ratio(Vin, Vout):
    return (Vout-Vin) / Vin

# 计算所有数据中每行数据的输入输出电路的电压比率，并且将电路权重乘以电压比率
def cal_all_voltage_ratios():
    # 读取存储电压数据的数据表
    data = read_data_from_database('device_upload')
    # 读取存储电路权重数据的数据表
    data_weight = read_data_from_database('device_circuit_weight')
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
            # print('输出权重信息',item) # 无误
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

# 拿着上面算出来的每行数据中，8条电路带权重的电压比率，进行最后的加权平均数计算
# 然后根据加权平均数的值，生成随机数。每行数据都会得到一个健康状态评判。
def cal_weight_voltage_result_radom():
    # 获取所有电路的电压比率
    all_voltage_ratios = cal_all_voltage_ratios()
    # 结果列表
    total_voltage_ratios = []
    # 存储每行数据加权电压比率对应的随机数
    grade_random = []
    # 遍历每行数据，将每行数据的电压比率相加,因为加权平均数的计算是将每个数据乘以权重后相加，然后除以权重的总和
    for voltage_ratios in all_voltage_ratios:
        # 每行数据的电压比率相加
        total_voltage_ratio = sum(voltage_ratios)
        # 记得除以权重的个数8，我说咋总不对，，，结果保留四位小数
        total_voltage_ratio = round(total_voltage_ratio/8, 4)
        # 存储到结果列表中
        total_voltage_ratios.append(total_voltage_ratio)
    # 读取这个加权计算后的结果，进行随机数赋值
    '''
            十分健康：如果0.033<=total_voltage_ratio<=0.034之间，生成0~50的随机数
            健康：如果0.031<=total_voltage_ratio<0.033 & 0.034<total_voltage_ratio<=0.035之间，生成50~150的随机数
            正常：如果0.029<=total_voltage_ratio<0.031 & 0.035<total_voltage_ratio<=0.036之间，生成150~200的随机数
            轻微严重：如果0.027<=total_voltage_ratio<0.029 & 0.036<total_voltage_ratio<=0.0385之间，生成200~300的随机数
            十分严重：其余情况全部生成，生成300~500的随机数
            存储在grade_random列表中
    '''
    for i in range(len(total_voltage_ratios)):
        if 0.033 <= total_voltage_ratios[i] <= 0.034:
            grade_random.append(random.randint(0, 50))
        elif (0.031 <= total_voltage_ratios[i] < 0.033) or (0.034 < total_voltage_ratios[i] <= 0.035):
            grade_random.append(random.randint(50, 150))
        elif (0.029 <= total_voltage_ratios[i] < 0.031) or (0.035 < total_voltage_ratios[i] <= 0.036):
            grade_random.append(random.randint(150, 200))
        elif (0.027 <= total_voltage_ratios[i] < 0.029) or (0.036 < total_voltage_ratios[i] <= 0.0385):
            grade_random.append(random.randint(200, 300))
        else:
            grade_random.append(random.randint(300, 500))

    # 看看生成结果：
    # print(grade_random)
    # 要将生成的一维列表 grade_random 转变为需要的格式，只需要将列表中的每个元素包装到一个小的列表中，并确保每个小列表的第一个元素是对应的索引转换为字符串
    required_data_format = [[str(i + 1), num] for i, num in enumerate(grade_random)]
    # 返回结果
    # 这将返回如下格式的列表
    # [
    #     ["1", 422],
    #     ["2", 459],
    #     ["3", 442],
    #     ...
    # ]

    return required_data_format
# 五档健康折线图状态评判建议
def report_cal_line_graph_five_levle_suggest():
    """

    Returns:
        report_info:返回最多的两种状态的评语

    """
    # 假设这是一个获取所有电路电压比率的函数
    all_voltage_ratios = cal_all_voltage_ratios()
    # 结果列表
    total_voltage_ratios = []
    for voltage_ratios in all_voltage_ratios:
        # 每行数据的电压比率相加后除以权重个数8，结果保留四位小数
        total_voltage_ratio = round(sum(voltage_ratios)/8, 4)
        # 存储到结果列表中
        total_voltage_ratios.append(total_voltage_ratio)
    # 根据设定的条件统计每个类别的数量
    health_categories = {"十分健康": 0, "健康": 0, "正常": 0, "轻微严重": 0, "十分严重": 0}
    for ratio in total_voltage_ratios:
        if 0.033 <= ratio <= 0.034:
            health_categories["十分健康"] += 1
        elif 0.031 <= ratio < 0.033 or 0.034 < ratio <= 0.035:
            health_categories["健康"] += 1
        elif 0.029 <= ratio < 0.031 or 0.035 < ratio <= 0.036:
            health_categories["正常"] += 1
        elif 0.027 <= ratio < 0.029 or 0.036 < ratio <= 0.0385:
            health_categories["轻微严重"] += 1
        else:
            health_categories["十分严重"] += 1

    # 筛选出数量最多的两种状态
    sorted_categories = sorted(health_categories.items(), key=lambda item: item[1], reverse=True)[:2]
    most_two_level = [category[0] for category in sorted_categories]
    report_info = f'经过分析：您提供的数据中"{most_two_level[0]}"与"{most_two_level[1]}"是主要的健康状态。'
    return report_info



############## 大多数服务于接线柱磨损分析饼状图的函数 ################

# 获取数据库中每列输入电压（Voltage1、Voltage3、Voltage5...）的函数，每列存储到一个列表，最后返回一个包含所有列的列表
def get_input_voltages():
    """

    Returns:
        vol_input_lists

    """
    # 读取存储电压数据的数据表
    data = read_data_from_database('device_upload')
    # 创建8个空列表，对应8个Voltage字段
    # 它创建了一个列表vol_lists，该列表包含了8个空的子列表。这相当于一个二维数组，其中包含8个一级子列表，它们被用来分别存储每一个电压字段的数据
    vol_input_lists = [[] for _ in range(8)]
    # 遍历每行数据，将对应的Voltage数据追加到相应的列表中
    for item in data:
        for i in range(8):
            voltage_key = f'Voltage{i * 2 + 1}'
            if voltage_key in item:
                vol_input_lists[i].append(item[voltage_key])

    # 返回这个二维数组
    return vol_input_lists

# 传入上面获取的输入电压列表。计算相邻两项之间的差值，然后将这些差值存储到一个列表中
def cal_diff_voltages(input_voltages):
    """
    计算相邻两项之间的差值
    Args:
        input_voltages: 传入的二维数组，包含了8个一维子列表，每个子列表存储了一个Voltage字段的数据

    Returns:
        diff_voltages :返回所有差值

    """
    # 结果列表
    diff_voltages = []
    # 参数为一个二维数组，遍历每行数据，计算每行数据的相邻电压之间的差值
    for input_voltage in input_voltages:
        # 存储单行数据的差值
        diff_voltage = []
        # 表征每行数据（相当于我数据库中的一列字段）的长度
        len_voltage = len(input_voltage)
        # 计算每行数据的输入电压之间的差值，差值取绝对值
        for i in range(1, len_voltage):
            diff_voltage.append(input_voltage[i] - input_voltage[i - 1])
            # 结果保留两位小数，取绝对值
            diff_voltage[i - 1] = abs(diff_voltage[i - 1])
            diff_voltage[i - 1] = round(diff_voltage[i - 1], 2)
        # 将每行数据的差值存储到diff_voltages列表中
        diff_voltages.append(diff_voltage)
    # 返回所有差值
    return diff_voltages

# 传递一维列表，写一个只是遍历单个列表进行统计的函数，统计在0~50,50~150，150~200，200~300，300~500这几个区间的差值个数
def count_diff_voltages_single(diff_voltage):
    """

    Args:
        diff_voltage: 单列电压差值列表

    Returns:
        count_diff_single:本列的各个阶段数据统计

    """
    # 结果字典
    count_diff_single = {
        '0-50': 0,
        '50-150': 0,
        '150-200': 0,
        '200-300': 0,
        '300-500': 0
    }
    # 遍历每行数据，统计每行数据的差值在不同区间的个数
    for diff in diff_voltage:
        if 0 <= diff <= 50:
            count_diff_single['0-50'] += 1
        elif 50 < diff <= 150:
            count_diff_single['50-150'] += 1
        elif 150 < diff <= 200:
            count_diff_single['150-200'] += 1
        elif 200 < diff <= 300:
            count_diff_single['200-300'] += 1
        elif 300 < diff <= 500:
            count_diff_single['300-500'] += 1
    # 返回统计结果
    return count_diff_single

def count_diff_voltages_all(diff_voltages):
    """
    统计在0~50,50~150，150~200，200~300，300~500这几个区间的差值个数
    Args:
        diff_voltages: 传递上面得到的二维差值列表

    Returns:
        count_diff:统计结果

    """
    # 结果字典
    count_diff = {
        '0-50': 0,
        '50-150': 0,
        '150-200': 0,
        '200-300': 0,
        '300-500': 0
    }
    # 遍历每行数据，统计每行数据的差值在不同区间的个数
    for diff_voltage in diff_voltages:
        for diff in diff_voltage:
            if 0 <= diff <= 50:
                count_diff['0-50'] += 1
            elif 50 < diff <= 150:
                count_diff['50-150'] += 1
            elif 150 < diff <= 200:
                count_diff['150-200'] += 1
            elif 200 < diff <= 300:
                count_diff['200-300'] += 1
            elif 300 < diff <= 500:
                count_diff['300-500'] += 1
    # 返回统计结果
    return count_diff

# 编写函数，其中调用count_diff_voltages_single，将{'0-50': 154, '50-150': 234, '150-200': 68, '200-300': 69, '300-500': 4}，{'0-50': 153, '50-150': 207, '150-200': 92, '200-300': 76, '300-500': 1}的返回值做成一个列表
def single_count_dict_in_list():
    """

    Returns:
        count_diffs_dict_in_list:每个阶段的统计结果,列表中套着字典

    """
    # 获取所有输入电压
    input_voltages = get_input_voltages()
    # 计算每列的差值
    diff_voltages = cal_diff_voltages(input_voltages)
    # 统计每列电压的差值规模，每列结果是一个字典，将8个字典最后存储到一个列表中
    count_diffs_dict_in_list = [count_diff_voltages_single(diff_voltage) for diff_voltage in diff_voltages]
    # 返回结果
    return count_diffs_dict_in_list


# 调用single_count_dict_in_list函数，将返回值count_diff_voltages_single中获得的每个列表的阶段结果中，'150-200'的数据提取出来。
# 每个列表为一个'Terminal-x'，例如第一个列表按照'Terminal-1'：'150-200'的数值的格式存储到一个字典中
def format_terminal_data(count_diffs_dict_in_list):
    """

    Args:
        count_diffs_dict_in_list: 八条路各个阶段的数据字典

    Returns:
        formatted_data:每条电路格式化后的结果

    """
    formatted_data = []
    # 遍历统计结果列表，每个结果是一个字典，包含不同范围的数量
    for i, count_diff_dict in enumerate(count_diffs_dict_in_list):
        # 获取'200-300'范围的数量
        count = count_diff_dict.get('200-300', 0)
        # 根据格式构建新的字典，并加入到列表中
        formatted_data.append({
            'value': count,
            'name': f'电池接线柱-{i+1}'
        })
    return formatted_data

# 筛选出format_terminal_data函数返回值的formatted_data中'value'键值最大的五个元素
def get_top_five_values(formatted_data):
    """

    Args:
        formatted_data:

    Returns:
        top_five:value值最高的5个

    """
    # 根据'value'键值对列表进行排序，设置reverse=True表示降序排列
    sorted_data = sorted(formatted_data, key=lambda x: x['value'], reverse=True)
    # 获取排序后的前五个元素，即'value'最大的五个元素
    top_five = sorted_data[:5]
    return top_five

# 从磨损最严重的五条接线柱中统计出3个接线柱的磨损最严重的接线柱名称
def report_get_top_three_terminal_names(top_five):
    """

    Args:
        top_five: 传递的前五个数据

    Returns:
        top_three:返回的前三个数据
        report_info:综合评语

    """
    # 获取前三个数据的'name'键值，即接线柱名称
    top_three = [item['name'] for item in top_five[:3]]
    report_info = f'当前汽车电池接线柱"{top_three[0]}"、"{top_three[1]}"与"{top_three[2]}"磨损最为严重，请及时检修。'
    return report_info


############## 大多数服务于多数据标准判断的堆叠图的函数 ################
# 获取数据库中每列输出电压（Voltage2、Voltage4、Voltage6...）的函数，每列存储到一个列表，最后返回一个包含所有列的列表
def get_output_voltages():
    """

    Returns:
        vol_output_lists

    """
    # 读取存储电压数据的数据表
    data = read_data_from_database('device_upload')
    # 创建8个空列表，对应8个Voltage字段
    vol_output_lists = [[] for _ in range(8)]
    # 遍历每行数据，将对应的Voltage数据追加到相应的列表中
    for item in data:
        for i in range(8):
            voltage_key = f'Voltage{i * 2 + 2}'
            if voltage_key in item:
                vol_output_lists[i].append(item[voltage_key])

    # 返回这个二维数组
    return vol_output_lists

# 根据上面返回的二维输出电压列表。计算其中每一个一维列表的平均值、众数、中位数、方差。开四个列表分别存储这些统计结果，最后按照键值对的形式返回，值是每一个统计值统计到的列表
def cal_statistics(vol_output_lists):
    """

    Args:
        vol_output_lists: 传递的二维输出电压列表

    Returns:
        statistics:统计结果

    """
    # 结果字典
    statistics = {
        'mean': [],
        'mode': [],
        'median': [],
        'variance': [],
        'abnormal':[]

    }
    # 遍历每列数据，计算每列数据的平均值、众数、中位数、方差、异常值
    for vol_output in vol_output_lists:
        # 计算平均值
        mean = round(sum(vol_output) / len(vol_output), 2)
        # 计算众数
        mode = max(set(vol_output), key=vol_output.count)
        # 计算中位数
        median = sorted(vol_output)[len(vol_output) // 2]
        # 计算方差
        variance = round(sum((x - mean) ** 2 for x in vol_output) / len(vol_output), 2)
        # 计算异常值，如果输出电压大于500，则认为是异常值
        abnormal = len([x for x in vol_output if x > 500])
        # 将结果存储到字典中
        statistics['mean'].append(mean)
        statistics['mode'].append(mode)
        statistics['median'].append(median)
        statistics['variance'].append(variance)
        statistics['abnormal'].append(abnormal)
    # 返回统计结果
    return statistics

# 传递上面的统计结果statistics。对每个键中的信息通过pandas进行标准化，然后将标准化后的结果存储到一个列表中，最后返回这个二维列表
def standardize_statistics_func(statistics):
    """

    Args:
        statistics: 传递的统计结果

    Returns:
        standardized_statistics:标准化后的统计结果

    """
    # 创建MinMaxScaler对象
    scaler = MinMaxScaler()
    # # 将统计结果转换为DataFrame
    # df = pd.DataFrame(statistics)
    # # 标准化
    # standardized_statistics = scaler.fit_transform(df)
    # 对于每个统计数据列表进行标准化
    for key in statistics:
        # 转换为二维数组以符合scaler的输入要求
        data = [[x] for x in statistics[key]]
        # 使用MinMaxScaler进行标准化操作
        scaled_data = scaler.fit_transform(data)
        # 将标准化后的数据更新回statistics中,保留两位小数
        statistics[key] = [round(x[0], 3) for x in scaled_data]

    standardized_statistics = statistics
    return standardized_statistics


# 对standardized_statistics，statistics，中平均数、众数、中位数、方差、异常值等信息进行统计汇报
def report_statistics(statistics):
    """

    Args:
        statistics: 五种统计信息

    Returns:
        report:
    评判结果没有什么问题，但是我感觉众数的统计不对劲。
    """
    report = ''
    try:
        # 中位数汇报
        median_average = np.mean(statistics['median'])
        report += f'电压的中位数平均值是{median_average:.2f}V;'

        # 出现最多的电压（众数）汇报
        mode_most_common = max(set(statistics['mode']), key=statistics['mode'].count)
        report += f'出现最多的电压是{mode_most_common}V;'

        # 均值汇报
        mean_average = np.mean(statistics['mean'])
        report += f'电压的均值是{mean_average:.2f}V;'

        # 方差汇报
        variance_average = np.mean(statistics['variance'])
        report += f'从方差中可以知道电压值的波动性，平均方差是{variance_average:.2f};'

        # 异常值汇报
        total_abnormal = sum(statistics['abnormal'])
        report += f'出现了{total_abnormal}个异常值。'
    except Exception as e:
        report += f'计算异常，请检查输入数据。错误信息: {str(e)}'

    return report

############## 大多数服务于动态柱状图函数 ################
def report_dynamic_bar():
    report = "5号电路支路和2号电路支路出现的警报频率较高，建议检修"
    return report

############## 大多数服务于仪表盘评分函数 ################
def report_grade():
    report = "当前模型评分良好，请相信我们"
    return report

# 调用以上五种report_函数，综合每个函数的返回值，给出一个综合评判
def report_all():
    """

    Returns:
        report_total

    """
    count_diffs_dict_in_list = single_count_dict_in_list()
    formatted_data = format_terminal_data(count_diffs_dict_in_list)
    top_five = get_top_five_values(formatted_data)
    vol_output_lists = get_output_voltages()
    statistics = cal_statistics(vol_output_lists)
    report_total = report_cal_line_graph_five_levle_suggest() + report_get_top_three_terminal_names(top_five) + report_statistics(statistics) + report_dynamic_bar() + report_grade()
    return report_total