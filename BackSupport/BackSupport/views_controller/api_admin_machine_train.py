from flask import Blueprint,jsonify,request
from BackSupport.model_logic.TotalModel import DeviceAnalysis,ModelStorage,Device_Upload
from BackSupport.service_logic.service_machine_learn import ServiceMachineLearn_KNN,ServiceMachineLearn_RF,ServiceMachineLearn_SVM,ServiceMachineLearn_ensemble
from BackSupport.utils import health_level_label_util
import time,os
import pandas as pd
# 解决跨域请求
from flask_cors import CORS
# 创建服务对象，挂载dao模型
service_machine_learn = ServiceMachineLearn_KNN(DeviceAnalysis)
service_machine_learn_rf = ServiceMachineLearn_RF(DeviceAnalysis)
service_machine_learn_svm = ServiceMachineLearn_SVM(DeviceAnalysis)
service_machine_learn_svm_predict = ServiceMachineLearn_SVM(Device_Upload)
service_machine_learn_knn_predict = ServiceMachineLearn_KNN(Device_Upload)
service_machine_learn_ensemble = ServiceMachineLearn_ensemble(DeviceAnalysis)




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
    ModelPath = service_machine_learn.save_model_knn(knn_model, filename='model_knn.pkl') # 模型保存成功
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
    # 获取用户upload的数据
    data_list = service_machine_learn_knn_predict.get_data()

    # 处理为DataFrame
    column_names = ['Voltage1', 'Voltage2', 'Voltage3', 'Voltage4', 'Voltage5', 'Voltage6', 'Voltage7', 'Voltage8', 'Voltage9' , 'Voltage10', 'Voltage11', 'Voltage12','Voltage13', 'Voltage14','Voltage15','Voltage16']
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
    model = service_machine_learn.load_model_knn(r'BackSupport\resource\machine_learn_model_save\model_knn.pkl')
    # 传入模型和数据，进行预测
    predictions_numeric = service_machine_learn.predict(model, data_list_python_to_machien)
    # 使用LabelEncoder进行反向编码
    predictions_labels = service_machine_learn.inverse_transform_labels(le_loaded, predictions_numeric)
    # print("预测结果：", predictions_labels)
    # # 调用count_labels统计预测结果中各个类别的数量
    # count_labels = health_level_label_util.count_labels(predictions_labels)
    # most_common_labels = [{'label': label, 'count': count} for label, count in count_labels]
    # return jsonify({'message': 'success','data':most_common_labels})
    # 调用count_labels统计预测结果中各个类别的数量
    most_common_labels = health_level_label_util.count_labels(predictions_labels)
    # 将most_common_labels转换为字典列表的形式
    most_common_labels_dict = [{'label': label, 'count': count} for label, count in most_common_labels]
    # 返回带有最常见标签的JSON响应
    return jsonify({'message': 'success', 'data': most_common_labels_dict})

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
        rf_model_best, accuracy, best_score, le = service_machine_learn_rf.train_rf(data)
        # 保留模型得分为四位小数
        best_score = round(best_score, 4)
        # 保存LabelEncoder
        le_path = service_machine_learn_rf.save_label_encoder_rf(le) # LabelEncoder保存成功
        le_loaded = service_machine_learn_rf.load_label_encoder_rf(os.path.basename(le_path))
        print(f"LabelEncoder loaded: {le_loaded}") # LabelEncoder加载成功
        # 保存模型并返回模型保存的路径
        ModelPath = service_machine_learn_rf.save_model_rf(rf_model_best, filename='model_rf.pkl') # 模型保存成功
        # 编写一个data字典，存储模型名称ModelName,创建者CreateUser,模型路径ModelPath,是否启用IsUse。调用service_machine_learn的add_info方法，将data字典传入
        data = {
            'ModelName': 'RandomForest_cv3',
            'CreateUser': 'Admin-yangzhi',
            'ModelPath': ModelPath,
            'IsUse': 0,
            'CreateTime': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
            'ModelScore': best_score
        }
        ModelStorage.add_info(data)
        # 延迟1秒
        time.sleep(1)
        # 返回JSON数据
        return jsonify({'message':'success'})
    except Exception as e:
        print(e)
        return jsonify({'message':str(e)}),500

# 编写训练svm模型的接口,做异常处理
@api_admin_machine_train.route('/api/train_model_SVM',methods=['GET'])
def train_model_SVM():
    '''
        训练SVM模型+保存模型+保存LabelEncoder+存储模型信息到数据库
    Returns:

    '''
    # 通过try-except捕获异常
    try:
        # 获取训练数据
        data = service_machine_learn_svm.get_data_svm()
        # 训练模型
        svm_model_best, accuracy, best_score, le = service_machine_learn_svm.train_svm(data)
        # 保留模型得分为四位小数
        best_score = round(best_score, 4)
        # 保存LabelEncoder
        le_path = service_machine_learn_svm.save_label_encoder_svm(le) # LabelEncoder保存成功
        le_loaded = service_machine_learn_svm.load_label_encoder_svm(os.path.basename(le_path))
        print(f"SvM_LabelEncoder loaded: {le_loaded}") # LabelEncoder加载成功
        # 保存模型并返回模型保存的路径
        ModelPath = service_machine_learn_svm.save_model_svm(svm_model_best, filename='model_svm_cv4.pkl') # 模型保存成功
        # 编写一个data字典，存储模型名称ModelName,创建者CreateUser,模型路径ModelPath,是否启用IsUse。调用service_machine_learn的add_info方法，将data字典传入
        data = {
            'ModelName': 'SVM模型cv5',
            'CreateUser': 'Admin-yangzhi',
            'ModelPath': ModelPath,
            'IsUse': 0,
            'CreateTime': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
            'ModelScore': best_score
        }
        ModelStorage.add_info(data)
        # 延迟1秒
        time.sleep(1)
        # 返回JSON数据
        return jsonify({'message':'success'})
    except Exception as e:
        print(e)
        return jsonify({'message':str(e)}),500


# 加载训练好的SVM模型进行预测
@api_admin_machine_train.route('/api/load_model_SVM',methods=['GET'])
def load_model_SVM():
    '''
        加载训练好的SVM模型进行预测+加载LabelEncoder进行反向编码展示具体的分类结果
    Returns:

    '''
    # 指定待预测数据
    # data_list = [
    #     [4.6, 4.12, 1.74, 4.64, 1.97, 3.42, 3.42, 2.69, 0.45, 1.8, 2.58, 4, 2.92, 2.57, 1.84, 2.03],
    #     [4.6, 4.02, 1.74, 5.64, 1.97, 3.42, 3.42, 2.69, 0.45, 1.8, 2.58, 4, 2.92, 2.57, 1.84, 2.03],
    #     [4.6, 4.33, 2.74, 4.04, 1.97, 3.42, 3.42, 2.69, 0.45, 1.8, 2.58, 4, 2.92, 2.57, 1.84, 2.03],
    #     [4.6, 4.56, 2.74, 4.14, 1.97, 3.42, 3.42, 2.69, 0.45, 1.8, 2.58, 4, 2.92, 2.57, 1.84, 2.03],
    # ]
    data_list = service_machine_learn_svm_predict.get_data_svm()
    # 获取用户upload的数据
    # data_list = request.json.get('data')
    # 处理
    column_names = ['Voltage1', 'Voltage2', 'Voltage3', 'Voltage4', 'Voltage5', 'Voltage6', 'Voltage7', 'Voltage8','Voltage13', 'Voltage14']
    data_list_python_to_machien = pd.DataFrame(data_list, columns=column_names)
    # 使用正确的方法加载 LabelEncoder，并处理异常
    filename = 'label_encoder_svm_cv4.pkl'
    try:
        le_loaded = service_machine_learn_svm_predict.load_label_encoder_svm(filename)
    except (FileNotFoundError, TypeError) as e:
        print(e)
        return jsonify({'message': str(e)}), 500
    # 加载指定目录下训练好的模型
    model = service_machine_learn_svm_predict.load_model_svm(r'BackSupport\resource\machine_learn_model_save\model_svm_cv4.pkl')
    # 传入模型和数据，进行预测
    predictions_numeric = service_machine_learn_svm_predict.predict_svm(model, data_list_python_to_machien)
    # 使用LabelEncoder进行反向编码
    predictions_labels = service_machine_learn_svm_predict.inverse_transform_labels(le_loaded, predictions_numeric)
    print("预测结果：", predictions_labels)
    return jsonify({'message': 'success'})


# 训练集成学习模型的接口
@api_admin_machine_train.route('/api/train_model_ensemble',methods=['GET'])
def train_model_ensemble():
    '''
        训练集成学习模型+保存模型+保存LabelEncoder+存储模型信息到数据库
    Returns:

    '''
    # 通过try-except捕获异常
    try:
        # 获取训练数据
        data = service_machine_learn_ensemble.get_data_ensemble()
        # 集成模型
        voting_clf = service_machine_learn_ensemble.create_ensemble_models()

        ModelStorage.add_info(data)
        # 延迟1秒
        time.sleep(1)
        # 返回JSON数据
        return jsonify({'message':'success'})
    except Exception as e:
        print(e)
        return jsonify({'message':str(e)}),500
