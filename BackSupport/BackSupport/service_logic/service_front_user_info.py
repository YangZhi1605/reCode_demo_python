
# 服务于前台用户信息的逻辑处理的服务类
class ServiceFrontUserInfo:
    # 构造函数
    def __init__(self, data_dao):
        # 创建数据访问对象
        self.dao = data_dao

    # 配合SQLAlchemy的FrontUserInfoTable模型中的get_all类方法，实现获取所有数据的功能
    def get_all(self):
        return self.dao.get_all()

    # 配合SQLAlchemy的FrontUserInfoTable模型中的delete_by_id类方法，实现根据id删除数据的功能
    def delete_info(self, id):
        return self.dao.delete_info(id)

    # 配合SQLAlchemy的FrontUserInfoTable模型中的search_info类方法，实现根据前台传递的条件查询数据的功能
    def search_info(self, condition):
        return self.dao.search_info(condition)

    # 配合SQLAlchemy的FrontUserInfoTable模型中的add_info类方法，实现添加用户信息的功能
    def add_info(self, data):
        return self.dao.add_info(data)

    # 配合SQLAlchemy的FrontUserInfoTable模型中的reset_password类方法，实现重置用户密码的功能
    def reset_password(self, id):
        return self.dao.reset_password(id)


