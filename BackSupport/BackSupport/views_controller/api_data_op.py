from flask import Blueprint, request, jsonify
import json
from flask import send_file
import os
from werkzeug.utils import secure_filename


# 创建蓝图对象
api_data_op = Blueprint('api_data_op', __name__)
# 定义本地计算机（即服务器中）模板文件的路径
path_to_excel = 'E:/develops/resource/devicedownload.xls'

# 创建准备传递动态折现图数据的接口函数
@api_data_op.route('/api/lineRace', methods=['GET'])
def lineRace():
    # 到resuorce文件夹下找到life-expectancy-table.json文件
    with open('BackSupport/resource/data/life-expectancy-table.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 返回数据,以json格式传递给前端
    return jsonify(data)

# 检查文件是否存在
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

# 创建传递excel模板的接口函数
@api_data_op.route('/api/downloadExcel', methods=['GET'])
def download_template():
    # 假设您的文件位于服务器的指定路径
    # path_to_excel = 'E:/develops/resource/devicedownload.xls'
    # 如果文件存在，则返回文件
    if def_check():
        return send_file(path_to_excel, as_attachment=True)
    else:
        return 'File path is incorrect or file does not exist.'


# 创建上传excel文件的接口函数
@api_data_op.route('/api/uploadExcel', methods=['POST'])
def upload_excel():
    print('接收到上传请求')
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

    # 确保目标文件夹存在，如果不存在，则创建
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
        print('目标文件夹不存在，已创建:', target_folder)

    uploaded_file = request.files['file']
    if uploaded_file:
        filename = secure_filename(uploaded_file.filename)
        file_path = os.path.join(target_folder, filename)
        try:
            uploaded_file.save(file_path)
            print('文件保存成功:', file_path)
        except Exception as e:
            print('保存文件时出错:', str(e))
            return 'Error saving file', 500
        return 'File uploaded successfully', 200
    else:
        print('没有接收到文件')
        return 'No file uploaded', 400

# 删除指定文件的逻辑
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