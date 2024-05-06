import json

from flask import request, jsonify, Blueprint
from BackSupport.model_logic.TotalModel import Cart,CartAddress,Order
from BackSupport.service_logic.service_front_cart import ServiceFrontCart,ServiceFrontAddress,ServiceFrontOrder
# 导入跨域支持
from flask_cors import CORS
# from china_region import get_provinces, get_cities_by_province
# 挂载dao模型到服务类
serviceFrontCart = ServiceFrontCart(Cart)
serviceFrontAddress = ServiceFrontAddress(CartAddress)
serviceFrontOrder = ServiceFrontOrder(Order)
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

# 获取收货地址的路由
@api_data_op_cart.route('/api/get_address_info', methods=['GET'])
def get_address_info():
    # 获取收货地址信息
    result = serviceFrontAddress.get_all()
    result = [i.to_dict() for i in result]
    return jsonify({
        'success': True,
        'message': '获取成功',
        'data': result
    }), 200

# 获取chinese_regions，处理为json反馈给前台用于省市区三级联动
@api_data_op_cart.route('/api/get_chinese_regions', methods=['GET'])
def get_chinese_regions():
    # 获取resource文件夹下data文件夹中的region.json文件，反馈给前台
    with open('BackSupport/resource/data/region.json', 'r', encoding='utf-8') as f:
        data = json.load(f)  # 使用 json.load 而不是 f.read()

    return jsonify(data), 200

# 根据id和传入的数据更新收货地址信息的路由
@api_data_op_cart.route('/api/update_address_info', methods=['POST'])
def update_address_info():
    # 获取传入的数据
    data = request.json
    print('得到的数据',data)
    id = int(data['id'])
    # 更新收货地址信息
    result = serviceFrontAddress.update_info(id, data)
    return jsonify({
        'success': True,
        'message': '更新成功',
        'data': result
    }), 200

# 编写根据前台传递的数据添加收货地址信息的路由
@api_data_op_cart.route('/api/add_address_info', methods=['POST'])
def add_address_info():
    # 获取传入的数据
    data = request.json
    print('得到的数据',data)
    # 添加收货地址信息
    result = serviceFrontAddress.add_info(data)
    return jsonify({
        'success': True,
        'message': '添加成功',
        'data': result
    }), 200

# 编写根据传入的id删除收货地址信息的路由
@api_data_op_cart.route('/api/delete_address_info', methods=['POST'])
def delete_address_info():
    # 获取传入的数据
    data = request.json
    id = int(data['id'])
    # 删除收货地址信息
    result = serviceFrontAddress.delete_info(id)
    return jsonify({
        'success': True,
        'message': '删除成功',
        'data': result
    }), 200

# 编写根据传入的id和选中状态isUse更新收货地址信息的路由
@api_data_op_cart.route('/api/update_isUse', methods=['POST'])
def update_isUse():
    # 获取传入的数据
    data = request.json
    id = int(data['id'])
    print('得到的数据',data)
    # 更新收货地址信息
    result = serviceFrontAddress.update_isUse(id, data)
    return jsonify({
        'success': True,
        'message': '更新成功',
        'data': result
    }), 200

# 接受前台传递的订单信息，暂时只是打印的接口函数
@api_data_op_cart.route('/api/submit_order', methods=['POST'])
def submit_order():
    # 获取传入的数据
    data = request.json
    print('得到的数据',data)
    '''
    举例：
    得到的数据 {
        'userInfo': { 'id': 1 }, # 用户id
        'addressInfo': { 'id': 1 }, # 收货地址id
        'cartList': [{'id': 1}, {'id': 2}], # 购物车列表，只需要每个商品的id
        'totalPrice': 2903.8900000000003, 
        'itemCount': 14
    }
    '''
    # 我目前得到的数据
    # 得到的数据 {'userInfo': {}, 'addressInfo': {'id': 1, 'isUse': True, 'receiverAddress': '海科路东段99号', 'receiverCity': '天津市', 'receiverDistrict': '和平区', 'receiverMobile': '13918562354', 'receiverName': '杨枝', 'receiverProvince': '天津市'}, 'cartList': [{'cartTotalQuantity': 5, 'id': 4, 'name': '轮胎', 'price': 674.67, 'selected': 1, 'total': 3373.35}], 'totalPrice': 3373.35, 'itemCount': 5}
    # 调用服务类的createOrder方法，创建订单
    result = serviceFrontOrder.createOrder(data)
    return jsonify({
        'success': True,
        'message': '提交成功',
        'data': data
    }), 200

# 编写根据前台传递的购物车信息实现删除的接口
@api_data_op_cart.route('/api/delete_cart_items', methods=['POST'])
def delete_cart_items():
    # 获取传入的数据
    data = request.json
    print('得到的数据',data)
    # 提取购物车项目的ID
    cartIds = [item['id'] for item in data['cartList']]

    # 删除购物车信息
    result = serviceFrontCart.deactivateCartItems(cartIds)
    return jsonify({
        'success': True,
        'message': '删除成功',
        'data': result
    }), 200

# 编写根据前台传递的订单
@api_data_op_cart.route('/api/get_order_info', methods=['GET'])
def get_order_info():
    # 获取订单信息
    result = serviceFrontOrder.get_all_orders_details()
    # result = [i.to_dict() for i in result]
    return jsonify({
        'success': True,
        'message': '获取成功',
        'data': result
    }), 200