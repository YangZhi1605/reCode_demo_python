from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

'''
需要在 User 模型中定义你的数据库表的字段。
每个字段都应该是 db.Column 类的一个实例，你需要指定字段的类型，
如 db.String、db.Integer 等。
如果字段是表的主键，你需要将 primary_key 参数设置为 True。 
例如，如果你的用户表有 id、username 和 email 三个字段，你可以这样定义 User 模型：
```
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
```
'''
# 如下是我的数据表信息：

# CREATE TABLE IF NOT EXISTS t_user(
#  id VARCHAR(20) PRIMARY KEY,
#  name VARCHAR(40),
#  age int(3),
#  salary DOUBLE(7,2),
#  phoneCode VARCHAR(11)
# );

# 创建一个数据库模型文件，比如models.py。在其中定义数据库模型
class User(db.Model):
    '''
    在 SQLAlchemy 中，模型类的名称默认会被转换为小写，并用作数据库表的名称。
    所以，如果你的模型类名为 User，那么 SQLAlchemy 默认会将其映射到名为 user 的数据库表。
    如果你想要映射到一个不同的表，例如 t_user，
    你可以在模型类中设置 __tablename__ 属性来指定表名。例如：

    '''
    __tablename__ = 't_user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    age = db.Column(db.Integer)
    salary = db.Column(db.Float)
    phoneCode = db.Column(db.String(11))


    # 查询所有的类方法
    @classmethod
    def find_all(cls):
        return cls.query.all()
