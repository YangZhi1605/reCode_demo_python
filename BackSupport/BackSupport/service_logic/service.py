# 服务层，读取数据库中需要的数据信息并整理返回，controller层可以直接调用从而得到结果，以JSON的形式反馈给前端。
from BackSupport.model_logic import VoltageModel
from BackSupport.model_logic.VoltageModel import Device,Device_Upload
from flask import jsonify
import os
import json

# 服务于动态折线图的服务类
class Dynamic_Line_Service:
    # 将获得的数据，处理为动态折线图所需的格式
    def get_dict_line_data(self):
        # 使用get_odd_voltages类方法获取数据
        voltages = Device.get_odd_voltages()
        # 调用model层中写好的格式化函数
        formatted_voltages_dict = Device.format_voltages(voltages)
        # 返回结果
        return formatted_voltages_dict

    # 将结果存储为JSON文件
    def save_json_to_resource(self, data, filename='line_data.json', folder='resource/data'):
        # 检查目标文件夹是否存在，如果不存在则创建
        os.makedirs(folder, exist_ok=True)
        # 文件路径
        file_path = os.path.join(folder, filename)
        # 写入JSON数据
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file)


# 服务于用户上传个人数据后，所形成数据表格的数据交互服务类
class User_Upload_Service:
    def __init__(self, data_dao):
        self.data_dao = data_dao

    # 配合SQLAlchemy的Device_Upload模型中的delete_info类方法，实现根据int类型的id删除数据库信息的功能
    def delete_info(self, id: int):
        self.data_dao.delete_info(id)




