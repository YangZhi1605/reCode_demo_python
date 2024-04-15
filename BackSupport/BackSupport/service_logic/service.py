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

    #配合SQLAlchemy的Device_Upload模型中的search_info类方法，实现根据传入的字符串进行模糊查询数据库信息的功能
    def search_info(self, search_str: str):
        return self.data_dao.search_info(search_str)

    # 配合SQLAlchemy的Device_Upload模型中的update_info，实现根据传入的指定id和新数据进行更新数据库信息的功能
    def update_info(self, id: int, new_data: dict):
        self.data_dao.update_info(id, new_data)



# 服务于后台管理修改电路分配权限占比的服务类
class Circuit_Weight_Service:
    def __init__(self, data_dao):
        self.data_dao = data_dao

    # 配合SQLAlchemy的Device_Circuit_Weight模型中的get_all类方法，实现获取所有数据的功能
    def get_all(self):
        return self.data_dao.get_all()

    # 配合SQLAlchemy的Device_Circuit_Weight模型中的update_info类方法，实现根据传入的指定id和新数据进行更新数据库信息的功能
    def update_info(self, id: int, new_data: dict):
        self.data_dao.update_info(id, new_data)

    # 配合SQLAlchemy的Device_Circuit_Weight模型中的delete_info类方法，实现根据int类型的id删除数据库信息的功能
    def delete_info(self, id: int):
        self.data_dao.delete_info(id)

    # 配合SQLAlchemy的Device_Circuit_Weight模型中的add_info类方法，实现根据传入的新数据添加数据库信息的功能
    # 在service层调用dao层的add_info类方法的写法看起来是正确的。我的service层方法会接收一个字典，然后将这个字典直接传递给dao层的add_info方法。
    def add_info(self, new_data: dict):
        self.data_dao.add_info(new_data)

    # 配合SQLAlchemy的Device_Circuit_Weight模型中的search_info类方法，实现根据传入的字符串进行模糊查询数据库信息的功能
    def search_info(self, search_str: str):
        return self.data_dao.search_info(search_str)

# 服务于前台维修日志管理的福利
class Repair_Log_Service:
    def __init__(self, data_dao):
        self.data_dao = data_dao

    # 配合SQLAlchemy的Device_Repair_Log模型中的get_all类方法，实现获取所有数据的功能
    def get_all(self):
        return self.data_dao.get_all()

    # 配合SQLAlchemy的Device_Repair_Log模型中的update_info类方法，实现根据传入的指定id和新数据进行更新数据库信息的功能
    def update_info(self, id: int, new_data: dict):
        self.data_dao.update_info(id, new_data)

    # 配合SQLAlchemy的Device_Repair_Log模型中的delete_info类方法，实现根据int类型的id删除数据库信息的功能
    def delete_info(self, id: int):
        self.data_dao.delete_info(id)

    # 配合SQLAlchemy的Device_Repair_Log模型中的add_info类方法，实现根据传入的新数据添加数据库信息的功能
    def add_info(self, new_data: dict):
        self.data_dao.add_info(new_data)

    # 配合SQLAlchemy的Device_Repair_Log模型中的search_info类方法，实现根据传入的字符串进行模糊查询数据库信息的功能
    def search_info(self, search_str: str):
        return self.data_dao.search_info(search_str)