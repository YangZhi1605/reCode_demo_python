from flask import request, jsonify,Blueprint
from BackSupport.model_logic.TotalModel import DeviceNodeStore
from BackSupport.service_logic.service_node_store import ServiceNodeStore
from datetime import datetime
from email.utils import parsedate_to_datetime
# 跨域
from flask_cors import CORS
# 创建服务对象，挂载dao模型
service_node_store = ServiceNodeStore(DeviceNodeStore)
# 创建蓝图
api_admin_node_store_manage = Blueprint('api_admin_node_store_manage', __name__)
# 解决跨域请求
CORS(api_admin_node_store_manage)

# 编写获取所有数据的接口
@api_admin_node_store_manage.route('/api/get_all_node_store',methods=['GET'])
def get_all_node_store():
    '''
        获取所有数据
    Returns:
    '''
    # 调用service_node_store的get_all方法，获取所有数据
    results = service_node_store.get_all()
    # 对象转换为字典
    results = [result.to_dict() for result in results]

    # 返回JSON数据
    return jsonify(results)


# 编写添加数据的接口
@api_admin_node_store_manage.route('/api/add_node_store',methods=['POST'])
def add_node_store():
    '''
        添加数据
    Returns:
    '''
    # 获取请求的数据
    data = request.json
    print('data:',data)
    # 将价格转换为浮点数,保留两位小数
    data['price'] = round(float(data['price']), 2)
    # 将库存转换为整数
    data['number'] = int(data['number'])
    # 将'editTime': '2024-05-03T10:08:39.000Z'转换为'editTime': '2024-05-03 10:08:39'
    data['editTime'] = data['editTime'].replace('T', ' ').replace('.000Z', '')

    # 调用service_node_store的add_info方法，添加数据
    result = service_node_store.add_info(data)
    # 返回JSON数据
    return jsonify(result)




# 转换前端传递的RFC 5322日期格式
def convert_rfc5322_date_str(date_str):
    dt = parsedate_to_datetime(date_str)
    return dt.strftime('%Y-%m-%d %H:%M:%S')

# 编写根据id获取数据的接口
@api_admin_node_store_manage.route('/api/update_node_store',methods=['POST'])
def update_node_store():
    '''
        根据id获取数据
    Returns:
    '''
    # 获取请求的数据
    data = request.json
    print(data)
    id = int(data['id'])
    # 将价格转换为浮点数,保留两位小数
    data['price'] = round(float(data['price']), 2)
    # 将库存转换为整数
    data['number'] = int(data['number'])
    # 将'editTime': '2024-05-03T10:08:39.000Z'转换为'editTime': '2024-05-03 10:08:39'
    data['editTime'] = convert_rfc5322_date_str(data['editTime'])

    # 调用service_node_store的update_info方法，根据id获取数据
    result = service_node_store.update_info(id, data)
    # 返回JSON数据
    return jsonify(result)

# 编写根据id删除数据的接口，get请求
@api_admin_node_store_manage.route('/api/delete_node_store',methods=['GET'])
def delete_node_store():
    '''
        根据id删除数据
    Returns:
    '''
    # 获取请求的数据
    id = int(request.args.get('id'))
    # 调用service_node_store的delete_info方法，根据id删除数据
    result = service_node_store.delete_info(id)
    # 返回JSON数据
    return jsonify(result)

# 编写根据条件查询数据的接口
@api_admin_node_store_manage.route('/api/search_node_store',methods=['POST'])
def search_node_store():
    '''
        根据条件查询数据
    Returns:
    '''
    # 获取请求的数据
    data = request.json
    print(data) # {'params': {'searchVal': '轮胎'}}
    paramss = data['params']
    searchVal = paramss['searchVal']
    # 调用service_node_store的search_info方法，根据条件查询数据
    results = service_node_store.search_info(searchVal)
    # 对象转换为字典
    results = [result.to_dict() for result in results]
    # 返回JSON数据
    return jsonify(results)

# 编写根据id获取数据的接口
@api_admin_node_store_manage.route('/api/get_info_by_id',methods=['GET'])
def get_info_by_id():
    '''
        根据id获取数据
    Returns:
    '''
    # 获取请求的数据
    id = int(request.args.get('id'))
    # 调用service_node_store的get_info_by_id方法，根据id获取数据
    result = service_node_store.get_info_by_id(id)
    # 对象转换为字典
    # result = result.to_dict()
    # 返回JSON数据
    return jsonify(result)