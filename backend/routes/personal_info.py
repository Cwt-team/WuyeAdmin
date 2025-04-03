from flask import Blueprint, jsonify, request, session, send_from_directory
from backend.models.personal_info import PersonalInfo
from backend.db import db
from datetime import datetime
import os
from werkzeug.utils import secure_filename
import uuid

personal_info_bp = Blueprint('personal_info', __name__)

@personal_info_bp.route('/api/personal-info', methods=['GET'])
def get_personal_info():
    """获取当前登录用户的个人信息"""
    try:
        if 'username' not in session:
            return jsonify({'error': '未登录'}), 401
            
        user = PersonalInfo.query.filter_by(account_number=session['username']).first()
        if not user:
            return jsonify({'error': '用户不存在'}), 404
            
        return jsonify(user.to_dict())
    except Exception as e:
        return jsonify({'error': f'获取个人信息失败: {str(e)}'}), 500

@personal_info_bp.route('/api/personal-info', methods=['PUT'])
def update_personal_info():
    """更新个人信息"""
    try:
        if 'username' not in session:
            return jsonify({'error': '未登录'}), 401
            
        data = request.json
        user = PersonalInfo.query.filter_by(account_number=session['username']).first()
        
        if not user:
            return jsonify({'error': '用户不存在'}), 404

        # 更新基本信息
        if 'nickname' in data:
            user.nickname = data['nickname']
        if 'phoneNumber' in data:
            # 检查手机号是否已被其他用户使用
            existing_user = PersonalInfo.query.filter(
                PersonalInfo.phone_number == data['phoneNumber'],
                PersonalInfo.id != user.id
            ).first()
            if existing_user:
                return jsonify({'error': '该手机号已被使用'}), 400
            user.phone_number = data['phoneNumber']
        if 'email' in data:
            # 检查邮箱是否已被其他用户使用
            existing_user = PersonalInfo.query.filter(
                PersonalInfo.email == data['email'],
                PersonalInfo.id != user.id
            ).first()
            if existing_user:
                return jsonify({'error': '该邮箱已被使用'}), 400
            user.email = data['email']
        if 'profilePicturePath' in data:
            user.profile_picture_path = data['profilePicturePath']
            
        db.session.commit()
        return jsonify({'message': '更新成功', 'data': user.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'更新个人信息失败: {str(e)}'}), 500

@personal_info_bp.route('/api/personal-info/password', methods=['PUT'])
def update_password():
    """修改密码"""
    try:
        if 'username' not in session:
            return jsonify({'error': '未登录'}), 401
            
        data = request.json
        old_password = data.get('oldPassword')
        new_password = data.get('newPassword')
        
        if not old_password or not new_password:
            return jsonify({'error': '请提供原密码和新密码'}), 400
            
        user = PersonalInfo.query.filter_by(account_number=session['username']).first()
        
        # 验证原密码
        if user.password != old_password:  # 直接比较密码
            return jsonify({'error': '原密码错误'}), 400
            
        # 更新为新密码
        user.password = new_password  # 直接存储新密码
        db.session.commit()
        
        return jsonify({'message': '密码修改成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'修改密码失败: {str(e)}'}), 500

@personal_info_bp.route('/api/update-email', methods=['PUT'])
def update_email():
    """更新邮箱"""
    try:
        if 'username' not in session:
            return jsonify({'error': '未登录'}), 401
            
        data = request.json
        new_email = data.get('newEmail')
        verify_code = data.get('verifyCode')
        
        if not new_email or not verify_code:
            return jsonify({'error': '请提供新邮箱和验证码'}), 400
            
        # 验证验证码
        code_info = verification_codes.get(f"email:{new_email}")
        if not code_info or code_info['code'] != verify_code:
            return jsonify({'error': '验证码错误'}), 400
            
        # 检查验证码是否过期
        if datetime.now() > code_info['expiry']:
            return jsonify({'error': '验证码已过期'}), 400
            
        # 更新邮箱
        user = PersonalInfo.query.filter_by(account_number=session['username']).first()
        if not user:
            return jsonify({'error': '用户不存在'}), 404
            
        # 检查邮箱是否已被其他用户使用
        existing_user = PersonalInfo.query.filter(
            PersonalInfo.email == new_email,
            PersonalInfo.id != user.id
        ).first()
        if existing_user:
            return jsonify({'error': '该邮箱已被使用'}), 400
            
        user.email = new_email
        db.session.commit()
        
        # 清除验证码
        del verification_codes[f"email:{new_email}"]
        
        # 记录邮箱更新操作
        log_user_activity(user.id, '更新邮箱', f'邮箱更新为 {new_email}')
        
        return jsonify({'message': '邮箱更新成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'更新邮箱失败: {str(e)}'}), 500

# 确保上传目录存在
def ensure_upload_folder():
    upload_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'static', 'uploads', 'avatars')
    os.makedirs(upload_folder, exist_ok=True)
    return upload_folder

@personal_info_bp.route('/api/upload-avatar', methods=['POST'])
def upload_avatar():
    """上传头像"""
    try:
        if 'username' not in session:
            return jsonify({'error': '未登录'}), 401
            
        if 'avatar' not in request.files:
            return jsonify({'error': '请上传头像文件'}), 400
            
        file = request.files['avatar']
        
        if file.filename == '':
            return jsonify({'error': '未选择文件'}), 400
            
        # 检查文件类型
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
        if not '.' in file.filename or file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
            return jsonify({'error': '文件类型不支持，请上传图片格式文件'}), 400
            
        # 生成安全的文件名
        filename = secure_filename(file.filename)
        new_filename = f"{uuid.uuid4().hex}_{filename}"
        
        # 确保上传目录存在
        upload_folder = ensure_upload_folder()
        
        # 保存文件
        file_path = os.path.join(upload_folder, new_filename)
        file.save(file_path)
        
        # 生成可访问的URL
        url = f"/static/uploads/avatars/{new_filename}"
        
        # 更新用户头像
        user = PersonalInfo.query.filter_by(account_number=session['username']).first()
        user.profile_picture_path = url
        db.session.commit()
        
        return jsonify({'message': '头像上传成功', 'url': url})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'头像上传失败: {str(e)}'}), 500

# 为静态文件添加接口
@personal_info_bp.route('/static/uploads/avatars/<filename>')
def uploaded_avatar(filename):
    upload_folder = ensure_upload_folder()
    return send_from_directory(upload_folder, filename)

# 创建用户安全日志模型
from flask import current_app
import logging
import json

def log_user_activity(user_id, action, details=None):
    """记录用户活动日志"""
    try:
        # 创建日志记录
        log_entry = UserActivityLog(
            user_id=user_id,
            action=action,
            details=details,
            ip_address=request.remote_addr,
            user_agent=request.user_agent.string
        )
        db.session.add(log_entry)
        db.session.commit()
        
        # 同时写入应用日志文件
        log_data = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'user_id': user_id,
            'action': action,
            'details': details,
            'ip': request.remote_addr,
            'user_agent': request.user_agent.string
        }
        current_app.logger.info(f"用户活动: {json.dumps(log_data, ensure_ascii=False)}")
        
    except Exception as e:
        current_app.logger.error(f"记录用户活动失败: {str(e)}")
        db.session.rollback()

@personal_info_bp.route('/api/personal-info/security-logs', methods=['GET'])
def get_security_logs():
    """获取用户安全日志"""
    try:
        if 'username' not in session:
            return jsonify({'error': '未登录'}), 401
            
        user = PersonalInfo.query.filter_by(account_number=session['username']).first()
        if not user:
            return jsonify({'error': '用户不存在'}), 404
            
        page = int(request.args.get('page', 1))
        size = int(request.args.get('size', 10))
        
        logs = UserActivityLog.query.filter_by(user_id=user.id)\
            .order_by(UserActivityLog.created_at.desc())\
            .paginate(page=page, per_page=size, error_out=False)
            
        return jsonify({
            'logs': [log.to_dict() for log in logs.items],
            'total': logs.total,
            'page': logs.page,
            'size': size,
            'pages': logs.pages
        })
    except Exception as e:
        return jsonify({'error': f'获取安全日志失败: {str(e)}'}), 500

@personal_info_bp.route('/api/personal-info/check-password', methods=['POST'])
def check_password():
    """验证用户密码"""
    try:
        if 'username' not in session:
            return jsonify({'error': '未登录'}), 401
            
        password = request.json.get('password')
        if not password:
            return jsonify({'error': '请提供密码'}), 400
            
        user = PersonalInfo.query.filter_by(account_number=session['username']).first()
        if not user:
            return jsonify({'error': '用户不存在'}), 404
            
        is_correct = user.password == password  # 直接比较密码
        
        return jsonify({
            'correct': is_correct
        })
    except Exception as e:
        return jsonify({'error': f'验证密码失败: {str(e)}'}), 500

# 用于管理员查看系统中的管理员列表（仅超级管理员可用）
@personal_info_bp.route('/api/admins', methods=['GET'])
def get_admin_list():
    """获取管理员列表（仅超级管理员可用）"""
    try:
        if 'username' not in session:
            return jsonify({'error': '未登录'}), 401
            
        # 检查是否为超级管理员
        if session['username'] != 'admin':  # 假设只有 admin 是超级管理员
            return jsonify({'error': '权限不足'}), 403
            
        page = int(request.args.get('page', 1))
        size = int(request.args.get('size', 10))
        name = request.args.get('name', '')
        
        query = PersonalInfo.query
        if name:
            query = query.filter(
                db.or_(
                    PersonalInfo.account_number.like(f'%{name}%'),
                    PersonalInfo.nickname.like(f'%{name}%')
                )
            )
            
        total = query.count()
        admins = query.order_by(PersonalInfo.created_at.desc())\
            .offset((page - 1) * size)\
            .limit(size)\
            .all()
            
        return jsonify({
            'admins': [admin.to_dict() for admin in admins],
            'total': total
        })
    except Exception as e:
        return jsonify({'error': f'获取管理员列表失败: {str(e)}'}), 500

# 用于超级管理员创建新的管理员账号
@personal_info_bp.route('/api/admins', methods=['POST'])
def create_admin():
    """创建新管理员（仅超级管理员可用）"""
    try:
        if 'username' not in session:
            return jsonify({'error': '未登录'}), 401
            
        # 检查是否为超级管理员
        if session['username'] != 'admin':  # 假设只有 admin 是超级管理员
            return jsonify({'error': '权限不足'}), 403
            
        data = request.json
        
        # 验证必需字段
        required_fields = ['username', 'password', 'nickname']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'请提供{field}字段'}), 400
        
        # 检查用户名是否已存在
        existing_user = PersonalInfo.query.filter_by(account_number=data['username']).first()
        if existing_user:
            return jsonify({'error': '用户名已存在'}), 400
            
        # 检查可选字段的唯一性
        if 'phoneNumber' in data and data['phoneNumber']:
            existing_user = PersonalInfo.query.filter_by(phone_number=data['phoneNumber']).first()
            if existing_user:
                return jsonify({'error': '手机号已被使用'}), 400
                
        if 'email' in data and data['email']:
            existing_user = PersonalInfo.query.filter_by(email=data['email']).first()
            if existing_user:
                return jsonify({'error': '邮箱已被使用'}), 400
        
        # 创建新管理员
        new_admin = PersonalInfo(
            account_number=data['username'],
            nickname=data['nickname'],
            password=data['password'],
            phone_number=data.get('phoneNumber'),
            email=data.get('email'),
            profile_picture_path=data.get('profilePicturePath')
        )
        
        db.session.add(new_admin)
        db.session.commit()
        
        # 记录日志
        log_user_activity(
            user_id=PersonalInfo.query.filter_by(account_number='admin').first().id,
            action='创建管理员',
            details=f'创建了管理员 {data["username"]}'
        )
        
        return jsonify({
            'message': '管理员创建成功',
            'admin': new_admin.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'创建管理员失败: {str(e)}'}), 500 