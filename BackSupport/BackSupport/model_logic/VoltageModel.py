from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_

db = SQLAlchemy()

# 写对应于device_fk的数据模型
# 我的数据表如下，我需要写对应的数据模型
'''
/*
-- ----------------------------
-- Table structure for device
-- ----------------------------
DROP TABLE IF EXISTS `device1`;
CREATE TABLE `device1`  (
  `ID` int(0) NOT NULL AUTO_INCREMENT,
  `InfoType` int(0) NULL DEFAULT NULL,
  `DeviceNodeID` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `DeviceName` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `UserID` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `CollectTime` datetime(0) NULL DEFAULT NULL,
  `Voltage1` float NULL DEFAULT NULL,
  `Voltage2` float NULL DEFAULT NULL,
  `Voltage3` float NULL DEFAULT NULL,
  `Voltage4` float NULL DEFAULT NULL,
  `Voltage5` float NULL DEFAULT NULL,
  `Voltage6` float NULL DEFAULT NULL,
  `Voltage7` float NULL DEFAULT NULL,
  `Voltage8` float NULL DEFAULT NULL,
  `Voltage9` float NULL DEFAULT NULL,
  `Voltage10` float NULL DEFAULT NULL,
  `Voltage11` float NULL DEFAULT NULL,
  `Voltage12` float NULL DEFAULT NULL,
  `Voltage13` float NULL DEFAULT NULL,
  `Voltage14` float NULL DEFAULT NULL,
  `Voltage15` float NULL DEFAULT NULL,
  `Voltage16` float NULL DEFAULT NULL,
  PRIMARY KEY (`ID`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 654378 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;

'''
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, DateTime

db = SQLAlchemy()

# 定义数据模型 —— 用于大量数据的可视化分析
class Device(db.Model):
    __tablename__ = 'device_fk'  # 表名称
    ID = Column(Integer, primary_key=True, autoincrement=True)  # 设备的唯一ID
    InfoType = Column(Integer)  # 信息类型
    DeviceNodeID = Column(String(50))  # 设备节点ID
    DeviceName = Column(String(50))  # 设备名
    UserID = Column(String(50))  # 用户ID
    CollectTime = Column(DateTime)  # 数据采集时间
    Voltage1 = Column(Float)  # 电压1
    Voltage2 = Column(Float)  # 电压2
    Voltage3 = Column(Float)  # 电压3
    Voltage4 = Column(Float)  # 电压4
    Voltage5 = Column(Float)  # 电压5
    Voltage6 = Column(Float)  # 电压6
    Voltage7 = Column(Float)  # 电压7
    Voltage8 = Column(Float)  # 电压8
    Voltage9 = Column(Float)  # 电压9
    Voltage10 = Column(Float)  # 电压10
    Voltage11 = Column(Float)  # 电压11
    Voltage12 = Column(Float)  # 电压12
    Voltage13 = Column(Float)  # 电压13
    Voltage14 = Column(Float)  # 电压14
    Voltage15 = Column(Float)  # 电压15
    Voltage16 = Column(Float)  # 电压16

    # 这个函数定义了实例的字符串表示形式
    # 当你在Python编写代码时，如果尝试打印一个对象或者在解释器中简单地输入一个对象实例并回车，
    # Python会调用这个对象的__repr__方法来获得可以显示的字符串。
    # 目的是为了方便调试和记录日志，提供一个对象的描述性信息。
    def __repr__(self):
        return f"<Device(ID={self.ID}, DeviceName={self.DeviceName}, UserID={self.UserID}, CollectTime={self.CollectTime})>"

    # 查询输入电压的类方法：使用ORM的查询语句来选取Voltage1, Voltage3, Voltage5, ..., Voltage15 这些特定的列。with_entities方法告诉查询只返回指定的列而不是整个Device对象。
    # 经过测试，能够拿到指定列的数据
    @classmethod
    def get_odd_voltages(cls):
        return cls.query.with_entities(
            cls.Voltage1, cls.Voltage3, cls.Voltage5, cls.Voltage7,
            cls.Voltage9, cls.Voltage11, cls.Voltage13, cls.Voltage15
        ).all()

    # 整理动态折线图数据的方法
    def format_voltages(voltages):
        # 存储格式化后的电压
        formatted_voltages = []
        # 创建表头信息
        header = ["VoltageVal", "VoltageName", "num"]
        # 将表头信息加入结果列表
        formatted_voltages.append(header)

        # 批次的编号
        batch_num = 1

        for voltage_tuple in voltages:
            for index, voltage in enumerate(voltage_tuple):
                # 创建电压列表，并将它们添加到结果列表中
                circuit_name = f"circuit{index + 1}"
                # 忽略零值的电压（如果电压实际可以为0，删除此行）
                if voltage != 0:
                    formatted_voltages.append([voltage, circuit_name, batch_num])
            # 更新设备编号
            batch_num += 1

        return formatted_voltages


# 定义用户上传数据的模型——用于上传数据后形成表格的数据交互
class Device_Upload(db.Model):
    __tablename__ = 'device_upload'  # 表名称
    ID = Column(Integer, primary_key=True, autoincrement=True)  # 设备的唯一ID
    InfoType = Column(Integer)  # 信息类型
    DeviceNodeID = Column(String(50))  # 设备节点ID
    DeviceName = Column(String(50))  # 设备名
    UserID = Column(String(50))  # 用户ID
    CollectTime = Column(DateTime)  # 数据采集时间
    Voltage1 = Column(Float)  # 电压1
    Voltage2 = Column(Float)  # 电压2
    Voltage3 = Column(Float)  # 电压3
    Voltage4 = Column(Float)  # 电压4
    Voltage5 = Column(Float)  # 电压5
    Voltage6 = Column(Float)  # 电压6
    Voltage7 = Column(Float)  # 电压7
    Voltage8 = Column(Float)  # 电压8
    Voltage9 = Column(Float)  # 电压9
    Voltage10 = Column(Float)  # 电压10
    Voltage11 = Column(Float)  # 电压11
    Voltage12 = Column(Float)  # 电压12
    Voltage13 = Column(Float)  # 电压13
    Voltage14 = Column(Float)  # 电压14
    Voltage15 = Column(Float)  # 电压15
    Voltage16 = Column(Float)  # 电压16

    # 这个函数定义了实例的字符串表示形式
    # 当你在Python编写代码时，如果尝试打印一个对象或者在解释器中简单地输入一个对象实例并回车，
    # Python会调用这个对象的__repr__方法来获得可以显示的字符串。
    # 目的是为了方便调试和记录日志，提供一个对象的描述性信息。
    def __repr__(self):
        return f"<Device(ID={self.ID}, DeviceName={self.DeviceName}, UserID={self.UserID}, CollectTime={self.CollectTime})>"

    # 根据传入id删除信息的类方法
    @classmethod
    def delete_info(cls, id):
        device = cls.query.get(id)
        db.session.delete(device)
        db.session.commit()
