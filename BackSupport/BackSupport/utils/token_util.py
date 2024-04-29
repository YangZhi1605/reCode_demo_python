import jwt
import datetime
# from BackSupport import create_app

def generate_token(user_info):
    try:
        # 设置token的过期时间，这里设置为24小时后过期
        exp = datetime.datetime.utcnow() + datetime.timedelta(days=1)
        # app = create_app() # 别这种做，每次都会创建一个新的app实例，会导致secret_key不一致
        # 使用我的JWT密钥，用于签名token，应保持安全
        secret_key = 'yangzhi823823'

        # 创建一个字典，包含想要放入token的信息
        payload = {
            'exp': exp,
            'iat': datetime.datetime.utcnow(),  # token的发行时间
            'sub': user_info  # 用户信息，比如用户ID或用户名
        }

        # 使用HS256算法生成token
        token_ret = jwt.encode(payload, secret_key, algorithm='HS256')

        return token_ret
    except Exception as e:
        return str(e)


# # 假设有个用户的信息是 'user_id_123'，生成token
# token = generate_token(user_info='user_id_123')
#
# print("Generated token:", token)