# 编写一个服务类，用于维护电动汽车的零件信息
class ServiceNodeStore:
    # 初始化方法，传入数据访问对象
    def __init__(self, data_dao):
        self.data_dao = data_dao

    # 配合SQLAlchemy的DeviceNodeStore模型中的get_all类方法，实现获取所有数据的功能
    def get_all(self):
        return self.data_dao.get_all()

    # 配合SQLAlchemy的DeviceNodeStore模型中的add_info类方法，实现添加数据的功能
    def add_info(self, data):
        return self.data_dao.add_info(data)

    # 配合SQLAlchemy的DeviceNodeStore模型中的update_info类方法，实现根据id获取数据的功能
    def update_info(self, id, data):
        return self.data_dao.update_info(id, data)

    # 配合SQLAlchemy的DeviceNodeStore模型中的delete_info类方法，实现根据id删除数据的功能
    def delete_info(self, id):
        return self.data_dao.delete_info(id)

    # 配合SQLAlchemy的DeviceNodeStore模型中的search_info类方法，实现根据条件查询数据的功能
    def search_info(self, data):
        return self.data_dao.search_info(data)
