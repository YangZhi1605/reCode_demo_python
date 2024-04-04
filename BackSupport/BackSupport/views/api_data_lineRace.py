from flask import Blueprint, request, jsonify
import json

# 创建蓝图对象
api_data_lineRace = Blueprint('api_data_lineRace', __name__)

# 创建准备传递数据的接口函数
@api_data_lineRace.route('/lineRace', methods=['GET'])
def lineRace():
    # 到resuorce文件夹下找到life-expectancy-table.json文件
    with open('BackSupport/resource/data/life-expectancy-table.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 返回数据,以json格式传递给前端
    return jsonify(data)
