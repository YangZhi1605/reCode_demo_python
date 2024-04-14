from flask import Blueprint,jsonify,request
import json
# 导入解决跨域请求
from flask_cors import CORS
from BackSupport.utils.wrben2_utils import cal_weight_voltage_result_radom, get_top_five_values, format_terminal_data, \
    single_count_dict_in_list, get_output_voltages, cal_statistics, standardize_statistics_func

# 创建蓝图
api_data_op_wrben2 = Blueprint('api_data_op_wrben2', __name__)
# 解决跨域请求
CORS(api_data_op_wrben2)

# 编写进行测试的路由
@api_data_op_wrben2.route('/api/test',methods=['GET'])
def test():
    return jsonify({'message':'测试成功','success':True})

# 工作台2——创建AQI数据接口函数
@api_data_op_wrben2.route('/api/graphLine', methods=['GET'])
def graphLine():
    # 到resuorce文件夹下找到life-expectancy-table.json文件
    with open('BackSupport/resource/data/aqi-beijing.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 返回数据,以json格式传递给前端
    return jsonify(data)

# 工作台2——调用wrben2_utils文件中的cal_weight_voltage_result函数得到一个字典，然后返回JSON数据给前台——非MVC版本
@api_data_op_wrben2.route('/api/graphLine_random', methods=['GET'])
def graphLine_random():
    # 调用other_utils文件中的cal_weight_voltage_result函数得到一个字典
    data = cal_weight_voltage_result_radom()
    # print(data)
    # 返回数据,以json格式传递给前端
    return jsonify(data)

# 工作台2——调用wrben2_utils文件中的get_top_five_values生成一个数据，返回给前端
@api_data_op_wrben2.route('/api/graphPie_top', methods=['GET'])
def graphPie_top():
    # 调用other_utils文件中的get_top_five_values生成一个数据
    count_diffs_dict_in_list = single_count_dict_in_list()
    formatted_data = format_terminal_data(count_diffs_dict_in_list)
    top_five = get_top_five_values(formatted_data)
    # 返回数据,以json格式传递给前端
    return jsonify(top_five)


# 工作台2——调用wrben2_utils文件中的standardize_statistics_func生成一个数据，返回给前端
@api_data_op_wrben2.route('/api/graph_stack', methods=['GET'])
def graph_stack():
    # 获取输出电压的数据
    vol_output_lists = get_output_voltages()
    # 计算统计数据
    statistics = cal_statistics(vol_output_lists)
    # 标准化统计数据
    standardized_statistics = standardize_statistics_func(statistics)
    # 返回数据,以json格式传递给前端
    return jsonify(standardized_statistics)