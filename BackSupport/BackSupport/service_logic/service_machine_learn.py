'''
机器学习模型的代码应该放在服务（service）层。
通常，控制器（controller）层负责处理HTTP请求和响应，
模型（model）层负责数据库交互，而服务（service）层则负责实现应用的业务逻辑。
由于训练机器学习模型是业务逻辑的一部分，因此应该将这部分代码放在服务层。
'''
import pandas as pd
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
import joblib
import os

# 加入网格搜索和交叉验证的包
from sklearn.model_selection import  GridSearchCV,RandomizedSearchCV
# 标签（十分健康、健康、正常、轻微严重，十分严重），它们看起来带有顺序关系，标签编码可能更适合
from sklearn.preprocessing import LabelEncoder


# 编写一个服务类，用于训练KNN模型算法
class ServiceMachineLearn_KNN:
    def __init__(self, data_dao):
        self.data_dao = data_dao

    # 从数据库中获取数据
    def get_data(self):
        '''
        从数据库中获取数据并转换为DataFrame
        Returns:
            data: DataFrame
        '''
        # 获取所有数据
        data = self.data_dao.get_all()
        # 将数据转换为DataFrame , 直接将字典列表转换为DataFrame
        data = pd.DataFrame([result.to_dict() for result in data])
        return data

    # 训练KNN模型
    def train_knn(self, data):
        '''
            用LabelEncoder将分类目标编码为数值，
            然后在拆分数据集，创建KNN分类器，训练模型并进行预测。
            还需要包含对模型的评估过程，
            如通过准确度、混淆矩阵、F1分数等度量来评估预测的准确性。
            这些评估步骤可以通过导入和使用sklearn.metrics模块中相应的函数完成
        Args:
            data:

        Returns:

        '''
        # 首先特征工程
        # 目前按照我的主观理解来进行特征抽取和特征预处理。特征降维待定
        # 筛选出特征值
        feature = data[
            ["Voltage1", "Voltage2", "Voltage3", "Voltage4", "Voltage5", "Voltage6", "Voltage7", "Voltage8", "Voltage9",
             "Voltage10", "Voltage11", "Voltage12", "Voltage13", "Voltage14", "Voltage15", "Voltage16"]
        ]
        target = data["HealthLevel"]
        # 创建LabelEncoder对象
        le = LabelEncoder()

        # 对目标列进行编码
        target_encoded = le.fit_transform(target)
        # 1.1 划分测试集
        x_train, x_test, y_train, y_test = train_test_split(feature, target_encoded, test_size=0.2, random_state=42)
        # 创建KNN分类器实例
        knn = KNeighborsClassifier()
        # 训练模型
        knn.fit(x_train, y_train)
        # 模型评估
        y_predict = knn.predict(x_test)
        print("y_predict:\n", y_predict)
        print("直接比对真实值和预测值:\n", y_test == y_predict)
        # 准确度
        accuracy = knn.score(x_test, y_test)
        # 混淆矩阵
        y_pred = knn.predict(x_test)
        # F1分数
        f1_score = metrics.f1_score(y_test, y_pred, average='micro')
        # 返回该模型和评估指标,在返回模型和评估指标的同时，也返回这个LabelEncoder对象
        return knn, accuracy, f1_score, le

    # 保存 LabelEncoder
    def save_label_encoder(self, le, filename='label_encoder.pkl'):
        model_directory = os.path.join('BackSupport', 'resource', 'machine_learn_model_save')
        if not os.path.exists(model_directory):
            os.makedirs(model_directory)
        file_path = os.path.join(model_directory, filename)
        joblib.dump(le, file_path)
        print(f"LabelEncoder被保存到 {file_path}")
        return file_path

    # 加载 LabelEncoder对象
    def load_label_encoder(self, filename):
        model_directory = os.path.join('BackSupport', 'resource', 'machine_learn_model_save')
        file_path = os.path.join(model_directory, filename)
        # 确保文件确实存在
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"LabelEncoder file not found: {file_path}")

        # 确保返回的是 LabelEncoder 对象
        le = joblib.load(file_path)
        if not isinstance(le, LabelEncoder):
            raise TypeError(f"The file {file_path} does not contain a valid LabelEncoder object.")

        return le

    # 将数值预测转换为文本标签
    def inverse_transform_labels(self, le, y_pred):
        return le.inverse_transform(y_pred)

    # 保存训练出来的模型
    def save_model_knn(self, model, filename='model_knn.pkl'):
        # 设置模型保存的目录
        model_directory = os.path.join('BackSupport', 'resource', 'machine_learn_model_save')
        # 检查目录是否存在，如果不存在则创建
        if not os.path.exists(model_directory):
            os.makedirs(model_directory)
        # 创建模型文件的完整路径
        file_path = os.path.join(model_directory, filename)
        # 保存模型到指定目录
        joblib.dump(model, file_path)
        print(f"模型已经被保存到 {file_path}")
        # 返回模型保存的路径
        return file_path


    # 加载模型
    def load_model_knn(self, filename):
        # 加载模型
        model = joblib.load(filename)
        print(f"Model loaded from {filename}")
        return model

    # 调用模型去预测
    def predict(self, model, data):
        # 这里假设data是一个可以直接用于预测的DataFrame
        # 如果实际的数据需要额外的预处理，您需要先进行预处理
        # 下面是一个简单的预处理示例，假设我们需要所有的特征列
        feature_columns = ["Voltage1", "Voltage2", "Voltage3", "Voltage4", "Voltage5", "Voltage6",
                           "Voltage7", "Voltage8", "Voltage9", "Voltage10", "Voltage11", "Voltage12",
                           "Voltage13", "Voltage14", "Voltage15", "Voltage16"]
        feature_data = data[feature_columns]

        # 使用模型进行预测
        predictions = model.predict(feature_data)

        # 打印预测结果
        print(f"Predictions: {predictions}")

        return predictions




# 编写一个服务类，用于训练随机森林模型算法
class ServiceMachineLearn_RF:
    def __init__(self, data_dao):
        self.data_dao = data_dao

    # 从数据库中获取数据
    def get_data_rf(self):
        '''
        从数据库中获取数据并转换为DataFrame
        Returns:
            data: DataFrame
        '''
        # 获取所有数据
        data = self.data_dao.get_all()
        # 将数据转换为DataFrame , 直接将字典列表转换为DataFrame
        data = pd.DataFrame([result.to_dict() for result in data])
        return data

    # 训练随机森林模型
    def train_rf(self, data):
        '''
            用LabelEncoder将分类目标编码为数值，
            然后在拆分数据集，创建随机森林分类器，训练模型并进行预测。
            还需要包含对模型的评估过程，
            如通过准确度、混淆矩阵、F1分数等度量来评估预测的准确性。
            这些评估步骤可以通过导入和使用sklearn.metrics模块中相应的函数完成
        Args:
            data:

        Returns:

        '''
        # 首先特征工程
        # 目前按照我的主观理解来进行特征抽取和特征预处理。特征降维待定
        # 筛选出特征值
        feature = data[
            ["Voltage1", "Voltage2", "Voltage3", "Voltage4", "Voltage5", "Voltage6", "Voltage7", "Voltage8", "Voltage9",
             "Voltage10", "Voltage11", "Voltage12", "Voltage13", "Voltage14", "Voltage15", "Voltage16"]
        ]
        target = data["HealthLevel"]
        # 创建LabelEncoder对象
        le = LabelEncoder()

        # 对目标列进行编码
        target_encoded = le.fit_transform(target)
        # 1.1 划分测试集
        x_train, x_test, y_train, y_test = train_test_split(feature, target_encoded, test_size=0.2, random_state=42)
        # 将训练集和测试集进行标准化
        scaler = StandardScaler()
        x_train = scaler.fit_transform(x_train)
        x_test = scaler.transform(x_test)
        # 创建随机森林分类器实例
        rf = RandomForestClassifier()
        # 超参数处理搜一个合适的+交叉验证
        # 设置参数
        param_grid = {
            'n_estimators': [5, 50, 100, 150,200],
            'max_depth': [5, 10, 15],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4]
        }
        # 确定交叉验证的次数
        cv = 3
        # 创建GridSearchCV对象
        grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=cv, n_jobs=-1)
        # 训练模型
        grid_search.fit(x_train, y_train)
        # 分类算法的模型评估比较类似
        # 模型评估
        # 方法一：直接比较真实值和预测值
        y_predict = grid_search.predict(x_test)
        print("y_predict:\n", y_predict)
        print("直接比对真实值和预测值:\n", y_test == y_predict)

        # 方法二：计算准确度
        accuracy = grid_search.score(x_test, y_test)
        print(f"准确度: {accuracy}")

        # 最佳参数
        best_params = grid_search.best_params_
        print(f"最佳参数: {best_params}")
        # 最佳结果
        best_score = grid_search.best_score_
        print(f"最佳结果: {best_score}")
        # 最佳估计器
        best_estimator = grid_search.best_estimator_
        print(f"最佳估计器: {best_estimator}")
        # 交叉验证结果
        cv_results = grid_search.cv_results_
        print(f"交叉验证结果: {cv_results}")
        # 返回该模型和评估指标,在返回模型和评估指标的同时，也返回这个LabelEncoder对象
        return best_estimator, accuracy, best_score, le

    # 保存 随机森林的LabelEncoder
    def save_label_encoder_rf(self, le, filename='label_encoder_rf_cv3.pkl'):
        model_directory = os.path.join('BackSupport', 'resource', 'machine_learn_model_save')
        if not os.path.exists(model_directory):
            os.makedirs(model_directory)
        file_path = os.path.join(model_directory, filename)
        joblib.dump(le, file_path)
        print(f"随机森林的LabelEncoder被保存到 {file_path}")
        return file_path

    # 加载 随机森林的LabelEncoder对象
    def load_label_encoder_rf(self, filename):
        model_directory = os.path.join('BackSupport', 'resource', 'machine_learn_model_save')
        file_path = os.path.join(model_directory, filename)
        # 确保文件确实存在
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"LabelEncoder file not found: {file_path}")

        # 确保返回的是 LabelEncoder 对象
        le = joblib.load(file_path)
        if not isinstance(le, LabelEncoder):
            raise TypeError(f"The file {file_path} does not contain a valid LabelEncoder object.")

        return le

    # 将数值预测转换为文本标签
    def inverse_transform_labels(self, le, y_pred):
        return le.inverse_transform(y_pred)

    # 保存训练出来的模型
    def save_model_rf(self, model, filename='model_rf_cv3.pkl'):
        # 设置模型保存的目录
        model_directory = os.path.join('BackSupport', 'resource', 'machine_learn_model_save')
        # 检查目录是否存在，如果不存在则创建
        if not os.path.exists(model_directory):
            os.makedirs(model_directory)
        # 创建模型文件的完整路径
        file_path = os.path.join(model_directory, filename)
        # 保存模型到指定目录
        joblib.dump(model, file_path)
        print(f"随机森林模型已经被保存到 {file_path}")
        # 返回模型保存的路径
        return file_path

    # 加载模型
    def load_model_rf(self, filename):
        # 加载模型
        model = joblib.load(filename)
        print(f"Model loaded from {filename}")
        return model

    # 调用模型去预测
    def predict_rf(self, model, data):
        # 这里假设data是一个可以直接用于预测的DataFrame
        # 如果实际的数据需要额外的预处理，您需要先进行预处理
        # 下面是一个简单的预处理示例，假设我们需要所有的特征列
        feature_columns = ["Voltage1", "Voltage2", "Voltage3", "Voltage4", "Voltage5", "Voltage6",
                           "Voltage7", "Voltage8", "Voltage9", "Voltage10", "Voltage11", "Voltage12",
                           "Voltage13", "Voltage14", "Voltage15", "Voltage16"]
        feature_data = data[feature_columns]
        # 使用模型进行预测
        predictions = model.predict(feature_data)
        # 打印预测结果
        print(f"Predictions: {predictions}")
        return predictions


# 编写一个服务类，用于训练SVM模型算法
class ServiceMachineLearn_SVM:
    def __init__(self, data_dao):
        self.data_dao = data_dao

    # 从数据库中获取数据
    def get_data_svm(self):
        '''
        从数据库中获取数据并转换为DataFrame
        Returns:
            data: DataFrame
        '''
        # 获取所有数据
        data = self.data_dao.get_all()
        # 将数据转换为DataFrame , 直接将字典列表转换为DataFrame
        data = pd.DataFrame([result.to_dict() for result in data])
        return data

    # 训练SVM模型
    def train_svm(self, data):
        '''
            用LabelEncoder将分类目标编码为数值，
            然后在拆分数据集，创建SVM分类器，训练模型并进行预测。
            还需要包含对模型的评估过程，
            如通过准确度、混淆矩阵、F1分数等度量来评估预测的准确性。
            这些评估步骤可以通过导入和使用sklearn.metrics模块中相应的函数完成
        Args:
            data:

        Returns:

        '''
        # 首先特征工程
        # 目前按照我的主观理解来进行特征抽取和特征预处理。特征降维待定
        # 筛选出特征值，这次我只用12个特征

        feature = data[
            ["Voltage1", "Voltage2", "Voltage3", "Voltage4", "Voltage5", "Voltage6", "Voltage7", "Voltage8", "Voltage13", "Voltage14"]
        ]
        target = data["HealthLevel"]
        # 创建LabelEncoder对象
        le = LabelEncoder()

        # 对目标列进行编码
        target_encoded = le.fit_transform(target)
        # 1.1 划分测试集
        x_train, x_test, y_train, y_test = train_test_split(feature, target_encoded, test_size=0.2, random_state=42)
        # 将训练集和测试集进行标准化
        scaler = StandardScaler()
        x_train = scaler.fit_transform(x_train)
        x_test = scaler.transform(x_test)
        # 创建SVM分类器实例
        svm = SVC()
        # 超参数处理搜一个合适的+交叉验证
        # 设置参数
        param_grid = {
            # C是惩罚系数，其越大，拟合程度可能越大，gamma是核函数的系数
            'C':[0.001, 0.01, 0.5],
            'gamma': ['scale', 'auto'],
            # kernel： 核函数类型，常见的有'linear'（线性）,'poly'（多项式）,'rbf'（径向基函数）
            'kernel': ['linear', 'rbf', 'poly']
        }
        # 确定交叉验证的次数
        cv = 5
        # 创建GridSearchCV对象
        grid_search = GridSearchCV(estimator=svm, param_grid=param_grid, cv=cv, n_jobs=-1)
        # 训练模型
        grid_search.fit(x_train, y_train)
        # 分类算法的模型评估比较类似
        # 模型评估
        # 方法一：直接比较真实值和预测值
        y_predict = grid_search.predict(x_test)
        print("y_predict:\n", y_predict)
        print("直接比对真实值和预测值:\n", y_test == y_predict)
        # 方法二：计算准确度
        accuracy = grid_search.score(x_test, y_test)
        print(f"准确度: {accuracy}")

        # 最佳参数
        best_params = grid_search.best_params_
        print(f"最佳参数: {best_params}")
        # 最佳结果
        best_score = grid_search.best_score_
        print(f"最佳结果: {best_score}")
        # 最佳估计器
        best_estimator = grid_search.best_estimator_
        print(f"最佳估计器: {best_estimator}")
        # 交叉验证结果
        cv_results = grid_search.cv_results_
        print(f"交叉验证结果: {cv_results}")
        # 返回该模型和评估指标,在返回模型和评估指标的同时，也返回这个LabelEncoder对象
        return best_estimator, accuracy, best_score,le

    # 保存 SVM的LabelEncoder
    def save_label_encoder_svm(self, le, filename='label_encoder_svm_cv5.pkl'):
        model_directory = os.path.join('BackSupport', 'resource', 'machine_learn_model_save')
        if not os.path.exists(model_directory):
            os.makedirs(model_directory)
        file_path = os.path.join(model_directory, filename)
        joblib.dump(le, file_path)
        print(f"SVM的LabelEncoder被保存到 {file_path}")
        return file_path
    # 加载 SVM的LabelEncoder对象
    def load_label_encoder_svm(self, filename):
        model_directory = os.path.join('BackSupport', 'resource', 'machine_learn_model_save')
        file_path = os.path.join(model_directory, filename)
        # 确保文件确实存在
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"LabelEncoder file not found: {file_path}")

        # 确保返回的是 LabelEncoder 对象
        le = joblib.load(file_path)
        if not isinstance(le, LabelEncoder):
            raise TypeError(f"The file {file_path} does not contain a valid LabelEncoder object.")

        return le

    # 将数值预测转换为文本标签
    def inverse_transform_labels(self, le, y_pred):
        return le.inverse_transform(y_pred)
    # 保存训练出来的模型
    def save_model_svm(self, model, filename='model_svm_cv5.pkl'):
        # 设置模型保存的目录
        model_directory = os.path.join('BackSupport', 'resource', 'machine_learn_model_save')
        # 检查目录是否存在，如果不存在则创建
        if not os.path.exists(model_directory):
            os.makedirs(model_directory)
        # 创建模型文件的完整路径
        file_path = os.path.join(model_directory, filename)
        # 保存模型到指定目录
        joblib.dump(model, file_path)
        print(f"SVM模型已经被保存到 {file_path}")
        # 返回模型保存的路径
        return file_path
    # 加载模型
    def load_model_svm(self, filename):
        # 加载模型
        model = joblib.load(filename)
        print(f"Model loaded from {filename}")
        return model
    # 调用模型去预测
    def predict_svm(self, model, data):
        # 这里假设data是一个可以直接用于预测的DataFrame
        # 如果实际的数据需要额外的预处理，您需要先进行预处理
        # 下面是一个简单的预处理示例，假设我们需要所有的特征列
        feature_columns = ["Voltage1", "Voltage2", "Voltage3", "Voltage4", "Voltage5", "Voltage6",
                           "Voltage7", "Voltage8", "Voltage9", "Voltage10", "Voltage11", "Voltage12",
                           "Voltage13", "Voltage14", "Voltage15", "Voltage16"]
        feature_data = data[feature_columns]
        # 使用模型进行预测
        predictions = model.predict(feature_data)
        # 打印预测结果
        print(f"Predictions: {predictions}")
        return predictions


# 负责处理将不同传统机器学习的基学习器通过VotingClassifier进行集成学习
class ServiceMachineLearn_ensemble:
    def __init__(self, data_dao):
        self.data_dao = data_dao

    # 从数据库中获取数据
    def get_data_ensemble(self):
        '''
        从数据库中获取数据并转换为DataFrame
        Returns:
            data: DataFrame
        '''
        # 获取所有数据
        data = self.data_dao.get_all()
        # 将数据转换为DataFrame , 直接将字典列表转换为DataFrame
        data = pd.DataFrame([result.to_dict() for result in data])
        return data

    # 进行模型的集成
    def create_ensemble_models(self):
        # 加载模型
        model_knn = joblib.load('machine_learn_model_save/model_knn.pkl')
        model_rf = joblib.load('machine_learn_model_save/model_rf.pkl')
        model_svm = joblib.load('machine_learn_model_save/model_svm.pkl')

        # 加载所有模型信息为一个列表
        models_list = [('knn', model_knn), ('rf', model_rf), ('svm', model_svm)]


        # 创建VotingClassifier
        voting_clf = VotingClassifier(estimators=models_list,voting='hard')

        return voting_clf

    # 保存集成学习模型
    def save_model_ensemble(self, model, filename='model_ensemble.pkl'):
        # 设置模型保存的目录
        model_directory = os.path.join('machine_learn_model_save')
        # 检查目录是否存在，如果不存在则创建
        if not os.path.exists(model_directory):
            os.makedirs(model_directory)
        # 创建模型文件的完整路径
        file_path = os.path.join(model_directory, filename)
        # 保存模型到指定目录
        joblib.dump(model, file_path)
        print(f"集成学习模型已经被保存到 {file_path}")
        # 返回模型保存的路径
        return file_path

