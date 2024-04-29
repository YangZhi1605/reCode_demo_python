from flask import Blueprint,jsonify,request
from BackSupport.model_logic.TotalModel import DeviceAnalysis,ModelStorage
from BackSupport.service_logic.service_machine_learn import ServiceMachineLearn_KNN,ServiceMachineLearn_RF
import time,os
import pandas as pd
# 解决跨域请求
from flask_cors import CORS
# 创建服务对象，挂载dao模型
service_machine_learn = ServiceMachineLearn_KNN(DeviceAnalysis)
service_machine_learn_rf = ServiceMachineLearn_RF(DeviceAnalysis)
# 创建蓝图
api_admin_machine_train = Blueprint('api_admin_machine_train', __name__)
CORS(api_admin_machine_train)

# 编写训练KNN模型的接口
@api_admin_machine_train.route('/api/train_model_KNN',methods=['GET'])
def train_model_KNN():
    '''
        训练KNN模型+保存模型+保存LabelEncoder+存储模型信息到数据库
    Returns:

    '''
    # 获取训练数据
    data = service_machine_learn.get_data()
    # 训练模型
    knn_model, accuracy, f1_score, le = service_machine_learn.train_knn(data)
    # # 保存LabelEncoder
    # service_machine_learn.save_label_encoder(le, filename='label_encoder.pkl')
    # 在保存后立即尝试加载
    le_path = service_machine_learn.save_label_encoder(le) # LabelEncoder保存成功
    le_loaded = service_machine_learn.load_label_encoder(os.path.basename(le_path))
    print(f"LabelEncoder loaded: {le_loaded}") # LabelEncoder加载成功
    # 保存模型并返回模型保存的路径
    ModelPath = service_machine_learn.save_model(knn_model, filename='model_knn.pkl') # 模型保存成功
    # 打印评估指标
    print(f"这是模型的精度Accuracy: {accuracy}")
    print(f"这是模型的F1 Score: {f1_score}")
    # 编写一个data字典，存储模型名称ModelName,创建者CreateUser,模型路径ModelPath,是否启用IsUse。调用service_machine_learn的add_info方法，将data字典传入
    data = {
        'ModelName': 'KNN',
        'CreateUser': 'Admin',
        'ModelPath': ModelPath,
        'IsUse': 0,
        'CreateTime': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    }
    ModelStorage.add_info(data)

    # 延迟3秒
    time.sleep(1)
    # 返回JSON数据
    return jsonify({'message':'success'})

# 编写测试加载模型的接口
@api_admin_machine_train.route('/api/load_model_KNN',methods=['GET'])
def load_model_KNN():
    '''
        加载训练好的模型进行预测+加载LabelEncoder进行反向编码展示具体的分类结果
    Returns:

    '''
    # 指定待预测数据
    data_list = [
        [4.6, 4.12, 1.74, 4.64, 1.97, 3.42, 3.42, 2.69, 0.45, 1.8, 2.58, 4, 2.92, 2.57, 1.84, 2.03],
        [4.6, 4.02, 1.74, 5.64, 1.97, 3.42, 3.42, 2.69, 0.45, 1.8, 2.58, 4, 2.92, 2.57, 1.84, 2.03],
        [4.6, 4.33, 2.74, 4.04, 1.97, 3.42, 3.42, 2.69, 0.45, 1.8, 2.58, 4, 2.92, 2.57, 1.84, 2.03],
        [4.6, 4.56, 2.74, 4.14, 1.97, 3.42, 3.42, 2.69, 0.45, 1.8, 2.58, 4, 2.92, 2.57, 1.84, 2.03],
    ]
    # 处理为DataFrame
    column_names = ['Voltage1', 'Voltage2', 'Voltage3', 'Voltage4', 'Voltage5', 'Voltage6', 'Voltage7', 'Voltage8',
                    'Voltage9', 'Voltage10', 'Voltage11', 'Voltage12', 'Voltage13', 'Voltage14', 'Voltage15',
                    'Voltage16']
    data_list_python_to_machien = pd.DataFrame(data_list, columns=column_names)

    # # 使用正确的方法加载 LabelEncoder，并处理异常 —— 阴差阳错，原本只是需要传入文件名，但是这里传入了文件路径却跑起来了
    # try:
    #     le_path = r'BackSupport\resource\machine_learn_model_save\label_encoder.pkl'
    #     le_loaded = service_machine_learn.load_label_encoder(os.path.basename(le_path))
    # except (FileNotFoundError, TypeError) as e:
    #     print(e)  # 打印错误信息便于调试
    #     return jsonify({'message': str(e)}), 500  # 返回500内部服务器错误
    filename = 'label_encoder.pkl'
    try:
        le_loaded = service_machine_learn.load_label_encoder(filename)
    except (FileNotFoundError, TypeError) as e:
        print(e)  # 打印错误信息便于调试
        return jsonify({'message': str(e)}), 500  # 返回500内部服务器错误

    # 加载指定目录下训练好的模型
    model = service_machine_learn.load_model(r'BackSupport\resource\machine_learn_model_save\model_knn.pkl')
    # 传入模型和数据，进行预测
    predictions_numeric = service_machine_learn.predict(model, data_list_python_to_machien)
    # 使用LabelEncoder进行反向编码
    predictions_labels = service_machine_learn.inverse_transform_labels(le_loaded, predictions_numeric)
    print("预测结果：", predictions_labels)
    return jsonify({'message': 'success'})

# 编写训练随机森林模型的接口
@api_admin_machine_train.route('/api/train_model_RF',methods=['GET'])
def train_model_RF():
    '''
        训练随机森林模型+保存模型+保存LabelEncoder+存储模型信息到数据库
    Returns:

    '''
    # 通过try-except捕获异常
    try:
        # 获取训练数据
        data = service_machine_learn_rf.get_data_rf()
        # 训练模型
        rf_model,  accuracy, best_score, le = service_machine_learn_rf.train_rf(data)
        # 保存LabelEncoder
        le_path = service_machine_learn_rf.save_label_encoder_rf(le) # LabelEncoder保存成功
        le_loaded = service_machine_learn_rf.load_label_encoder_rf(os.path.basename(le_path))
        print(f"LabelEncoder loaded: {le_loaded}") # LabelEncoder加载成功
        # 保存模型并返回模型保存的路径
        ModelPath = service_machine_learn.save_model(rf_model, filename='model_rf.pkl') # 模型保存成功
        # 编写一个data字典，存储模型名称ModelName,创建者CreateUser,模型路径ModelPath,是否启用IsUse。调用service_machine_learn的add_info方法，将data字典传入
        data = {
            'ModelName': 'RandomForest',
            'CreateUser': 'Admin-yangzhi',
            'ModelPath': ModelPath,
            'IsUse': 0,
            'CreateTime': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        }
        ModelStorage.add_info(data)
        # 延迟1秒
        time.sleep(1)
        # 返回JSON数据
        return jsonify({'message':'success'})
    except Exception as e:
        print(e)
        return jsonify({'message':str(e)}),500
