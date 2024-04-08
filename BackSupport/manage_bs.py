# 导入create_app函数，创建app对象
from BackSupport import create_app
# 导入解决跨域问题的flask_cors模块
from flask_cors import CORS
app = create_app()
CORS(app)

if __name__ == '__main__':
    app.run(debug=True)