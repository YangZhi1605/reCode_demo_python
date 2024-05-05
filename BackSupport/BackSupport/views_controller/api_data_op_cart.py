from flask import request, jsonify, Blueprint
from BackSupport.model_logic.TotalModel import Cart
from BackSupport.service_logic.service_front_cart import ServiceFrontCart
# 导入跨域支持
from flask_cors import CORS
# 挂载dao模型到服务类
serviceFrontCart = ServiceFrontCart(Cart)
# 创建蓝图
api_data_op_cart = Blueprint('api_data_op_cart', __name__)
# 解决跨域请求
CORS(api_data_op_cart)

# 创建获取购物车信息的路由
@api_data_op_cart.route('/api/get_cart_info', methods=['GET'])
def get_cart_info():
    # 获取购物车信息
    result = serviceFrontCart.get_all()
    result = [i.to_dict() for i in result]
    return jsonify({
        'success': True,
        'message': '获取成功',
        'data': result
    }), 200

# 创建根据传入id更新购物车商品数量和总价的路由
@api_data_op_cart.route('/api/update_cart_info', methods=['POST'])
def update_cart_info():
    # 获取传入的数据
    data = request.json
    id = int(data['id'])
    # 更新购物车信息
    result = serviceFrontCart.update_info(id, data)
    # result = [i.to_dict() for i in result]
    return jsonify({
        'success': True,
        'message': '更新成功',
        'data': result
    }), 200

# 创建根据传入的商品id列表更新购物车商品选中状态的路由
@api_data_op_cart.route('/api/update_selected_status', methods=['POST'])
def update_selected_status():
    # 获取传入的数据
    items_dict = request.json
    # 更新购物车商品选中状态
    result = serviceFrontCart.update_selected_status(items_dict)
    return jsonify({
        'success': True,
        'message': '更新成功',
        'data': result
    }), 200

# 创建根据传入的id删除购物车商品的路由
@api_data_op_cart.route('/api/delete_cart_info', methods=['POST'])
def delete_cart_info():
    # 获取传入的数据
    data = request.json
    id = int(data['id'])
    # 删除购物车信息
    result = serviceFrontCart.delete_info(id)
    return jsonify({
        'success': True,
        'message': '删除成功',
        'data': result
    }), 200

# 创建根据传入的商品信息添加购物车商品的路由
@api_data_op_cart.route('/api/add_cart_info', methods=['POST'])
def add_cart_info():
    # 获取传入的数据
    data = request.json
    print('得到的数据',data)
    # 添加购物车信息
    result = serviceFrontCart.add_info(data)
    print('添加后的数据',result)
    return jsonify({
        'success': True,
        'message': '添加成功',
        'data': result
    }), 200