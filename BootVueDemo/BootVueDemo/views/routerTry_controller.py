from flask import  request, jsonify, Blueprint
# 解决跨域请求
from flask_cors import CORS

# 声明蓝图
routerTry_controller = Blueprint('routerTry_controller', __name__)
# 解决跨域请求
CORS(routerTry_controller)

# 查询所有用户的路由，按照json的格式返回，自定义假数据，数据中有ID，姓名，年龄，生日
@routerTry_controller.route('/findInfoRouter',methods=['GET'])
def def_find():
    users = [
        {
            'id': 1,
            'name': '张三',
            'age': 18,
            'birthday': '2000-01-01'
        },
        {
            'id': 2,
            'name': '李四',
            'age': 19,
            'birthday': '2001-01-01'
        },
        {
            'id': 3,
            'name': '王五',
            'age': 20,
            'birthday': '2002-01-01'
        }
    ]
    return jsonify(users)
