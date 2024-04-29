from flask import Blueprint,request,jsonify
import json
# 导入解决跨域请求
from flask_cors import CORS
from BackSupport.service_logic.service import Repair_Log_Service
from BackSupport.model_logic.TotalModel import DeviceNode_MaintainInfo
import os
from datetime import datetime  # 从datetime模块导入datetime类

from BackSupport.utils.wrben2_utils import report_all

# 创建蓝图
api_data_op_maintaininfo = Blueprint('api_data_op_maintaininfo', __name__)
# 解决跨域请求
CORS(api_data_op_maintaininfo)

# 创建服务对象，挂载dao模型
repair_log_service = Repair_Log_Service(DeviceNode_MaintainInfo)

# 编写获取所有维修日志信息的接口
@api_data_op_maintaininfo.route('/api/get_all',methods=['GET'])
def get_all_maintain_info():
    # 获取所有维修日志信息
    repair_log_list = repair_log_service.get_all() # 这里得到的是对象
    # # 将获取的数据转换为字典，以便于返回
    repair_log = [result.to_dict() for result in repair_log_list]
    # 返回JSON数据
    return jsonify(repair_log)

# 编写获取前台id和数据进行更新的接口
@api_data_op_maintaininfo.route('/api/update_info',methods=['POST'])
def update_info():
    # 获取前台传来的数据
    data = request.get_data()
    print('前台反馈的数据',data)
    # 将前台传来的数据转换为字典
    data_dict = json.loads(data)
    # 获取id并将id转换为int类型
    id = int(data_dict['id'])
    # 获取新数据
    new_data = data_dict['new_data']
    # 假定new_data中的MaintenanceDate格式为 'yyyy-mm-ddTHH:MM:SS.sssZ'
    # 需要转换为MySQL接受的格式 'yyyy-mm-dd HH:MM:SS'
    # 首先移除毫秒和'Z'
    formatted_date = new_data['MaintenanceDate'].split('.')[0]
    # 接着去除'T'
    formatted_date = formatted_date.replace('T', ' ')
    # 将格式化后的时间字符串赋值回new_data
    new_data['MaintenanceDate'] = formatted_date
    # 调用服务层的更新方法
    repair_log_service.update_info(id,new_data)
    # 返回JSON数据
    return jsonify({'msg':'success'})

# 编写获取前台传来的id进行删除的接口
@api_data_op_maintaininfo.route('/api/delete_info',methods=['GET'])
def delete_info():
    # 获取前台传来的id
    id = int(request.args.get('id'))
    # 调用服务层的删除方法
    repair_log_service.delete_info(id)
    # 返回JSON数据
    return jsonify({'msg':'success'})

# 根据前台传来的搜索字符串进行模糊查询的接口
@api_data_op_maintaininfo.route('/api/search_info',methods=['GET'])
def search_info():
    # 获取前台传来的搜索字符串
    searchVal = request.args.get('searchVal')
    # 调用服务层的查询方法
    search_result = repair_log_service.search_info(searchVal)
    # 将查询结果转换为字典
    search_result = [result.to_dict() for result in search_result]
    # 返回JSON数据
    return jsonify(search_result)

# 接收前台传来的日志信息，进行添加的接口
@api_data_op_maintaininfo.route('/api/add_info',methods=['POST'])
def add_info():
    # 获取前台传来的数据
    data = request.get_data()
    # 将前台传来的数据转换为字典
    data_dict = json.loads(data)
    # 不用，前台传递的数据已经整理好了
    # # 假定new_data中的MaintenanceDate格式为 'yyyy-mm-ddTHH:MM:SS.sssZ'
    # # 需要转换为MySQL接受的格式 'yyyy-mm-dd HH:MM:SS'
    # # 首先移除毫秒和'Z'
    # formatted_date = data_dict['MaintenanceDate'].split('.')[0]
    # # 接着去除'T'
    # formatted_date = formatted_date.replace('T', ' ')
    # # 将格式化后的时间字符串赋值回new_data
    # data_dict['MaintenanceDate'] = formatted_date
    # 调用服务层的添加方法
    print("拿到的前台数据：",data_dict)
    repair_log_service.add_info(data_dict)
    # 返回JSON数据
    return jsonify({'msg':'success'})

# 接受前台请求，调用可视化分析结果函数，将这个日志信息结果返回给前台。
@api_data_op_maintaininfo.route('/api/create_logInfo',methods=['GET'])
def create_logInfo():
    # 调用综合性评判结果函数
    report_total = report_all()
    # 获取当前时间，并将其格式化为MySQL认可的格式
    # 问题在于你尝试从 datetime 模块直接调用 now() 方法，但在 datetime 模块里没有 now() 这个函数，它实际上是 datetime 类的一个方法。要正确地使用 now() 方法，你需要从 datetime 模块中导入 datetime 类
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # 编写本次日志信息，配合DeviceNode_MaintainInfo模型。report_total存储到MaintenanceRport
    log_info = {
        'MaintenanceDate': current_time,# 调用此函数的时间
        'MaintenanceRport':report_total,
        # 严格而言，这里的MaintenanceUser应该是从前台传递当前登录用户的用户名
        'MaintenanceUser':'yangzhi',
        'MaintenanceTage':'未处理',
    }
    # 将上述字典按照JSON返回
    return jsonify(log_info)
