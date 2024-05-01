from datetime import datetime

from flask import Blueprint, jsonify, request
from BackSupport.model_logic.TotalModel import FrontUserInfoTable
from BackSupport.service_logic.service_front_user_info import ServiceFrontUserInfo
from ..utils.email_utils import send_mail
import time
import json
# 跨域请求
from flask_cors import CORS
# 创建服务对象，挂载dao模型
service_front_user_info = ServiceFrontUserInfo(FrontUserInfoTable)
# 创建蓝图
api_data_op_userinfo_manage = Blueprint('api_data_op_userinfo_manage', __name__)
# 解决跨域请求
CORS(api_data_op_userinfo_manage)

# 编写获取所有前台用户信息的接口
@api_data_op_userinfo_manage.route('/api/get_all_front_user_info', methods=['GET'])
def get_all_front_user_info():
    '''
        获取所有前台用户信息
    Returns:
    '''
    # 获取所有前台用户信息
    results = service_front_user_info.get_all()
    # 创建一个空列表
    data = []
    # 遍历所有结果
    for result in results:
        # 将结果转换为字典
        result = result.to_dict()
        # 将字典添加到列表中
        data.append(result)
    # 返回JSON数据
    return jsonify(data)

# 根据前台传递的id删除前台用户信息的接口
@api_data_op_userinfo_manage.route('/api/delete_front_user_info', methods=['POST'])
def delete_front_user_info():
    '''
        根据前台传递的id删除前台用户信息
    Returns:
    '''
    # 获取前台传递的id
    id = request.json.get('id_info')
    email = request.json.get('email_info')
    reason = request.json.get('reason')
    print('email为：', email)
    # 将id转换为int类型
    id = int(id)
    # 删除前台用户信息
    result = service_front_user_info.delete_info(id)
    print('删除的信息', result)

    # 如果删除成功并且提供了邮箱，则发送邮件通知用户
    if result['success'] and email:
        subject = "账号删除通知"
        body = f"您的账号已经被删除。\n删除原因: {reason}\n删除时间: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))}"
        # 调用utils文件夹下的email_utils.py文件中的send_mail方法发送邮件
        send_mail(subject, body, [email])
    # 返回删除成功获取失败的信息

    return jsonify(result)


# 根据前台传递的用户名或者电话号码查询前台用户信息的接口
@api_data_op_userinfo_manage.route('/api/search_front_user_info', methods=['POST'])
def search_front_user_info():
    '''
        根据前台传递的用户名或者电话号码查询前台用户信息
    Returns:
    '''
    # 获取前台传递的条件
    condition = request.json.get('condition')
    # 查询前台用户信息
    results = service_front_user_info.search_info(condition)
    # 创建一个空列表
    data = []
    # 遍历所有结果
    for result in results:
        # 将结果转换为字典
        result = result.to_dict()
        # 将字典添加到列表中
        data.append(result)
    # 返回JSON数据
    return jsonify(data)

# 添加前台用户信息的接口
@api_data_op_userinfo_manage.route('/api/add_front_user_info', methods=['POST'])
def add_front_user_info():
    '''
        添加前台用户信息
    Returns:
    '''
    # 获取前台传递的数据
    data = request.json
    # 在服务器端生成当前时间戳
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data['editTime'] = current_time
    result = service_front_user_info.add_info(data)
    # 返回添加成功或者失败的信息
    if result['success'] and data['email']:
        subject = "账号添加通知"
        body = (f"您的账号已经被添加。\n"
                f"添加时间: {current_time}\n"
                f"添加信息: {json.dumps(data, ensure_ascii=False)}")
        # 调用发送邮件的方法
        send_mail(subject, body, [data['email']])
    return jsonify(result)


# 重置前台用户密码的接口，发送邮件通知用户账户和密码
@api_data_op_userinfo_manage.route('/api/reset_front_user_password', methods=['POST'])
def reset_front_user_password():
    '''
        重置前台用户密码
    Returns:
    '''
    # 获取前台传递的id
    id = request.json.get('id_info')
    email = request.json.get('email_info')
    # 将id转换为int类型
    id = int(id)
    # 重置前台用户密码
    result = service_front_user_info.reset_password(id)
    # 返回重置成功或者失败的信息
    if result['success'] and email:
        subject = "账号密码重置通知"
        body = (f"您的账号密码已经被重置。\n"
                f"重置时间: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))}\n"
                f"新密码: {123456}")
        # 调用发送邮件的方法
        send_mail(subject, body, [email])
    return jsonify(result)
