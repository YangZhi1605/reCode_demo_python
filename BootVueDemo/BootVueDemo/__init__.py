from flask import Flask
from flask_migrate import Migrate
# 我导入的config包下的setting模块中的Config类
from .config.setting import Config
# 导入utils包下的models模块中的db对象
from .utils.models import db
# 导入views包下的primaryRoute模块中的user蓝图对象
from .views.primaryRoute import indexPage
from .views.user_controller import user_controller



def create_app():
    app = Flask(__name__)
    app.secret_key = 'yangzhi823823'
    # 加载配置文件
    app.config.from_object(Config)
    # 初始化db
    db.init_app(app)
    # 初始化migrate
    Migrate(app, db)
    # 注册蓝图
    app.register_blueprint(indexPage, url_prefix='/admin')
    app.register_blueprint(user_controller, url_prefix='/admin')


    return app