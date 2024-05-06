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

    # 配合SQLAlchemy的Cart模型中的deleteCartItems类方法，实现删除传递过来的购物车中的商品信息的功能
    def deactivateCartItems(self,data):
        return self.dao.deactivateCartItems(data)

# 编写一个服务类，用于维护购物车的收货地址信息
class ServiceFrontAddress:
    def __init__(self,data_dao):
        self.dao = data_dao

    # 配合SQLAlchemy的Address模型中的get_all类方法，实现获取所有数据的功能
    def get_all(self):
        return self.dao.get_all()
    # 配合SQLAlchemy的Address模型中的add_info类方法，实现添加收货地址信息的功能
    def add_info(self,data):
        return self.dao.add_info(data)
    # 配合SQLAlchemy的Address模型中的update_info类方法，实现更新收货地址信息的功能
    def update_info(self,id,data):
        return self.dao.update_info(id,data)
    # 配合SQLAlchemy的Address模型中的delete_info类方法，实现删除收货地址信息的功能
    def delete_info(self,id):
        return self.dao.delete_info(id)
    # 配合SQLAlchemy的Address模型中的update_isUse类方法，实现根据id更新收货地址的选中状态的功能
    def update_isUse(self,id,data):
        return self.dao.update_isUse(id,data)

# 编写一个服务类，用于维护订单信息
class ServiceFrontOrder:
    def __init__(self,data_dao):
        self.dao = data_dao

    # 配合SQLAlchemy的Order模型中的get_all类方法，实现获取所有数据的功能
    def get_all(self):
        return self.dao.get_all()
    # 配合SQLAlchemy的Order模型中的add_info类方法，实现添加订单信息的功能
    def add_info(self,data):
        return self.dao.add_info(data)
    # 配合SQLAlchemy的Order模型中的update_info类方法，实现更新订单信息的功能
    def update_info(self,id,data):
        return self.dao.update_info(id,data)
    # 配合SQLAlchemy的Order模型中的delete_info类方法，实现删除订单信息的功能
    def delete_info(self,id):
        return self.dao.delete_info(id)
    # 配合SQLAlchemy的Order模型中的createOrder类方法，实现根据用户id、收货地址id、商品信息id创建订单的功能
    def createOrder(self,data):
        return self.dao.createOrder(data)
    # 配合SQLAlchemy的Order模型中的get_all_orders_details类方法，实现根据id获得每笔订单的详细信息
    def get_all_orders_details(self):
        return self.dao.get_all_orders_details()
