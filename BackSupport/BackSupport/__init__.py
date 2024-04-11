from flask import Flask
# 导入蓝图的py文件
from .views_controller import AdminIndex
from .views_controller import api_data_op
# 导入的config包下的setting模块中的Config类
from .config.setting import Config
# 导入model_logic包下的VoltageModle模块中的db对象
from .model_logic.VoltageModel import db


def create_app():
    app = Flask(__name__)
    app.secret_key = 'yangzhi823823'

    # 加载配置文件
    app.config.from_object(Config)
    # 初始化db
    db.init_app(app)
    # 初始化migrate
    # Migrate(app, db)

    # 注册蓝图
    app.register_blueprint(AdminIndex.adminIndex)
    app.register_blueprint(api_data_op.api_data_op)


    return app