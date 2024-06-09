
# 服务于机器学习模型管理的服务类
class ServiceMachine:
    def __init__(self, data_dao):
        self.data_dao = data_dao

   # 配合SQLAlchemy的ModelStorage模型中的get_all类方法，实现获取所有数据的功能
    def get_all(self):
        return self.data_dao.get_all()

    # 配合SQLAlchemy的ModelStorage模型中的update_info类方法，实现根据传入的指定id和新数据进行更新数据库信息的功能
    def update_info(self, id: int, new_data: dict):
        self.data_dao.update_info(id, new_data)

    # 配合SQLAlchemy的ModelStorage模型中的delete_info类方法，实现根据int类型的id删除数据库信息的功能
    def delete_info(self, id: int):
        self.data_dao.delete_info(id)

    # 配合SQLAlchemy的ModelStorage模型中的add_info类方法，实现根据传入的新数据添加数据库信息的功能
    def add_info(self, new_data: dict):
        self.data_dao.add_info(new_data)

    # 配合SQLAlchemy的ModelStorage模型中的search_info类方法，实现根据传入的字符串进行模糊查询数据库信息的功能
    def search_info(self, search_str: str):
        return self.data_dao.search_info(search_str)

    # 配合SQLAlchemy的ModelStorage模型中的get_all_score类方法，实现获取所有模型评分的功能
    def get_all_score(self):
        return self.data_dao.get_all_score()
    # 配合SQLAlchemy的ModelStorage模型中的get_score_list类方法，将模型评分数据转换为列表的功能
    def get_score_list(self):
        return self.data_dao.get_score_list()



# 服务于管理员登录和注册，以及后面信息展示的服务类
class ServiceAdmin:
    def __init__(self, data_dao):
        self.data_dao = data_dao

    # 配合SQLAlchemy的AdminStorage模型中的get_all类方法，实现获取所有数据的功能
    def get_all(self):
        return self.data_dao.get_all()

    # 配合SQLAlchemy的AdminInfoTable模型中的is_exist类方法，实现根据传入的用户名和密码判断是否存在该用户的功能
    def is_exist(self, username: str, password: str):
        return self.data_dao.is_exist(username, password)
    # 配合SQLAlchemy的AdminInfoTable模型中的add_info类方法，实现根据传入的新数据添加数据库信息的功能
    def add_info(self, new_data: dict):
        self.data_dao.add_info(new_data)
