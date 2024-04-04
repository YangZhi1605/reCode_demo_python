from flask import Flask
# 导入蓝图的py文件
from .views import AdminIndex
from .views import api_data_lineRace

def create_app():
    app = Flask(__name__)
    app.secret_key = 'yangzhi823823'

    # 注册蓝图
    app.register_blueprint(AdminIndex.adminIndex)
    app.register_blueprint(api_data_lineRace.api_data_lineRace)


    return app