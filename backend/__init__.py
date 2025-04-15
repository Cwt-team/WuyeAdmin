from flask import Flask, jsonify, request, session, send_from_directory
from flask_cors import CORS
from .db import db, init_db
import logging
import os
import time
import random
from datetime import datetime

# 设置 SQLAlchemy 的日志级别为 WARNING 或更高
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)

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
    
    # 加载配置
    from .config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS, SQLALCHEMY_ECHO
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
    app.config['SQLALCHEMY_ECHO'] = SQLALCHEMY_ECHO

    # 初始化数据库
    init_db(app)

    # 推迟导入路由以避免循环导入
    from backend.routes.community import community_bp
    from backend.routes.house import house_bp
    from backend.routes.admin_role import admin_role_bp
    from backend.routes.community_admin import community_admin_bp
    from backend.routes.property_admin import property_admin_bp
    from backend.routes.owner import owner_bp
    from backend.models.owner import OwnerInfo
    from backend.routes.owner_application import owner_application_bp
    from backend.routes.room_notification import room_notification_bp
    from backend.routes.community_notification import community_notification_bp
    from backend.routes.advertisement import advertisement_bp
    from backend.routes.call_record import call_record_bp
    from backend.routes.alarm_record import alarm_record_bp
    from backend.routes.unlock_record import unlock_record_bp
    from backend.models.personal_info import PersonalInfo
    from backend.routes.personal_info import personal_info_bp
    from backend.routes.maintenance import maintenance_bp
    from backend.routes.community_review import community_review_bp
    from backend.routes.complaint import complaint_bp

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
    app.register_blueprint(room_notification_bp)
    app.register_blueprint(community_notification_bp)
    app.register_blueprint(advertisement_bp)
    app.register_blueprint(call_record_bp)
    app.register_blueprint(alarm_record_bp)
    app.register_blueprint(unlock_record_bp)
    app.register_blueprint(personal_info_bp)
    app.register_blueprint(community_review_bp)
    app.register_blueprint(complaint_bp)

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

    # 原有网页管理员登录API保持不变
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

    # 修改移动端登录的路由路径为 /api/mobile/login
    @app.route('/api/mobile/login', methods=['POST'])
    def mobile_login():
        data = request.form
        username = data.get('username')
        password = data.get('password')
        
        try:
            # 验证账号密码
            owner = db.session.query(OwnerInfo).filter_by(account=username, password=password).first()
            
            if owner:
                # 成功找到用户
                return jsonify({
                    'success': True,
                    'message': '登录成功',
                    'ownerInfo': {
                        'id': owner.id,
                        'name': owner.name,
                        'phoneNumber': owner.phone_number,
                        'account': owner.account,
                        'communityId': owner.community_id,
                        'houseId': owner.house_id
                    }
                })
            else:
                # 未找到用户
                return jsonify({
                    'success': False,
                    'message': '账号或密码错误'
                })
        except Exception as e:
            # 记录错误
            app.logger.error(f"移动端登录失败: {str(e)}")
            return jsonify({
                'success': False,
                'message': f'登录失败: {str(e)}'
            })

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
        from backend.models.owner import OwnerInfo  # 使用绝对导入
        query = OwnerInfo.query
        if room:
            query = query.filter(OwnerInfo.room.contains(room))
        if name:
            query = query.filter(OwnerInfo.name.contains(name))
        
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
            from backend.models.owner import OwnerInfo  # 使用绝对导入
            
            # Read and parse CSV
            stream = io.StringIO(file.stream.read().decode('UTF8'), newline=None)
            reader = csv.reader(stream)
            
            # Skip header
            next(reader)
            
            # Process rows
            for row in reader:
                if len(row) != 7:
                    continue
                
                owner = OwnerInfo(
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

    # 添加静态文件路由
    @app.route('/static/uploads/avatars/<filename>')
    def get_avatar(filename):
        upload_folder = os.path.join(app.root_path, 'static', 'uploads', 'avatars')
        os.makedirs(upload_folder, exist_ok=True)
        return send_from_directory(upload_folder, filename)

    # 添加获取业主信息的API接口
    @app.route('/api/owners/<phone>', methods=['GET'])
    def get_owner_by_phone(phone):
        try:
            owner = db.session.query(OwnerInfo).filter_by(phone_number=phone).first()
            
            if owner:
                return jsonify({
                    'id': owner.id,
                    'name': owner.name,
                    'phoneNumber': owner.phone_number,
                    'account': owner.account
                    # 其他需要返回的字段
                })
            else:
                return jsonify({'error': '业主不存在'}), 404
        except Exception as e:
            app.logger.error(f"获取业主信息失败: {str(e)}")
            return jsonify({'error': f'获取业主信息失败: {str(e)}'}), 500

    @app.route('/api/ping', methods=['GET'])
    def ping():
        return '', 200  # 返回空响应，状态码 200

    # 为移动端添加获取业主详细信息的API接口
    @app.route('/api/mobile/owners/<int:owner_id>', methods=['GET'])
    def get_owner_detail_by_id(owner_id):
        try:
            owner = db.session.query(OwnerInfo).filter_by(id=owner_id).first()
            
            if not owner:
                return jsonify({'success': False, 'message': '业主不存在'}), 404
            
            # 获取关联的小区和房屋信息
            community = owner.community
            house = owner.house
            
            # 构建详细的业主信息
            owner_data = {
                'id': owner.id,
                'name': owner.name,
                'phoneNumber': owner.phone_number,
                'account': owner.account,
                'gender': owner.gender,
                'idCard': owner.id_card,
                'email': owner.email,
                'city': owner.city,
                'address': owner.address,
                'ownerType': owner.owner_type,
                'faceImage': owner.face_image,
                'faceStatus': owner.face_status,
                'communityInfo': {
                    'id': community.id,
                    'name': community.community_name,
                    'city': community.community_city
                },
                'houseInfo': {
                    'id': house.id,
                    'fullName': house.house_full_name,
                    'districtNumber': house.district_number,
                    'buildingNumber': house.building_number,
                    'unitNumber': house.unit_number,
                    'roomNumber': house.room_number
                }
            }
            
            # 获取业主权限信息
            permissions = owner.permissions.first()
            if permissions:
                owner_data['permissions'] = {
                    'id': permissions.id,
                    'permissionStatus': permissions.permission_status,
                    'validPeriod': permissions.valid_period,
                    'callingEnabled': permissions.calling_enabled,
                    'pstnEnabled': permissions.pstn_enabled
                }
            
            return jsonify({'success': True, 'data': owner_data})
        except Exception as e:
            app.logger.error(f"获取业主详细信息失败: {str(e)}")
            return jsonify({'success': False, 'message': f'获取业主详细信息失败: {str(e)}'}), 500

    # 为移动端添加更新业主信息的API接口
    @app.route('/api/mobile/owners/<int:owner_id>', methods=['PUT'])
    def update_owner_info(owner_id):
        try:
            data = request.json
            owner = db.session.query(OwnerInfo).filter_by(id=owner_id).first()
            
            if not owner:
                return jsonify({'success': False, 'message': '业主不存在'}), 404
            
            # 只允许更新部分字段
            allowed_fields = ['email', 'city', 'address']
            for field in allowed_fields:
                if field in data:
                    setattr(owner, field, data[field])
            
            # 更新密码（需要验证旧密码）
            if 'oldPassword' in data and 'newPassword' in data:
                if owner.password == data['oldPassword']:
                    owner.password = data['newPassword']
                else:
                    return jsonify({'success': False, 'message': '原密码不正确'}), 400
            
            # 保存更改
            db.session.commit()
            
            return jsonify({'success': True, 'message': '信息更新成功'})
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"更新业主信息失败: {str(e)}")
            return jsonify({'success': False, 'message': f'更新业主信息失败: {str(e)}'}), 500

    # 为移动端添加上传人脸图像的API接口
    @app.route('/api/mobile/owners/<int:owner_id>/face', methods=['POST'])
    def upload_owner_face(owner_id):
        try:
            if 'image' not in request.files:
                return jsonify({'success': False, 'message': '未上传图片'}), 400
            
            file = request.files['image']
            if file.filename == '':
                return jsonify({'success': False, 'message': '文件名为空'}), 400
            
            # 查找业主
            owner = db.session.query(OwnerInfo).filter_by(id=owner_id).first()
            if not owner:
                return jsonify({'success': False, 'message': '业主不存在'}), 404
            
            # 保存图片
            filename = f'owner_face_{owner_id}_{int(time.time())}.jpg'
            upload_folder = os.path.join(app.root_path, 'static', 'uploads', 'faces')
            os.makedirs(upload_folder, exist_ok=True)
            
            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)
            
            # 更新业主人脸信息
            owner.face_image = f'/static/uploads/faces/{filename}'
            owner.face_status = 1  # 已录入
            db.session.commit()
            
            return jsonify({
                'success': True, 
                'message': '人脸图像上传成功',
                'faceImage': owner.face_image,
                'faceStatus': owner.face_status
            })
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"上传人脸图像失败: {str(e)}")
            return jsonify({'success': False, 'message': f'上传人脸图像失败: {str(e)}'}), 500

    return app

# 创建应用实例
app = create_app()
