from flask import Blueprint,jsonify,request
from BackSupport.model_logic.TotalModel import ModelStorage
from BackSupport.service_logic.service_machine import ServiceMachine
from datetime import datetime
# 跨域
from flask_cors import CORS
# 创建服务对象，挂载dao模型
service_machine = ServiceMachine(ModelStorage)
# 创建蓝图
api_admin_machine_manage = Blueprint('api_admin_machine_manage', __name__)
# 解决跨域请求
CORS(api_admin_machine_manage)

# 编写获取所有模型信息的接口
@api_admin_machine_manage.route('/api/get_all_machine',methods=['GET'])
def get_all():
    # 获取所有模型信息
    model_list = service_machine.get_all()
    # 将获取的数据转换为字典，以便于返回
    models = [result.to_dict() for result in model_list]
    # 返回JSON数据,返回成功的信息

    return jsonify(models)


# 编写更新模型信息的接口
@api_admin_machine_manage.route('/api/update_machine',methods=['POST'])
def update_info():
    # 获取请求数据
    data = request.get_json()
    # 获取id
    id = data.get('id')
    # 获取新数据
    new_data = data.get('new_data')
    print("获得的是否启用",new_data.get('IsUse'))
    # 输入前台获得的JSON数据
    print("获得的新数据",new_data)
    # 从前端传来的JSON数据中得到字典信息
    new_data = {
        'ModelName':new_data.get('ModelName'),
        'CreateTime':new_data.get('CreateTime'),
        'ModelPath':new_data.get('ModelPath'),
        'CreateUser':new_data.get('CreateUser'),
        'IsUse':new_data.get('IsUse'),
    }
    # 更新模型信息
    service_machine.update_info(id,new_data)
    # 返回JSON数据
    return jsonify({'message':'success'})

# 编写删除模型信息的接口
@api_admin_machine_manage.route('/api/delete_machine',methods=['GET'])
def delete_info():
    # 获取请求数据
    id = request.args.get('id')
    # 将id转换为int类型
    id = int(id)
    # 删除模型信息
    service_machine.delete_info(id)
    # 返回JSON数据
    return jsonify({'message':'success'})