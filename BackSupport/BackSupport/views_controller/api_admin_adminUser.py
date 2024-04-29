from flask import request, jsonify,Blueprint
from BackSupport.model_logic.TotalModel import AdminInfoTable
from BackSupport.service_logic.service_machine import ServiceAdmin
from flask_cors import CORS
from ..utils.token_util import generate_token
# 创建一个蓝图对象，蓝图对象用于管理路由
api_admin_adminUser = Blueprint('api_admin_adminUser', __name__)
# 创建一个ServiceAdmin对象
service_admin = ServiceAdmin(AdminInfoTable)
# 解决跨域请求
CORS(api_admin_adminUser)

# 创建根据传入的用户名和密码判断是否存在该用户的路由
@api_admin_adminUser.route('/api/is_exist', methods=['POST'])
def is_exist():
    # 获取传入的json数据
    data = request.get_json()
    # 判断是否存在该用户
    result = service_admin.is_exist(data['username'], data['password'])

    # 准备根据用户名生成token
    token = generate_token(data['username'])
    if result is not None:
        # 如果用户存在，返回成功的状态码和token
        return jsonify({
            'success': True,
            'message': '登录成功',
            'data': {
                'token': token,
                # 其他需要传递给前端的用户信息
            }
        }), 200
    else:
        # 如果用户不存在，返回错误的状态码和消息
        return jsonify({
            'success': False,
            'message': '用户名或密码错误'
        }), 401  # 或者其他的适当 HTTP 状态码

# 创建添加用户的路由，处理添加成功和失败的情况
@api_admin_adminUser.route('/api/add_user_info', methods=['POST'])
def add_info():
    # 获取传入的json数据
    data = request.get_json()
    # 添加用户
    service_admin.add_info(data)
    return jsonify({
        'success': True,
        'message': '添加成功'
    }), 200

