from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_

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
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    age = db.Column(db.Integer)
    salary = db.Column(db.Float)
    phoneCode = db.Column(db.String(11))


    # 查询所有的类方法
    @classmethod
    def find_all(cls):
        return cls.query.all()

    # 将查询到的用户数据转换成字典列表并返回JSON。假如不是字典的情况下，因为我自己数据库查询到的结果是字典，所以我直接返回了，
    # 注意区分__dict__属性和to_dict()方法的区别.后者是我自己写的，一定程度上可以决定我需要暴露哪些字段给前端。
    # ython 中的每个对象都有一个内置的 __dict__ 属性，它是一个字典，包含了该对象的所有属性和它们的值。你可以直接使用 __dict__ 属性来将对象转换为字典
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'salary': self.salary,
            'phoneCode': self.phoneCode
        }

    # 保存用户的类方法
    @classmethod
    def save(cls, user):
        db.session.add(user)
        db.session.commit()

    # 根据int类型的id删除用户的类方法
    @classmethod
    def delete(cls, id):
        user = cls.query.get(id)
        db.session.delete(user)
        db.session.commit()

    # 根据int类型的id查询一个用户的类方法
    @classmethod
    def find_one(cls, id):
        return cls.query.get(id)

    # 根据int类型的id查询一个用户的类方法
    @classmethod
    def update(cls, user):
        db.session.merge(user)
        db.session.commit()

    # 根据string类型的name或者string类型的phoneCode进行模糊查询所有用户的类方法
    # 在这个方法中，cls.name.like('%' + name + '%')和cls.phoneCode.like('%' + phoneCode + '%')是两个查询条件，or_函数会返回满足任一条件的结果。all()方法则是获取所有满足条件的记录。
    @classmethod
    def find_by_name_or_phone(cls, name, phoneCode):
        return cls.query.filter(or_(cls.name.like('%' + name + '%'), cls.phoneCode.like('%' + phoneCode + '%'))).all()

    '''
    filter函数在SQLAlchemy中用于构建WHERE子句，它接受一或多个条件作为参数，
    这些条件通常是模型类的属性和值之间的比较。
    在上面代码中，filter函数用于构建一个查询，该查询会返回满足指定条件的所有记录。
    filter函数接受了一个or_函数作为参数，
    or_函数接受两个条件：
    cls.name.like('%' + name + '%')和cls.phoneCode.like('%' + phoneCode + '%')。
    这两个条件分别表示name字段和phoneCode字段的值包含指定的字符串。
    or_函数表示只要满足任一条件，就会返回对应的记录。  
    all()函数则是获取所有满足条件的记录。
    如果你想获取满足条件的第一条记录，可以使用first()函数。  
    所以，cls.query.filter(or_(cls.name.like('%' + name + '%'), cls.phoneCode.like('%' + phoneCode + '%'))).all()
    这行代码的作用是查询name字段或phoneCode字段的值包含指定字符串的所有记录。
    '''