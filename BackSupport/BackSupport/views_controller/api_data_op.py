from flask import Blueprint, request, jsonify
import json
from flask import send_file
import os
from werkzeug.utils import secure_filename
import pandas as pd
from ..utils import sqlhelper,dbutils
import time,datetime
from BackSupport.service_logic.service import Dynamic_Line_Service
from BackSupport.utils.dbutils import read_data_from_database
# 导入dao模型
from BackSupport.model_logic.VoltageModel import Device, Device_Upload
from BackSupport.service_logic.service import User_Upload_Service
# 解决跨域请求
from flask_cors import CORS



# 创建蓝图对象
api_data_op = Blueprint('api_data_op', __name__)
# 加载跨域请求
CORS(api_data_op)
# 创建service服务类的对象，将dao模型传入
data_upload_service = User_Upload_Service(Device_Upload)

# 定义本地计算机（即服务器中）模板文件的路径
path_to_excel = 'E:/develops/resource/devicedownload.xlsx'

# 创建准备传递动态折现图数据的接口函数——最初测试版本
@api_data_op.route('/api/lineRace', methods=['GET'])
def lineRace():
    # 到resuorce文件夹下找到life-expectancy-table.json文件
    with open('BackSupport/resource/data/life-expectancy-table.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 返回数据,以json格式传递给前端
    return jsonify(data)

# 首页——创建贴合用户的电动汽车数据的动态折线图api接口
@api_data_op.route('/api/lineData',methods=['GET'])
def get_dynamic_line_data():
    service = Dynamic_Line_Service()
    result = service.get_dict_line_data()
    return jsonify(result)

# 工作台2——创建AQI数据接口函数
@api_data_op.route('/api/graphLine', methods=['GET'])
def graphLine():
    # 到resuorce文件夹下找到life-expectancy-table.json文件
    with open('BackSupport/resource/data/aqi-beijing.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 返回数据,以json格式传递给前端
    return jsonify(data)

# 辅助函数——检查文件是否存在
def def_check():
    # 检查文件是否存在
    file_exists = os.path.exists(path_to_excel)
    is_exist = False
    # 输出检查结果
    if file_exists:
        result = f'File path is correct. File exists: {path_to_excel}'
        is_exist = True
    else:
        result = 'File path is incorrect or file does not exist.'
        is_exist = False

    print(result)
    return is_exist

# 工作台1——创建下载excel模板的接口函数
@api_data_op.route('/api/downloadExcel', methods=['GET'])
def download_template():
    # 假设您的文件位于服务器的指定路径
    # path_to_excel = 'E:/develops/resource/devicedownload.xls'
    # 如果文件存在，则返回文件
    if def_check():
        return send_file(path_to_excel, as_attachment=True)
    else:
        return 'File path is incorrect or file does not exist.'


# 工作台1——创建上传excel文件并持久化到数据库的接口函数
@api_data_op.route('/api/uploadExcel', methods=['POST'])
def upload_excel():
    print('接收到上传请求')
    # 获取当前脚本的绝对路径
    current_file_path = os.path.abspath(__file__)
    # 获取 'BackSupport/views_controller' 目录的路径
    views_controller_dir = os.path.dirname(current_file_path)
    # 获取 'BackSupport' 目录的路径
    back_support_dir = os.path.dirname(views_controller_dir)
    # 设置 'BackSupport/resource/front_data_analysis' 为目标文件夹# 目前看到，只能一层一层的join
    resource_dir = os.path.join(back_support_dir, 'resource')
    target_folder = os.path.join(resource_dir, 'front_data_analysis')

    # 确保目标文件夹存在，如果不存在，则创建
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
        print('目标文件夹不存在，已创建:', target_folder)

    uploaded_file = request.files['file']
    if uploaded_file:
        filename = secure_filename(uploaded_file.filename)
        file_path = os.path.join(target_folder, filename)
        try:
            # 保存文件 + 存入数据库 的方法调用
            uploaded_file.save(file_path)
            print('文件保存成功:', file_path)
            # 保存文件到数据库
            excel_file_path = file_path
            # 假设希望将Excel文件的数据存储到名为"your_table_name"的数据表中
            database_table_name = "device_upload"
            dbutils.save_excel_to_database(excel_file_path, database_table_name)

            return '文件成功上传并存入数据库', 200
        except Exception as e:
            print('处理文件或是数据库操作时出错:', str(e))
            return '处理文件或是数据库操作时出错', 500
    else:
        print('没有接收到文件')
        return 'No file uploaded', 400

# 工作台1——删除指定文件的逻辑
@api_data_op.route('/api/deleteExcel', methods=['POST'])
def delete_excel():
    # 获取前端发送的要删除的文件名
    data = request.json
    filename = data.get('filename')
    if filename:
        # 以下部分代码用于定位文件存储位置，与您之前提供的代码相同
        current_file_path = os.path.abspath(__file__)
        views_controller_dir = os.path.dirname(current_file_path)
        back_support_dir = os.path.dirname(views_controller_dir)
        resource_dir = os.path.join(back_support_dir, 'resource')
        target_folder = os.path.join(resource_dir, 'front_data_analysis')

        # 安全的获取文件名
        filename = secure_filename(filename)
        file_path = os.path.join(target_folder, filename)

        # 删除文件
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                print('文件删除成功:', file_path)
                return 'File deleted successfully', 200
            else:
                print('文件不存在:', file_path)
                return 'File does not exist', 404
        except Exception as e:
            print('删除文件时出错:', str(e))
            return 'Error deleting file', 500
    else:
        print('无法获取文件名')
        return 'No filename provided', 400

# 工作台1——对上传的Excel文件进行整理的逻辑
@api_data_op.route('/api/organizeExcel', methods=['POST'])
def organize_excel():
    print("接收到整理请求")
    # 获取前端发送的要整理的文件名
    data = request.json
    filename = data.get('filename')
    print(filename)
    if filename:
        # 定位文件存储位置的代码与之前相同
        # 获取当前脚本的绝对路径
        current_file_path = os.path.abspath(__file__)
        # 获取 'BackSupport/views_controller' 目录的路径
        views_controller_dir = os.path.dirname(current_file_path)
        # 获取 'BackSupport' 目录的路径
        back_support_dir = os.path.dirname(views_controller_dir)

        # 设置 'BackSupport/resource/front_data_analysis' 为目标文件夹
        # 目前看到，只能一层一层的join
        resource_dir = os.path.join(back_support_dir, 'resource')
        target_folder = os.path.join(resource_dir, 'front_data_analysis')

        filename = secure_filename(filename)
        file_path = os.path.join(target_folder, filename)

        if os.path.exists(file_path):
            try:
                # Specify `engine='openpyxl'` for xlsx files
                df = pd.read_excel(file_path, engine='openpyxl')
                # Your data processing logic goes here
                # df.fillna(方法或值)
                # When saving, also specify `engine='openpyxl'` for xlsx files
                df.to_excel(file_path, index=False, engine='openpyxl')
                return 'File organized successfully', 200
            except Exception as e:
                print('整理文件时出错:', str(e))
                return 'Error organizing file', 500
        else:
            return 'File does not exist', 404


# 工作台1——传递后端数据库中数据表到前台进行表格展示
@api_data_op.route('/api/getDB_data', methods=['GET'])
def get_data():
    # 调用函数读取存储进去的数据库中的数据，返回给前台展示其中的信息
    data_list = read_data_from_database('device_upload')
    # 因为原始数据中包含了 datetime.datetime 对象，
    # 使用 jsonify 之前需要先将这些对象转换成字符串格式，
    # 因为 JSON 标准不直接支持 datetime 对象。
    for data in data_list:
        if isinstance(data['CollectTime'], datetime.datetime):
            data['CollectTime'] = data[
                'CollectTime'].isoformat()  # 输出的日期时间格式是 "YYYY-MM-DDTHH:MM:SS" 形式的 ISO 标准字符串

    return jsonify(data_list)

# 根据前台请求，传入的id参数，到数据库中删除对应的数据
@api_data_op.route('/api/deleteData', methods=['GET'])
def delete_item():
    print('进入id删除函数了')
    # 运用service层写好的根据id删除的方法进行删除.上述中，将dao传入service模型中，即完成了service层的实例化和对dao层的挂载
    try:
        # 通过查询字符串获取 item_id
        item_id = int(request.args.get('id', type=int))
        print('item_id:', item_id)

        if item_id is None:
            return jsonify({'message': 'ID parameter is required'}), 400
        # 调用service层的方法
        data_upload_service.delete_info(item_id)
        # 如果没有异常被抛出，则认为删除成功
        return jsonify({'message': 'Data deleted successfully', 'id': item_id}), 200
    except Exception as e:
        # 发生任何异常时返回错误信息和500内部服务器错误状态码
        return jsonify({'message': 'Deletion failed', 'error': str(e)}), 500


# 根据前台传入的参数，到数据库中进行模糊查询
@api_data_op.route('/api/searchData', methods=['GET'])
def search_data():
    # 获取查询字符串，在前端代码中，您使用了 'query' 作为键来传递搜索字符串
    search_str = request.args.get('query')
    print('获取的前台参数：',search_str)
    # 调用service层的方法
    results = data_upload_service.search_info(search_str)
    print('查询结果:', results) # 此时的结果不是一个字典，无法JSON序列化。。查询结果: [<Device(ID=27, DeviceName=电池, UserID=1001, CollectTime=2019-03-13 21:15:41)>, <Device(ID=28, DeviceName=电池, UserID=1001, CollectTime=2019-03-13 21:15:41)>, <Device(ID=29, DeviceName=电池, UserID=1001, CollectTime=2019-03-13 21:15:41)>]
    # 将查询结果转换为字典列表以便JSON序列化
    json_results = [
        {
            'ID': result.ID,
            'DeviceNodeID': result.DeviceNodeID,
            'DeviceName': result.DeviceName,
            'UserID': result.UserID,
            'CollectTime': result.CollectTime.strftime('%Y-%m-%d %H:%M:%S') if result.CollectTime else None,
            'Voltage1':result.Voltage1,
            'Voltage2':result.Voltage2,
            'Voltage3':result.Voltage3,
            'Voltage4':result.Voltage4,
            'Voltage5':result.Voltage5,
            'Voltage6':result.Voltage6,
            'Voltage7':result.Voltage7,
            'Voltage8':result.Voltage8,
            'Voltage9':result.Voltage9,
            'Voltage10':result.Voltage10,
            'Voltage11':result.Voltage11,
            'Voltage12':result.Voltage12,
            'Voltage13':result.Voltage13,
            'Voltage14':result.Voltage14,
            'Voltage15':result.Voltage15,
            'Voltage16':result.Voltage16,
        } for result in results
    ]
    return jsonify(json_results)

# 根据传入的指定id和新数据进行更新数据库信息的接口
@api_data_op.route('/api/edit_info', methods=['POST'])
def update_data():
    # 获取请求中的json数据
    data = request.get_json()
    # 获取id
    id = data.get('Row_id')
    # 获取新的数据
    rowData = data.get('editData')
    # 获取新数据
    new_data = {
        'DeviceNodeID': rowData.get('DeviceNodeID'),
        'DeviceName': rowData.get('DeviceName'),
        'UserID': rowData.get('UserID'),
        'CollectTime': rowData.get('CollectTime'),
        'Voltage1': rowData.get('Voltage1'),
        'Voltage2': rowData.get('Voltage2'),
        'Voltage3': rowData.get('Voltage3'),
        'Voltage4': rowData.get('Voltage4'),
        'Voltage5': rowData.get('Voltage5'),
        'Voltage6': rowData.get('Voltage6'),
        'Voltage7': rowData.get('Voltage7'),
        'Voltage8': rowData.get('Voltage8'),
        'Voltage9': rowData.get('Voltage9'),
        'Voltage10': rowData.get('Voltage10'),
        'Voltage11': rowData.get('Voltage11'),
        'Voltage12': rowData.get('Voltage12'),
        'Voltage13': rowData.get('Voltage13'),
        'Voltage14': rowData.get('Voltage14'),
        'Voltage15': rowData.get('Voltage15'),
        'Voltage16': rowData.get('Voltage16'),
    }
    # 调用service层的方法
    data_upload_service.update_info(id, new_data)
    return jsonify({'message': 'Data updated successfully', 'id': id}), 200