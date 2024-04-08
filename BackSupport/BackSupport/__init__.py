from flask import Flask
# 导入蓝图的py文件
from .views_controller import AdminIndex
from .views_controller import api_data_op

def create_app():
    app = Flask(__name__)
    app.secret_key = 'yangzhi823823'

    # 注册蓝图
    app.register_blueprint(AdminIndex.adminIndex)
    app.register_blueprint(api_data_op.api_data_op)


    return app