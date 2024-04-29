import os
import sys
import unittest
from BackSupport import create_app
from BackSupport.model_logic.TotalModel import db, Device  # 确保导入Device模型

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class TestDevice(unittest.TestCase):

    def setUp(self):
        # 创建一个app对象
        self.app = create_app()
        # 加载测试类的配置文件，测试类中设置 Flask 应用的 SQLAlchemy 数据库连接 URI
        self.app.config.from_object('BackSupport.config.setting.TestConfig')
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            # 删除所有的数据记录
            db.session.query(Device).delete()
            db.session.commit()

    # tearDown 方法中完成这些清理工作
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


    def test_get_odd_voltages(self):
        # 添加一些测试设备数据
        device1 = Device(Voltage1=1.0, Voltage3=3.0, Voltage5=5.0, Voltage7=7.0, Voltage9=9.0, Voltage11=11.0, Voltage13=13.0, Voltage15=15.0)
        device2 = Device(Voltage1=2.0, Voltage3=4.0, Voltage5=6.0, Voltage7=8.0, Voltage9=10.0, Voltage11=12.0, Voltage13=14.0, Voltage15=16.0)
        db.session.add(device1)
        db.session.add(device2)
        db.session.commit()

        # 获取结果的对象
        results = Device.get_odd_voltages()
        self.assertEqual(len(results), 2)
        self.assertAlmostEqual(results[0][0], 1.0)  # Voltage1 for device1
        self.assertAlmostEqual(results[1][0], 2.0)  # Voltage1 for device2
        # ... 对其他奇数电压值进行测试断言

if __name__ == '__main__':
    unittest.main()