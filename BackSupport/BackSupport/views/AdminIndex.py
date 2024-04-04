from flask import Blueprint

# 创建蓝图对象
adminIndex = Blueprint('adminIndex', __name__)

# 编写视图函数,首页默认的视图函数
@adminIndex.route('/')
def index():
    return 'adminIndex搭建好，启动成功！'