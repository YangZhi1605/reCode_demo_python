# 用于维护购物车的服务类
class ServiceFrontCart:
    def __init__(self,data_dao):
        self.dao = data_dao

    # 配合SQLAlchemy的Cart模型中的get_all类方法，实现获取所有数据的功能
    def get_all(self):
        return self.dao.get_all()
    # 配合SQLAlchemy的Cart模型中的add_info类方法，实现添加购物车信息的功能
    def add_info(self,data):
        return self.dao.add_info(data)
    # 配合SQLAlchemy的Cart模型中的update_info类方法，实现删除购物车信息的功能
    def update_info(self,id,data):
        return self.dao.update_info(id,data)
    # 配合SQLAlchemy的Cart模型中的update_selected_status类方法，实现更新购物车商品选中状态的功能
    def update_selected_status(self,items_dict):
        return self.dao.update_selected_status(items_dict)
    # 配合SQLAlchemy的Cart模型中的delete_info类方法，实现删除购物车信息的功能
    def delete_info(self,id):
        return self.dao.delete_info(id)
