from BootVueDemo.utils.sqlhelper import def_fetchall
from flask import jsonify
# 这里没有用单元测试，是不正规的，但是为了方便演示，我直接在这里调用了def_fetchall方法
# 编写t_user中查询所有用户的sql语句
sql = 'select * from t_user'
# 调用def_fetchall方法，传入sql语句，获取查询结果
users = def_fetchall(sql)
# 打印查询结果
print(jsonify(users))