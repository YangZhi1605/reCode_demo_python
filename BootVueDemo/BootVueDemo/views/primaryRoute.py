from flask import Blueprint

# 定义蓝图
indexPage = Blueprint('indexPage', __name__)

@indexPage.route('/')
def index():

    return '蓝图下的首页'