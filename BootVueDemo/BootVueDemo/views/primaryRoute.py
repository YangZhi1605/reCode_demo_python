from flask import Blueprint

# 定义蓝图
user = Blueprint('user', __name__)

@user.route('/')
def index():

    return '蓝图下的首页'