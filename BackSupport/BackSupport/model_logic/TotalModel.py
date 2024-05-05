from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_, Text
from sqlalchemy import cast, String
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.exc import SQLAlchemyError

db = SQLAlchemy()

######################################################################################
#                               电路信息相关模型类                                        #
#                                                                                    #
######################################################################################

# 写对应于device_fk的数据模型,改成device_upload了。因为两个数据表只是名称不同，功能相同，device_fk用于测试。现在device_upload用于实际数据
# 但是暂时不改，首页的动态折线图用的device_fk的。然后下面已经有device_upload了。日志整合好以后，重新给它整合下去
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

    # 根据传入的字符串对设备名和电压数值进行模糊查询的类方法
    # tips:针对您的情况，由于 Voltage1 到 Voltage16 字段是 Float 类型，
    # 直接使用 like 方法将引发错误，因为 like 预期的是字符串。
    # 对于这种情况，可以将 Float 类型的电压值先转换成字符串，
    # 再使用 like。在SQLAlchemy里，可以用 cast 函数进行类型转换
    @classmethod
    def search_info(cls, search_str):
        return cls.query.filter(or_(
            cls.DeviceName.like(f'%{search_str}%'),
            cast(cls.Voltage1, String).like(f'%{search_str}%'),
            cast(cls.Voltage2, String).like(f'%{search_str}%'),
            cast(cls.Voltage3, String).like(f'%{search_str}%'),
            cast(cls.Voltage4, String).like(f'%{search_str}%'),
            cast(cls.Voltage5, String).like(f'%{search_str}%'),
            cast(cls.Voltage6, String).like(f'%{search_str}%'),
            cast(cls.Voltage7, String).like(f'%{search_str}%'),
            cast(cls.Voltage8, String).like(f'%{search_str}%'),
            cast(cls.Voltage9, String).like(f'%{search_str}%'),
            cast(cls.Voltage10, String).like(f'%{search_str}%'),
            cast(cls.Voltage11, String).like(f'%{search_str}%'),
            cast(cls.Voltage12, String).like(f'%{search_str}%'),
            cast(cls.Voltage13, String).like(f'%{search_str}%'),
            cast(cls.Voltage14, String).like(f'%{search_str}%'),
            cast(cls.Voltage15, String).like(f'%{search_str}%'),
            cast(cls.Voltage16, String).like(f'%{search_str}%'),
            cls.UserID.like(f'%{search_str}%'),
        )).all()

    # 根据前台传递的ID和数据对象，更新数据库中对应ID的数据的类方法
    @classmethod
    def update_info(cls, id, data):
        # device = cls.query.get(id) 这行代码是用于从数据库中查找并获取具有特定 id 的实体对象。这里 cls 代表类方法中的类本身，在这个场景中，它应该是指代一个定义了数据库映射的模型类。作用在于，它告诉 SQLAlchemy 去数据库中对应表格查询主键值为 id 的行
        device = cls.query.get(id)
        # 如果没有查询到对象，返回 None
        print('得到的device对象是：', device)
        device.DeviceNodeID = data['DeviceNodeID']
        device.DeviceName = data['DeviceName']
        device.UserID = data['UserID']
        device.CollectTime = data['CollectTime']
        device.Voltage1 = data['Voltage1']
        device.Voltage2 = data['Voltage2']
        device.Voltage3 = data['Voltage3']
        device.Voltage4 = data['Voltage4']
        device.Voltage5 = data['Voltage5']
        device.Voltage6 = data['Voltage6']
        device.Voltage7 = data['Voltage7']
        device.Voltage8 = data['Voltage8']
        device.Voltage9 = data['Voltage9']
        device.Voltage10 = data['Voltage10']
        device.Voltage11 = data['Voltage11']
        device.Voltage12 = data['Voltage12']
        device.Voltage13 = data['Voltage13']
        device.Voltage14 = data['Voltage14']
        device.Voltage15 = data['Voltage15']
        device.Voltage16 = data['Voltage16']
        db.session.merge(device)
        db.session.commit()


# 定义管理电路权限的模型，其sql数据格式如下：
'''
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for device_circuit_weight
-- ----------------------------
DROP TABLE IF EXISTS `device_circuit_weight`;
CREATE TABLE `device_circuit_weight`  (
  `DataID` int(0) NOT NULL AUTO_INCREMENT,
  `RuleName` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '某套权重分配规则的名称',
  `Circuit1` float(40, 4) NULL DEFAULT NULL COMMENT '电路权重',
  `Circuit2` float(40, 4) NULL DEFAULT NULL,
  `Circuit3` float(40, 4) NULL DEFAULT NULL,
  `Circuit4` float(40, 4) NULL DEFAULT NULL,
  `Circuit5` float(40, 4) NULL DEFAULT NULL,
  `Circuit6` float(40, 4) NULL DEFAULT NULL,
  `Circuit7` float(40, 4) NULL DEFAULT NULL,
  `Circuit8` float(40, 4) NULL DEFAULT NULL,
  `IsSet` int(0) NULL DEFAULT NULL COMMENT '通过0和1表示是否运用',
  PRIMARY KEY (`DataID`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;
'''
class Device_Circuit_Weight(db.Model):
    __tablename__ = 'device_circuit_weight'  # 表名称
    DataID = Column(Integer, primary_key=True, autoincrement=True)  # 电路权重的唯一ID
    RuleName= Column(String(255))  # 某套权重分配规则的名称
    Circuit1 = Column(Float)  # 电路1的权重
    Circuit2 = Column(Float)  # 电路2的权重
    Circuit3 = Column(Float)  # 电路3的权重
    Circuit4 = Column(Float)  # 电路4的权重
    Circuit5 = Column(Float)  # 电路5的权重
    Circuit6 = Column(Float)  # 电路6的权重
    Circuit7 = Column(Float)  # 电路7的权重
    Circuit8 = Column(Float)  # 电路8的权重
    IsSet = Column(Integer)  # 通过0和1表示是否运用
    EditUser = Column(String(50))  # 编辑用户
    EditTime = Column(DateTime)  # 编辑时间

    # 这个函数定义了实例的字符串表示形式
    # 当你在Python编写代码时，如果尝试打印一个对象或者在解释器中简单地输入一个对象实例并回车，
    # Python会调用这个对象的__repr__方法来获得可以显示的字符串。
    # 目的是为了方便调试和记录日志，提供一个对象的描述性信息。
    def __repr__(self):
        return f"<Device_Circuit_Weight(DataID={self.DataID}, RuleName={self.RuleName}, Circuit1={self.Circuit1}, Circuit2={self.Circuit2}, Circuit3={self.Circuit3}, Circuit4={self.Circuit4}, Circuit5={self.Circuit5}, Circuit6={self.Circuit6}, Circuit7={self.Circuit7}, Circuit8={self.Circuit8},IsSet={self.IsSet},EditTime={self.EditTime},EditUser={self.EditUser})>"

    #编写to_dict方法，将模型获取的结果转换为字典返回
    def to_dict(self):
        return {
            'DataID': self.DataID,
            'RuleName': self.RuleName,
            'Circuit1': self.Circuit1,
            'Circuit2': self.Circuit2,
            'Circuit3': self.Circuit3,
            'Circuit4': self.Circuit4,
            'Circuit5': self.Circuit5,
            'Circuit6': self.Circuit6,
            'Circuit7': self.Circuit7,
            'Circuit8': self.Circuit8,
            'IsSet': self.IsSet,
            'EditUser': self.EditUser,
            'EditTime': self.EditTime
        }

    # 查询所有数据的类方法
    @classmethod
    def get_all(cls):
        return cls.query.all()

    # 编写根据前台传递的ID和对象进行修改的类方法
    @classmethod
    def update_info(cls, id, data):
        device = cls.query.get(id)
        print('查询到结果：',device)
        print('前台拿到的内容：',id,data)
        device.RuleName = data['RuleName']
        device.Circuit1 = data['Circuit1']
        device.Circuit2 = data['Circuit2']
        device.Circuit3 = data['Circuit3']
        device.Circuit4 = data['Circuit4']
        device.Circuit5 = data['Circuit5']
        device.Circuit6 = data['Circuit6']
        device.Circuit7 = data['Circuit7']
        device.Circuit8 = data['Circuit8']
        device.IsSet = data['IsSet']
        device.EditUser = data['EditUser']
        # 让修改时间设置为当前的时间
        device.EditTime = datetime.utcnow()  # 如果数据库中以UTC时间存储，这里就不需要转换了
        db.session.merge(device)
        db.session.commit()

    # 编写根据前台传递的对象进行添加的类方法
    @classmethod
    def add_info(cls, data):

        new_device = cls(
            RuleName=data['RuleName'],
            Circuit1=data['Circuit1'],
            Circuit2=data['Circuit2'],
            Circuit3=data['Circuit3'],
            Circuit4=data['Circuit4'],
            Circuit5=data['Circuit5'],
            Circuit6=data['Circuit6'],
            Circuit7=data['Circuit7'],
            Circuit8=data['Circuit8'],
            IsSet=data['IsSet'],
            EditUser=data['EditUser'],
            # 要调用时间模块，将时间转换为MYSQL的datetime格式
            EditTime = datetime.strptime(data['EditTime'], '%Y-%m-%dT%H:%M:%S.%fZ')  # 转换为datetime对象
        )
        db.session.add(new_device)
        db.session.commit()

    # 根据前台传递的'规则名称'和'修改者名称'两个参数进行模糊查询的类方法
    @classmethod
    def search_info(cls, search_str):
        return cls.query.filter(or_(
            cls.RuleName.like(f'%{search_str}%'),
            cls.EditUser.like(f'%{search_str}%')
        )).all()

    # 根据前台传递的DataID进行删除的类方法
    @classmethod
    def delete_info(cls, id):
        device = cls.query.get(id)
        db.session.delete(device)
        db.session.commit()


# 定义一个检修日志模型。其数据表结果如下：
"""
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for devicenode_maintaininfo
-- ----------------------------
DROP TABLE IF EXISTS `devicenode_maintaininfo`;
CREATE TABLE `devicenode_maintaininfo`  (
  `DeviceNodeID` int(0) NOT NULL AUTO_INCREMENT,
  `MaintenanceDate` datetime(0) NULL DEFAULT NULL,
  `MaintenanceUser` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `MaintenanceRport` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '检测建议',
  `MaintenanceTage` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '是否处理',
  PRIMARY KEY (`DeviceNodeID`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
ALTER TABLE `devicenode_maintaininfo` AUTO_INCREMENT = 1;

"""
class DeviceNode_MaintainInfo(db.Model):
    __tablename__ = 'devicenode_maintaininfo'  # 表名称
    DeviceNodeID = Column(Integer, primary_key=True, autoincrement=True)  # 设备节点的唯一ID
    MaintenanceDate = Column(DateTime)  # 检修日期
    MaintenanceUser = Column(String(255))  # 检修用户
    MaintenanceRport = Column(String(255))  # 检测建议
    MaintenanceTage = Column(String(255))  # 是否处理

    # 这个函数定义了实例的字符串表示形式
    # 当你在Python编写代码时，如果尝试打印一个对象或者在解释器中简单地输入一个对象实例并回车，
    # Python会调用这个对象的__repr__方法来获得可以显示的字符串。
    # 目的是为了方便调试和记录日志，提供一个对象的描述性信息。
    def __repr__(self):
        return f"<DeviceNode_MaintainInfo(DeviceNodeID={self.DeviceNodeID}, MaintenanceDate={self.MaintenanceDate}, MaintenanceUser={self.MaintenanceUser}, MaintenanceRport={self.MaintenanceRport}, MaintenanceTage={self.MaintenanceTage})>"

    # 编写to_dict方法，将模型获取的结果转换为字典返回
    def to_dict(self):
        return {
            'DeviceNodeID': self.DeviceNodeID,
            # 'MaintenanceDate': self.MaintenanceDate,
            # flask 使用了 jsonify 函数来完成这个转换，而 jsonify 在内部使用标准的 json 模块。
            # json 模块默认无法直接序列化 datetime 对象，
            # 因此需要提供一个自定义的序列化方法或在对象转换为字典之前，将日期时间对象格式化为字符串。
            # 但是我们需要数据库中的ISO 8601格式
            'MaintenanceDate': self.MaintenanceDate.strftime('%Y-%m-%d %H:%M:%S'),
            'MaintenanceUser': self.MaintenanceUser,
            'MaintenanceRport': self.MaintenanceRport,
            'MaintenanceTage': self.MaintenanceTage
        }

    # 编写根据前台传递的ID和对象进行修改的类方法
    @classmethod
    def update_info(cls, id, data):
        device = cls.query.get(id)
        device.MaintenanceDate = data['MaintenanceDate']
        device.MaintenanceUser = data['MaintenanceUser']
        device.MaintenanceRport = data['MaintenanceRport']
        device.MaintenanceTage = data['MaintenanceTage']
        db.session.merge(device)
        db.session.commit()

    # 获取所有数据的类方法
    @classmethod
    def get_all(cls):
        return cls.query.all()

    # 根据指定id删除数据的类方法
    @classmethod
    def delete_info(cls, id):
        device = cls.query.get(id)
        db.session.delete(device)
        db.session.commit()

    # 根据前台输入的信息进行模糊查询的类方法
    @classmethod
    def search_info(cls, search_str):
        return cls.query.filter(or_(
            cls.MaintenanceUser.like(f'%{search_str}%'),
            cls.MaintenanceRport.like(f'%{search_str}%'),
            cls.MaintenanceTage.like(f'%{search_str}%')
        )).all()

    # 接收前台传来的数据，添加到数据库中的类方法
    @classmethod
    def add_info(cls, data):
        new_device = cls(
            MaintenanceDate=data['MaintenanceDate'],
            MaintenanceUser=data['MaintenanceUser'],
            MaintenanceRport=data['MaintenanceRport'],
            MaintenanceTage=data['MaintenanceTage']
        )
        db.session.add(new_device)
        db.session.commit()


######################################################################################
#                               机器学习模型类                                        #
#                                                                                    #
######################################################################################
'''
/*
-- ----------------------------
-- Table structure for modelstorage
-- ----------------------------
DROP TABLE IF EXISTS `modelstorage`;
CREATE TABLE `modelstorage`  (
  `ID` int(0) NOT NULL AUTO_INCREMENT,
  `CreateTime` datetime(0) NULL DEFAULT CURRENT_TIMESTAMP(0),
  `ModelName` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `CreateUser` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `ModelPath` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `IsUse` int(1) NOT NULL DEFAULT 1,
  PRIMARY KEY (`ID`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

'''
# 根据上述数据表，创建模型存储类
class ModelStorage(db.Model):
    __tablename__ = 'modelstorage'
    ID = Column(db.Integer, primary_key=True, autoincrement=True)
    CreateTime = Column(DateTime)
    ModelName = Column(db.String(255), nullable=False)
    CreateUser = Column(db.String(255), nullable=False)
    ModelPath = Column(db.Text, nullable=False)
    IsUse = Column(db.Integer, default=True)
    ModelScore = Column(db.Float, default=0.0)

    def __repr__(self):
        return '<ModelStorage %r>' % self.ModelName


    # 将对象信息转换为字典
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    # 编写获取数据表中所有数据的类方法
    @classmethod
    def get_all(cls):
        return cls.query.all()

    # 编写根据前台传递的ID和对象进行修改的类方法
    @classmethod
    def update_info(cls, id, data):
        device = cls.query.get(id)
        device.ModelName = data['ModelName']
        device.CreateUser = data['CreateUser']
        device.ModelPath = data['ModelPath']
        device.IsUse = data['IsUse']
        db.session.merge(device)
        db.session.commit()

    # 根据id删除的类方法
    @classmethod
    def delete_info(cls, id):
        device = cls.query.get(id)
        db.session.delete(device)
        db.session.commit()

    # 编写根据提供的数据对象进行添加机器学习模型路径的类方法
    @classmethod
    def add_info(cls, data):
        new_model = cls(
            ModelName=data['ModelName'],
            CreateUser=data['CreateUser'],
            ModelPath=data['ModelPath'],
            IsUse=data['IsUse'],
            CreateTime=data['CreateTime'],
            ModelScore=data['ModelScore']
        )
        db.session.add(new_model)
        db.session.commit()


'''

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for admininfo_table
-- ----------------------------
DROP TABLE IF EXISTS `admininfo_table`;
CREATE TABLE `admininfo_table`  (
  `id` int(0) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `email` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `contact` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

'''
# 我当前的数据表如上，创建一个对应的模型,负责存储管理员信息
class AdminInfoTable(db.Model):
    __tablename__ = 'admininfo_table'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255))
    email = Column(String(255))
    contact = Column(String(255))
    password = Column(String(255))

    def __repr__(self):
        return '<AdminInfoTable %r>' % self.username

    # 将对象信息转换为字典
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    # 编写获取数据表中所有数据的类方法
    @classmethod
    def get_all(cls):
        return cls.query.all()



    # 根据前台传递的'用户名'和'密码'两个参数进行查询的类方法
    @classmethod
    def is_exist(cls, username, password):
        return cls.query.filter_by(username=username, password=password).first()

    # 根据前台传递的对象进行添加的类方法
    @classmethod
    def add_info(cls, data):
        new_device = cls(
            username=data['username'],
            email=data['email'],
            contact=data['contact'],
            password=data['password']
        )
        db.session.add(new_device)
        db.session.commit()

'''
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for device_analysis
-- ----------------------------
DROP TABLE IF EXISTS `device_analysis`;
CREATE TABLE `device_analysis`  (
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
  `HealthLevel` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`ID`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

'''
# 根据上述数据表，创建一个模型，负责存储设备分析信息
class DeviceAnalysis(db.Model):
    __tablename__ = 'device_analysis'
    ID = Column(Integer, primary_key=True, autoincrement=True)
    InfoType = Column(Integer)
    DeviceNodeID = Column(String(50))
    DeviceName = Column(String(50))
    UserID = Column(String(50))
    CollectTime = Column(DateTime)
    Voltage1 = Column(Float)
    Voltage2 = Column(Float)
    Voltage3 = Column(Float)
    Voltage4 = Column(Float)
    Voltage5 = Column(Float)
    Voltage6 = Column(Float)
    Voltage7 = Column(Float)
    Voltage8 = Column(Float)
    Voltage9 = Column(Float)
    Voltage10 = Column(Float)
    Voltage11 = Column(Float)
    Voltage12 = Column(Float)
    Voltage13 = Column(Float)
    Voltage14 = Column(Float)
    Voltage15 = Column(Float)
    Voltage16 = Column(Float)
    HealthLevel = Column(String(50))

    def __repr__(self):
        return '<DeviceAnalysis %r>' % self.DeviceName

    # 编写获取数据表中所有数据的类方法
    @classmethod
    def get_all(cls):
        return cls.query.all()

    # 将对象信息转换为字典
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


'''
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for front_userinfo_table
-- ----------------------------
DROP TABLE IF EXISTS `front_userinfo_table`;
CREATE TABLE `front_userinfo_table`  (
  `id` int(0) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `phone` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `sex` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `email` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `editTime` datetime(0) NULL DEFAULT NULL,
  `carName` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
   `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
ALTER TABLE front_userinfo_table AUTO_INCREMENT = 1;

'''
# 我当前的数据表如上，创建一个对应的模型,负责存储前台用户信息
class FrontUserInfoTable(db.Model):
    __tablename__ = 'front_userinfo_table'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255))
    phone = Column(String(255))
    sex = Column(String(10))
    email = Column(String(255))
    editTime = Column(DateTime)
    carName = Column(String(255))
    password = Column(String(255))

    # 编写获取数据表中所有数据的类方法
    @classmethod
    def get_all(cls):
        return cls.query.all()

    # 将对象信息转换为字典
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    # 根据传入的id删除信息的类方法
    @classmethod
    def delete_info(cls, id):
        try:
            device = cls.query.get(id)
            if device is None:  # 检查是否找到了要删除的对象
                return {'success': False, 'message': '对象不存在。'}
            db.session.delete(device)
            db.session.commit()
            return {'success': True, 'message': '对象删除成功。'}
        except Exception as e:
            # 在这里你可以记录异常信息，比如：print(e) 或者使用应用的日志系统
            return {'success': False, 'message': '删除过程中发生错误。'}


    # 根据前台传递的username和phone进行模糊查询的类方法，只要有一个字段匹配即可
    @classmethod
    def search_info(cls, search_str):
        return cls.query.filter(or_(
            cls.username.like(f'%{search_str}%'),
            cls.phone.like(f'%{search_str}%')
        )).all()

    # 根据前台传递的信息进行添加的类方法
    @classmethod
    def add_info(cls, data):
        try:
            new_user = cls(
                username=data['username'],
                phone=data['phone'],
                email=data['email'],
                password=data['password'],
                sex=data['sex'],
                carName=data['carName'],
                editTime=data['editTime']  # 如果数据库中以UTC时间存储，这里就不需要转换了
            )
            db.session.add(new_user)
            db.session.commit()
            return {'success': True, 'message': '用户添加成功。'}
        except Exception as e:
            # 在这里你可以记录异常信息，比如：print(e) 或者使用应用的日志系统
            db.session.rollback()  # 发生异常后回滚
            return {'success': False, 'message': '添加过程中发生错误。'}

    # 根据前台传递的ID,将密码重置为123456的类方法，做异常处理
    @classmethod
    def reset_password(cls, id):
        try:
            user = cls.query.get(id)
            if user is None:  # 检查是否找到了要删除的对象
                return {'success': False, 'message': '对象不存在。'}
            user.password = '123456'
            db.session.merge(user)
            db.session.commit()
            return {'success': True, 'message': '密码重置成功。'}
        except Exception as e:
            # 在这里你可以记录异常信息，比如：print(e) 或者使用应用的日志系统
            return {'success': False, 'message': '密码重置过程中发生错误。'}

    # 根据前台传递的email和password进行查询的类方法,返回查询到的对象，用户名和密码不能为空，提供查询成功和不成功的异常处理
    @classmethod
    def is_exist(cls, email, password):
        # 检查email和password是否为空
        if not email or not password:
            raise ValueError("邮箱和密码不能为空")

        try:
            # 执行数据库查询
            user = cls.query.filter_by(email=email, password=password).first()
            if user:
                return user
            else:
                raise ValueError("未找到匹配的用户")
        except SQLAlchemyError as e:
            # 处理查询过程中可能出现的异常
            raise Exception(f"数据库查询失败: {e}")


    # 根据前台传递的对象进行添加的类方法，用于注册用户，返回注册成功和不成功的异常处理
    @classmethod
    def register(cls, data):
        # 检查email和password是否为空
        if not data['email'] or not data['password']:
            raise ValueError("邮箱和密码不能为空")

        try:
            new_user = cls(
                username=data['username'],
                phone=data['phone'],
                email=data['email'],
                password=data['password'],
                sex=data['sex'],
                carName=data['carName'],
                editTime=data['editTime']  # 如果数据库中以UTC时间存储，这里就不需要转换了
            )
            db.session.add(new_user)
            db.session.commit()
            return new_user
        except SQLAlchemyError as e:
            # 处理查询过程中可能出现的异常
            raise Exception(f"数据库查询失败: {e}")



'''
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for device_node_store
-- ----------------------------
DROP TABLE IF EXISTS `device_node_store`;
CREATE TABLE `device_node_store`  (
  `id` int(0) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '零件商品名称',
  `desc` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '零件商品描述',
  `price` float(10, 2) NULL DEFAULT NULL COMMENT '零件商品价格',
  `img` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '零件商品存储路径',
  `number` int(0) NULL DEFAULT NULL COMMENT '库存数量',
  `productCompany` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '商品所属公司',
  `editTime` datetime(0) NULL DEFAULT NULL COMMENT '修改时间',
  `editUser` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '修改者姓名',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
ALTER TABLE device_node_store AUTO_INCREMENT = 1;

'''
# 我当前的数据表如上，创建一个对应的模型,负责存储零件商品信息
class DeviceNodeStore(db.Model):
    __tablename__ = 'device_node_store'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    desc = Column(Text)
    price = Column(Float)
    img = Column(String(255))
    number = Column(Integer)
    productCompany = Column(String(255))
    editTime = Column(DateTime)
    editUser = Column(String(255))


    # 编写获取数据表中所有数据的类方法
    @classmethod
    def get_all(cls):
        return cls.query.all()

    # 将对象信息转换为字典
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    # 根据传入的id删除信息的类方法
    @classmethod
    def delete_info(cls, id):
        try:
            device = cls.query.get(id)
            if device is None:  # 检查是否找到了要删除的对象
                return {'success': False, 'message': '对象不存在。'}
            db.session.delete(device)
            db.session.commit()
            return {'success': True, 'message': '对象删除成功。'}
        except Exception as e:
            # 在这里你可以记录异常信息，比如：print(e) 或者使用应用的日志系统
            return {'success': False, 'message': '删除过程中发生错误。'}

    # 根据前台传递的name和productCompany进行模糊查询的类方法
    @classmethod
    def search_info(cls, search_str):
        return cls.query.filter(or_(
            cls.name.like(f'%{search_str}%'),
            cls.productCompany.like(f'%{search_str}%')
        )).all()

    # 根据前台传递的信息进行添加的类方法
    @classmethod
    def add_info(cls, data):
        try:
            new_device_node = cls(
                name=data['name'],
                desc=data['desc'],
                price=data['price'],
                img=data['img'],
                number=data['number'],
                productCompany=data['productCompany'],
                editTime=data['editTime'],  # 如果数据库中以UTC时间存储，这里就不需要转换了
                editUser=data['editUser']

            )
            db.session.add(new_device_node)
            db.session.commit()
            return {'success': True, 'message': '零件商品添加成功。'}
        except Exception as e:
            # 在这里你可以记录异常信息，比如：print(e) 或者使用应用的日志系统
            print(e)  # 将异常信息打印出来
            db.session.rollback()
            return {'success': False, 'message': '添加过程中发生错误。'}

    # 根据前台传递的ID和数据对象，更新数据库中对应ID的数据的类方法
    @classmethod
    def update_info(cls, id, data):
        try:
            device = cls.query.get(id)
            device.name = data['name']
            device.desc = data['desc']
            device.price = data['price']
            device.img = data['img']
            device.number = data['number']
            device.productCompany = data['productCompany']
            device.editTime = data['editTime']
            device.editUser = data['editUser']
            db.session.merge(device)
            db.session.commit()
            return {'success': True, 'message': '零件商品更新成功。'}
        except Exception as e:
            # 在这里你可以记录异常信息，比如：print(e) 或者使用应用的日志系统
            print(e)
            db.session.rollback()
            return {'success': False, 'message': '更新过程中发生错误。'}

    # 根据前台传递的id，查询指定的数据信息的类方法，做异常处理
    @classmethod
    def get_info_by_id(cls, id):
        try:
            device = cls.query.get(id)
            if device is None:
                return {'success': False, 'message': '对象不存在。'}
            return {'success': True, 'data': device.to_dict()}
        except Exception as e:
            # 在这里你可以记录异常信息，比如：print(e) 或者使用应用的日志系统
            print(e)
            return {'success': False, 'message': '查询过程中发生错误。'}


'''
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for cart
-- ----------------------------
DROP TABLE IF EXISTS `cart`;
CREATE TABLE `cart`  (
  `id` int(0) NOT NULL AUTO_INCREMENT,
  `selected` int(0) NULL DEFAULT NULL COMMENT '表示是否选中',
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `price` float(10, 2) NULL DEFAULT NULL,
  `cartTotalQuantity` int(0) NULL DEFAULT NULL COMMENT '购物车中零件商品的数量',
  `total` float(10, 2) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
'''
# 我当前的数据表如上，创建一个对应的模型,负责存储购物车信息
class Cart(db.Model):
    __tablename__ = 'cart'
    id = Column(Integer, primary_key=True, autoincrement=True)
    selected = Column(Integer)
    name = Column(String(255))
    price = Column(Float)
    cartTotalQuantity = Column(Integer)
    total = Column(Float)

    # 编写获取数据表中所有数据的类方法
    @classmethod
    def get_all(cls):
        return cls.query.all()

    # 将对象信息转换为字典
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    # 根据传入的id删除信息的类方法
    @classmethod
    def delete_info(cls, id):
        try:
            device = cls.query.get(id)
            if device is None:  # 检查是否找到了要删除的对象
                return {'success': False, 'message': '对象不存在。'}
            db.session.delete(device)
            db.session.commit()
            return {'success': True, 'message': '对象删除成功。'}
        except Exception as e:
            # 在这里你可以记录异常信息，比如：print(e) 或者使用应用的日志系统
            return {'success': False, 'message': '删除过程中发生错误。'}


    # 根据前台传递的name进行模糊查询的类方法
    @classmethod
    def search_info(cls, search_str):
        return cls.query.filter(cls.name.like(f'%{search_str}%')).all()


    # 根据前台传递的信息进行添加的类方法，添加前判断是否已经存在，存在则数量加上前台传递的数量，不存在则添加，做异常处理
    @classmethod
    def add_info(cls, data):
        try:
            # 查询是否已经存在该商品
            device = cls.query.filter_by(name=data['name']).first()
            if device:
                # 前台传递的是quantity
                device.cartTotalQuantity += data['quantity']
                device.total += data['total']
                db.session.merge(device)
                db.session.commit()
                return {'success': True, 'message': '购物车商品添加成功。'}
            else:
                new_device = cls(
                    selected=data['selected'],
                    name=data['name'],
                    price=data['price'],
                    cartTotalQuantity=data['quantity'],
                    total=data['total']
                )
                db.session.add(new_device)
                db.session.commit()
                return {'success': True, 'message': '购物车商品添加成功。'}
        except Exception as e:
            # 在这里你可以记录异常信息，比如：print(e) 或者使用应用的日志系统
            print(e)  # 将异常信息打印出来
            db.session.rollback()
            return {'success': False, 'message': '添加过程中发生错误。'}

    # 编写根据传入的id更新数量和依据数量计算总价的类方法
    @classmethod
    def update_info(cls, id, data):
        try:
            device = cls.query.get(id)
            # 更新数量
            device.cartTotalQuantity = data['cartTotalQuantity']
            # 计算新的总价：单价 * 数量
            device.total = device.price * data['cartTotalQuantity']
            db.session.merge(device)
            db.session.commit()
            return {'success': True, 'message': '购物车商品更新成功。'}
        except Exception as e:
            # 在这里你可以记录异常信息，比如：print(e) 或者使用应用的日志系统
            print(e)
            db.session.rollback()
            return {'success': False, 'message': '更新过程中发生错误。'}

    # 个方法将接收一个字典数组，每个字典包含商品ID和对应的选中状态（0或1）。然后，我们将迭代这些数据，更新每一项的 selected 字段，并提交到数据库中。
    @classmethod
    def update_selected_status(cls, items):
        try:
            # items 应该是一个字典数组，每个字典包含'id'和'selected'
            for item in items:
                # 根据id找到对应的购物车条目
                cart_item = cls.query.get(item['id'])
                if cart_item:
                    # 更新selected状态
                    cart_item.selected = item['selected']
                    db.session.merge(cart_item)
            db.session.commit()
            return {'success': True, 'message': '购物车商品选中状态更新成功。'}
        except Exception as e:
            # 打印异常信息，记录错误，或使用应用的日志系统
            print(e)
            db.session.rollback()
            return {'success': False, 'message': '更新过程中发生错误。'}


