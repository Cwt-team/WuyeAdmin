from flask import Flask, jsonify, request, session
from flask_cors import CORS
# from db import init_db, User  # 不再需要数据库相关的导入

app = Flask(__name__)
CORS(app, supports_credentials=True)  # 允许跨域请求并支持 Cookie
app.secret_key = 'your_secret_key'  # 用于 session 加密

# 如果不再使用数据库，可以移除相关配置
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:123456@localhost:3326/wuye'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 如果不使用数据库，可以移除初始化数据库的部分
# init_db(app)

# 获取用户信息的API
@app.route('/api/user-info', methods=['GET'])
def get_user_info():
    if 'username' not in session:
        return jsonify({'error': '未登录'}), 401
    return jsonify({'username': session['username']})

# 退出登录的API
@app.route('/api/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return jsonify({'message': '已成功退出登录'})

# 修改后的登录的API
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # 仅当用户名为 'admin' 且密码为 'password' 时登录成功
    if username == 'admin' and password == 'password':
        session['username'] = username
        return jsonify({'success': True, 'message': '登录成功'})
    else:
        return jsonify({'success': False, 'message': '用户名或密码错误'})

# 如果不使用数据库，可以移除测试数据库连接的API
# @app.route('/api/test-db', methods=['GET'])
# def test_db():
#     try:
#         # 尝试查询数据库
#         user = User.query.first()
#         return jsonify({'message': '数据库连接成功', 'user': user.username if user else 'No users found'})
#     except Exception as e:
#         return jsonify({'message': f'数据库连接失败: {e}'})

if __name__ == '__main__':
    app.run(debug=True)
