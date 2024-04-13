from flask import Blueprint,jsonify,request
import json

# 导入解决跨域请求
from flask_cors import CORS
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
