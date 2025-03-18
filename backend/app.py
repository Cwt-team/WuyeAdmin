from flask import Flask, jsonify, request, session
from flask_cors import CORS
from db import db, init_db
from routes.community import community_bp
from routes.house import house_bp
from routes.admin_role import admin_role_bp
from routes.community_admin import community_admin_bp
from routes.property_admin import property_admin_bp
from routes.owner import owner_bp
from routes.owner_application import owner_application_bp
from routes.house_query import house_query_bp
from routes.room_notification import room_notification_bp
from routes.community_notification import community_notification_bp
from routes.advertisement import advertisement_bp
from routes.call_record import call_record_bp
from routes.alarm_record import alarm_record_bp
from routes.unlock_record import unlock_record_bp
from models.personal_info import PersonalInfo
from routes.personal_info import personal_info_bp
from routes.maintenance import maintenance_bp
import logging

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True)  # 允许跨域请求并支持 Cookie
    app.secret_key = 'your_secret_key'  # 用于 session 加密

    # 初始化数据库
    init_db(app)

    # 注册蓝图前记录日志
    logger.info("正在注册维修模块蓝图")
    app.register_blueprint(maintenance_bp)
    logger.info("维修模块蓝图注册完成")

    # 注册蓝图
    app.register_blueprint(community_bp)
    app.register_blueprint(house_bp)
    app.register_blueprint(admin_role_bp)
    app.register_blueprint(community_admin_bp)
    app.register_blueprint(property_admin_bp)
    app.register_blueprint(owner_bp)
    app.register_blueprint(owner_application_bp)
    app.register_blueprint(house_query_bp)
    app.register_blueprint(room_notification_bp)
    app.register_blueprint(community_notification_bp)
    app.register_blueprint(advertisement_bp)
    app.register_blueprint(call_record_bp)
    app.register_blueprint(alarm_record_bp)
    app.register_blueprint(unlock_record_bp)
    app.register_blueprint(personal_info_bp)

    @app.before_request
    def log_request_info():
        logger.debug('Headers: %s', request.headers)
        logger.debug('Body: %s', request.get_data())

    @app.after_request
    def log_response_info(response):
        logger.debug('Response: %s', response.get_data())
        return response

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

        # 超级管理员账号
        if username == 'admin' and password == 'password':
            session['username'] = username
            return jsonify({'success': True, 'message': '登录成功'})

        # 普通用户登录
        user = PersonalInfo.query.filter_by(account_number=username).first()
        if user and user.password == password:  # 直接比较密码
            session['username'] = username
            return jsonify({'success': True, 'message': '登录成功'})
        
        return jsonify({'success': False, 'message': '用户名或密码错误'})

    @app.route('/api/owners/export-template', methods=['GET'])
    def export_owner_template():
        if 'username' not in session:
            return jsonify({'error': '未登录'}), 401
        
        # Create CSV template
        import io
        import csv
        
        output = io.StringIO()
        writer = csv.writer(output)
        # Write header
        writer.writerow(['房间号', '姓名', '性别', '身份证号', '手机号', '备注', '业主类型'])
        
        # Create response
        response = app.response_class(
            response=output.getvalue(),
            status=200,
            mimetype='text/csv',
            headers={'Content-Disposition': 'attachment;filename=owner_template.csv'}
        )
        return response

    @app.route('/api/owners/export', methods=['GET'])
    def export_owners():
        if 'username' not in session:
            return jsonify({'error': '未登录'}), 401
        
        # Get filter parameters from request
        room = request.args.get('room')
        name = request.args.get('name')
        
        # Query owners
        from db import Owner
        query = Owner.query
        if room:
            query = query.filter(Owner.room.contains(room))
        if name:
            query = query.filter(Owner.name.contains(name))
        
        owners = query.all()
        
        # Create CSV
        import io
        import csv
        
        output = io.StringIO()
        writer = csv.writer(output)
        # Write header
        writer.writerow(['房间号', '姓名', '性别', '身份证号', '手机号', '备注', '业主类型', '更新时间'])
        # Write data
        for owner in owners:
            writer.writerow([
                owner.room,
                owner.name,
                owner.gender,
                owner.id_card,
                owner.phone,
                owner.remark,
                owner.owner_type,
                owner.update_time.strftime('%Y-%m-%d %H:%M:%S')
            ])
        
        # Create response
        response = app.response_class(
            response=output.getvalue(),
            status=200,
            mimetype='text/csv',
            headers={'Content-Disposition': 'attachment;filename=owners_export.csv'}
        )
        return response

    @app.route('/api/owners/import', methods=['POST'])
    def import_owners():
        if 'username' not in session:
            return jsonify({'error': '未登录'}), 401
        
        if 'file' not in request.files:
            return jsonify({'error': '未上传文件'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': '未选择文件'}), 400
        
        try:
            import io
            import csv
            from db import db, Owner
            
            # Read and parse CSV
            stream = io.StringIO(file.stream.read().decode('UTF8'), newline=None)
            reader = csv.reader(stream)
            
            # Skip header
            next(reader)
            
            # Process rows
            for row in reader:
                if len(row) != 7:
                    continue
                
                owner = Owner(
                    community_id=1,  # TODO: Get community ID from session
                    room=row[0],
                    name=row[1],
                    gender=row[2],
                    id_card=row[3],
                    phone=row[4],
                    remark=row[5],
                    owner_type=row[6]
                )
                db.session.add(owner)
            
            db.session.commit()
            return jsonify({'success': True, 'message': '导入成功'})
        
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'导入失败: {str(e)}'}), 500

    @app.errorhandler(500)
    def handle_500_error(error):
        print('Server Error:', error)  # 在控制台打印详细错误信息
        return jsonify({'error': 'Internal Server Error'}), 500

    return app

# 创建应用实例
app = create_app()

if __name__ == '__main__':
    logger.info("Flask应用启动")
    app.run(debug=True)
