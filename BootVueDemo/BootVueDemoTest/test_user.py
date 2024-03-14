import sys
import os
# 将 BootVueDemoTest 目录添加到 Python 的模块搜索路径中。你可以在 test_user.py 文件的顶部添加以下代码
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# 你可以在 test_user.py 文件的顶部添加以下代码
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import unittest
# 导入BootvueDemo包中的create_app函数，该函数在__init__.py文件中
from BootVueDemo import create_app
# 导入SQLAlchemy的db对象和User模型
from BootVueDemo.utils.models import db, User



# 创建一个测试类，继承自 unittest.TestCase
class TestUser(unittest.TestCase):

    # 在setUp方法中设置测试环境
    def setUp(self):
        # 创建一个app对象
        self.app = create_app()
        # 加载测试类的配置文件，测试类中设置 Flask 应用的 SQLAlchemy 数据库连接 URI
        self.app.config.from_object('BootVueDemo.config.setting.TestConfig')
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            # 删除所有的用户记录
            db.session.query(User).delete()
            db.session.commit()

    # tearDown 方法中完成这些清理工作
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    # 测试查询所有用户
    def test_find_all(self):
        with self.app.app_context():
            # 创建两个User对象
            user1 = User(id='001', name='Tom', age=20, salary=5000.00, phoneCode='12345678901')
            user2 = User(id='002', name='Jerry', age=22, salary=6000.00, phoneCode='09876543210')
            # 将两个User对象添加到数据库
            db.session.add(user1)
            db.session.add(user2)
            # 提交
            db.session.commit()

            # 查询所有的User对象
            users = User.find_all()
            # 断言: assert 语句来检查你的代码的行为是否符合预期
            self.assertEqual(len(users), 2)
            self.assertEqual(users[0].name, 'Tom')
            self.assertEqual(users[1].name, 'Jerry')


if __name__ == '__main__':
    unittest.main()