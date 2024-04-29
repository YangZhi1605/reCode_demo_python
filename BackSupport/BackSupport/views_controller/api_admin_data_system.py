from flask import Blueprint,jsonify,request
from BackSupport.service_logic.service import Dynamic_Line_Service,User_Upload_Service,Circuit_Weight_Service
from BackSupport.model_logic.TotalModel import Device,Device_Upload,Device_Circuit_Weight
import os
import json

# 创建蓝图对象，此蓝图负责管理后台数据系统的路由
api_admin_data_system = Blueprint('api_admin_data_system', __name__)

# 将电路权限管理dao对象传入服务类
circuit_weight_service = Circuit_Weight_Service(Device_Circuit_Weight)

# 编写获取权限数据库所有数据的视图函数
@api_admin_data_system.route('/api/get_all_circuit_weight',methods=['GET'])
def get_all_circuit_weight():
    # 调用服务类方法获取数据
    results = circuit_weight_service.get_all()
    # 将获取的数据转换为字典，以便于返回
    results = [result.to_dict() for result in results]
    # 返回结果
    return jsonify(results)

# 编写获取前台传递的id和新数据，更新数据库信息的视图函数
@api_admin_data_system.route('/api/update_circuit_weight',methods=['POST'])
def update_circuit_weight():
    # 获取前台传递的id和新数据
    id = request.json.get('id')
    # 如何获取到前台传递的新数据？
    new_data = request.json.get('new_data')
    print(id,new_data)
    # 调用服务类方法更新数据库信息
    circuit_weight_service.update_info(id,new_data)
    # 返回结果
    return jsonify({'message':'update success'})

# 编写获得前台传递的添加对象的数据，添加到数据库的视图函数
@api_admin_data_system.route('/api/add_circuit_weight',methods=['POST'])
def add_circuit_weight():
    # 获取前台传递的新数据
    new_data = request.json.get('new_data')
    # 将new_data中的内容显示写成字典，其中，需要将字符串转换为浮点数
    # new_data中的内容有：AddForm:{
    #         RuleName:'',
    #         Circuit1:'',
    #         Circuit2:'',
    #         Circuit3:'',
    #         Circuit4:'',
    #         Circuit5:'',
    #         Circuit6:'',
    #         Circuit7:'',
    #         Circuit8:'',
    #         IsSet:'',
    #         EditTime:'',
    #         EditUser:'',
    #       },
    # 我自己定义IsSet为默认值为0，EditTime为当前时间，EditUser为当前用户
    new_data = {
        'RuleName':new_data.get('RuleName'),
        'Circuit1':float(new_data.get('Circuit1')),
        'Circuit2':float(new_data.get('Circuit2')),
        'Circuit3':float(new_data.get('Circuit3')),
        'Circuit4':float(new_data.get('Circuit4')),
        'Circuit5':float(new_data.get('Circuit5')),
        'Circuit6':float(new_data.get('Circuit6')),
        'Circuit7':float(new_data.get('Circuit7')),
        'Circuit8':float(new_data.get('Circuit8')),
        'IsSet':0,
        'EditTime':new_data.get('EditTime'),
        'EditUser':new_data.get('EditUser')
    }
    print('前台反馈的结果是：',new_data)
    # 调用model层的类方法添加数据，将字典new_data传递给add_info方法
    Device_Circuit_Weight.add_info(new_data)
    # 返回结果
    return jsonify({'message':'add success'})

# 编写获取前台传递的'规则名称'和'修改者名称'的参数，进行模糊查询数据库信息的视图函数
@api_admin_data_system.route('/api/search_circuit_weight',methods=['GET'])
def search_circuit_weight():
    # 获取前台传递的搜索字符串
    search_str = request.args.get('searchVal')
    print('前台传递的搜索字符串是：',search_str)
    # 调用服务类方法进行模糊查询
    results = circuit_weight_service.search_info(search_str)
    # 将获取的数据(数据库对象，我写了转换为字典的方法)转换为字典，以便于返回
    results = [result.to_dict() for result in results]
    # 返回结果
    return jsonify(results)

# 编写获取前台传递的id，删除数据库信息的视图函数
@api_admin_data_system.route('/api/delete_circuit_weight',methods=['POST'])
def delete_circuit_weight():
    # 获取前台传递的id
    id = request.json.get('id')
    # 调用服务类方法删除数据库信息
    circuit_weight_service.delete_info(id)
    # 返回结果
    return jsonify({'message':'delete success'})



