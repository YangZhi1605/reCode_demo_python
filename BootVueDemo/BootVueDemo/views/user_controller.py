from flask import Blueprint,jsonify,request
from BootVueDemo.business_logic.UserService import UserService
from BootVueDemo.utils.models import User,db
# 导入解决跨域请求
from flask_cors import CORS
# 创建蓝图
user_controller = Blueprint('user_controller', __name__)
# 解决跨域请求
CORS(user_controller)
# 创建UserService对象
userService = UserService(User)

# 查询所有用户的路由
@user_controller.route('/findAll',methods=['GET'])
def def_find_all():
    # 直接调用UserService对象的find_all方法，其背后运用User模型的find_all的API
    users = userService.find_all()
    # 将查询到的用户数据转换成字典列表并返回JSON
    # users 列表中的数据已经是字典格式，所以你可以直接将其转换为 JSON 格式并返回。
    # 打印model对象
    # print(users)
    # 打印字典对象，以列表形式
    # print([user.to_dict() for user in users])
    response = jsonify([user.to_dict() for user in users])
    # print(response.get_json())
    return jsonify([user.to_dict() for user in users])


# 编写保存用户信息的路由，并处理异常
#
#
# @user_controller.route('/save', methods=['POST'])
# def save_user():
#     data = request.get_json()
#     name = data.get('name')
#     age = int(data.get('age'))  # 将 'age' 字段转换为整数
#     salary = float(data.get('salary'))  # 将 'salary' 字段转换为浮点数
#     phoneCode = data.get('phoneCode')
#
#     user = User(name=name, age=age, salary=salary, phoneCode=phoneCode)
#     # User.save(user)
#     userService.save(user)  # 使用 userService 的 save 方法
#
#     return {'message': '用户保存成功！', 'success': True}

@user_controller.route('/save', methods=['POST'])
def save_user():
    # tag:数据保存到数据库成功。需要了关于SQLAlchemy的自增长，以及数据表创建时候相配合的操作
    try:
        data = request.get_json()
        name = data.get('name')
        age = int(data.get('age'))  # 将 'age' 字段转换为整数
        salary = float(data.get('salary'))  # 将 'salary' 字段转换为浮点数
        phoneCode = data.get('phoneCode')

        user = User(name=name, age=age, salary=salary, phoneCode=phoneCode)
        userService.save(user)  # 使用 userService 的 save 方法

        return {'message': '用户保存成功！', 'success': True}
    except Exception as e:
        # 打印异常信息，方便调试
        print(e)
        return {'message': '保存用户失败', 'success': False}

# 编写根据id删除用户的路由，并处理异常
@user_controller.route('/deleteInfo', methods=['GET'])
def delete_user():
    try:
        # 获取请求参数中的id
        id = int(request.args.get('id'))
        userService.delete(id)  # 使用 userService 的 delete 方法
        return {'message': '用户删除成功', 'success': True}
    except Exception as e:
        # 打印异常信息，方便调试
        print(e)
        return {'message': '删除用户失败', 'success': False}

# 根据id查询一个用户的路由，并处理异常，返回JSON格式的数据
@user_controller.route('/findOne', methods=['GET'])
def find_one():
    try:
        # 获取请求参数中的id
        id = int(request.args.get('id'))
        user = userService.find_one(id)  # 使用 userService 的 find_one 方法
        return jsonify(user.to_dict())
    except Exception as e:
        # 打印异常信息，方便调试
        print(e)
        return {'message': '查询用户失败', 'success': False}

# 更新用户信息的路由，并处理异常
@user_controller.route('/updateInfo', methods=['POST'])
def update_user():
    try:
        # 获取请求参数中json
        data = request.get_json()
        id = int(data.get('id'))
        name = data.get('name')
        age = int(data.get('age'))  # 将 'age' 字段转换为整数
        salary = float(data.get('salary'))  # 将 'salary' 字段转换为浮点数
        phoneCode = data.get('phoneCode')

        user = User(id=id, name=name, age=age, salary=salary, phoneCode=phoneCode)
        userService.update(user)  # 使用 userService 的 update 方法

        return {'message': '用户更新成功', 'success': True}
    except Exception as e:
        # 打印异常信息，方便调试
        print(e)
        return {'message': '更新用户失败', 'success': False}

# 根据name或者phoneCode进行模糊查询所有用户的路由，并处理异常，返回JSON格式的数据
@user_controller.route('/findByNameOrPhone', methods=['GET'])
def find_by_name_or_phone():
    try:
        # 获取请求参数中的name和phoneCode
        name = request.args.get('name')
        # 如果没有传递name参数，就使用空字符串
        name = name or ' '
        print('name=',name)
        phoneCode = request.args.get('phoneCode') or ' '
        users = userService.find_by_name_or_phone(name, phoneCode)  # 使用 userService 的 find_by_name_or_phone 方法
        return jsonify([user.to_dict() for user in users])
    except Exception as e:
        # 打印异常信息，方便调试
        print(e)
        return {'message': '查询用户失败', 'success': False}