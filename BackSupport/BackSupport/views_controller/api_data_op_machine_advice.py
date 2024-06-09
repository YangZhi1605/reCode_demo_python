from flask import Flask, Blueprint, request, jsonify
import json
from BackSupport.utils.wrben2_utils import report_cal_line_graph_five_levle_suggest, \
    report_get_top_three_terminal_names, report_statistics, single_count_dict_in_list, format_terminal_data, \
    get_top_five_values, get_output_voltages, cal_statistics, report_grade, report_dynamic_bar
# 导入解决跨域请求
from flask_cors import CORS
# 创建蓝图
api_data_op_machine_advice = Blueprint('api_data_op_machine_advice', __name__)
# 解决跨域请求
CORS(api_data_op_machine_advice)

# 调用report_cal_line_graph_five_levle_suggest获取折线图分析建议的请求接口
@api_data_op_machine_advice.route('/api/get_machine_advice',methods=['GET'])
def get_machine_advice():
    # 获取折线图分析建议
    result = report_cal_line_graph_five_levle_suggest()
    return jsonify({
        'success': True,
        'message': '获取成功',
        'data': result
    }), 200

# 调用report_get_top_three_terminal_names获取前三名磨损状态最严重的接线柱名称的请求接口
@api_data_op_machine_advice.route('/api/get_top_three_terminal_names',methods=['GET'])
def get_top_three_terminal_names():
    # 数据获取
    count_diffs_dict_in_list = single_count_dict_in_list()
    formatted_data = format_terminal_data(count_diffs_dict_in_list)
    top_five = get_top_five_values(formatted_data)
    # 获取前三名磨损状态最严重的接线柱名称
    result = report_get_top_three_terminal_names(top_five)
    return jsonify({
        'success': True,
        'message': '获取成功',
        'data': result
    }), 200


# 调用report_statistics获取统计数据的请求接口
@api_data_op_machine_advice.route('/api/get_statistics',methods=['GET'])
def get_statistics():
    vol_output_lists = get_output_voltages()
    statistics = cal_statistics(vol_output_lists)
    # 获取统计数据
    result = report_statistics(statistics)
    return jsonify({
        'success': True,
        'message': '获取成功',
        'data': result
    }), 200

# 调用report_dynamic_bar获取动态柱状图的评测结果的接口
@api_data_op_machine_advice.route('/api/get_dynamic_bar',methods=['GET'])
def get_dynamic_bar():
    # 获取动态柱状图的评测结果
    result = report_dynamic_bar()
    return jsonify({
        'success': True,
        'message': '获取成功',
        'data': result
    }), 200


# 调用report_grade获得仪表板评分结果的接口
@api_data_op_machine_advice.route('/api/get_grade',methods=['GET'])
def get_grade():
    # 获取评分结果
    result = report_grade()
    return jsonify({
        'success': True,
        'message': '获取成功',
        'data': result
    }), 200