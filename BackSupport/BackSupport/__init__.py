from flask import Flask
# 导入蓝图的py文件
from .views_controller import AdminIndex
from .views_controller import api_data_op_wrben1_3
from .views_controller import api_data_op_wrben2
from .views_controller import api_admin_data_system
from .views_controller import api_data_op_maintaininfo
from .views_controller import api_admin_machine_manage
from .views_controller import api_admin_adminUser
from .views_controller import api_admin_machine_train
from .views_controller import api_data_op_userinfo_manage
# 导入的config包下的setting模块中的Config类
from .config.setting import Config
# 导入model_logic包下的VoltageModle模块中的db对象,即SQLAlchemy对象是需要在__init__.py中导入并初始化的
from .model_logic.TotalModel import db
# 导入发送邮件的模块
from flask_mail import Mail, Message


def create_app():
    app = Flask(__name__)
    app.secret_key = 'yangzhi823823'

    # 加载配置文件
    app.config.from_object(Config)
    # 初始化db，一个flask应用只能有一个db
    db.init_app(app)
    # 初始化migrate
    # Migrate(app, db)

    # 注册蓝图
    app.register_blueprint(AdminIndex.adminIndex)
    app.register_blueprint(api_data_op_wrben1_3.api_data_op_wrben1_3)
    app.register_blueprint(api_data_op_wrben2.api_data_op_wrben2)
    app.register_blueprint(api_admin_data_system.api_admin_data_system)
    app.register_blueprint(api_data_op_maintaininfo.api_data_op_maintaininfo)
    app.register_blueprint(api_admin_machine_manage.api_admin_machine_manage)
    app.register_blueprint(api_admin_adminUser.api_admin_adminUser)
    app.register_blueprint(api_admin_machine_train.api_admin_machine_train)
    app.register_blueprint(api_data_op_userinfo_manage.api_data_op_userinfo_manage)

    # 初始化邮件发送对象
    mail = Mail(app)
    # 邮件配置
    app.config['MAIL_SERVER'] = 'smtp.163.com'
    app.config['MAIL_PORT'] = 465  # 端口号，根据是否使用SSL/TLS选择端口
    app.config['MAIL_USE_TLS'] = False  # 网易邮箱中不使用TLS，根据邮箱服务提供商的要求设置
    app.config['MAIL_USE_SSL'] = True  # 网易邮箱使用了SSL，根据邮箱服务提供商的要求设置
    app.config['MAIL_USERNAME'] = 'yangzhi15791605@163.com'  # 将your_email@163.com替换为我的163邮箱地址
    app.config['MAIL_PASSWORD'] = 'LQSGAYMZXFPPJKHW'  # 将your_email_authorization_code替换为我的163邮箱授权码
    app.config['MAIL_DEFAULT_SENDER'] = 'yangzhi15791605@163.com'  # 发件人邮箱地址
    mail.init_app(app)


    return app