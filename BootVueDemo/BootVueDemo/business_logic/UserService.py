from typing import List
# 导入模型
from BootVueDemo.utils.models import User
# from your_project.models import User

class UserService:
    def __init__(self, user_dao):
        self.user_dao = user_dao

    # 配合SQLAlchemy的User模型，实现查询所有用户的功能
    def find_all(self) -> List[User]:
        return self.user_dao.find_all()

    # 配合SQLAlchemy的User模型，实现保存用户信息的功能
    def save(self, user: User):
        self.user_dao.save(user)

    # 配合SQLAlchemy的User模型，实现根据int类型的id删除用户的功能
    def delete(self, id: int):
        self.user_dao.delete(id)

    # 配合SQLAlchemy的User模型，实现根据int类型的id查询一个用户的功能
    def find_one(self, id: int):
        return self.user_dao.find_one(id)

    # 配合SQLAlchemy的User模型，实现根据int类型的id更新用户的功能
    def update(self, user: User):
        self.user_dao.update(user)

    # 配合SQLAlchemy的User模型，实现根据string类型的name或者string类型的phoneCode进行模糊查询所有用户的功能
    def find_by_name_or_phone(self, name: str, phoneCode: str):
        return self.user_dao.find_by_name_or_phone(name, phoneCode)