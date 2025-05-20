from flask import Blueprint, request, jsonify
from backend.db import db
from backend.models.owner import OwnerInfo
from backend.models.housing_application import HousingApplication
from backend.models.house_info import HouseInfo
from backend.models.community_info import CommunityInfo
import os
import time
import logging

# 配置日志
logger = logging.getLogger(__name__)

# 创建蓝图
mobile_api_bp = Blueprint('mobile_api', __name__)

# 移动端登录API
@mobile_api_bp.route('/api/mobile/login', methods=['POST'])
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
        logger.error(f"移动端登录失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'登录失败: {str(e)}'
        })

# 移动端用户注册API
@mobile_api_bp.route('/api/mobile/register', methods=['POST'])
def mobile_register():
    data = request.form
    username = data.get('username')
    password = data.get('password')
    name = data.get('name')
    phone_number = data.get('phone')
    
    try:
        # 验证必填项
        if not all([username, password, name, phone_number]):
            return jsonify({
                'success': False,
                'message': '请填写所有必要信息'
            })
            
        # 验证账号是否已存在
        existing_account = db.session.query(OwnerInfo).filter_by(account=username).first()
        if existing_account:
            return jsonify({
                'success': False,
                'message': '该账号已被注册'
            })
            
        # 验证手机号是否已存在
        existing_phone = db.session.query(OwnerInfo).filter_by(phone_number=phone_number).first()
        if existing_phone:
            return jsonify({
                'success': False,
                'message': '该手机号已被注册'
            })
        
        # 创建新用户，但不绑定房屋，设置审核状态为"未绑定"
        new_owner = OwnerInfo(
            community_id=None,  # 暂不绑定社区
            house_id=None,      # 暂不绑定房屋
            name=name,
            gender='M',         # 默认性别
            phone_number=phone_number,
            account=username,
            password=password,
            owner_type='待审核',  # 标记为待审核状态
            updated_at=db.func.current_timestamp()
        )
        
        db.session.add(new_owner)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '注册成功，请登录后提交房屋绑定申请'
        })
            
    except Exception as e:
        # 记录错误
        logger.error(f"移动端注册失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'注册失败: {str(e)}'
        })

# 获取业主详细信息
@mobile_api_bp.route('/api/mobile/owners/<int:owner_id>', methods=['GET'])
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
                'id': community.id if community else None,
                'name': community.community_name if community else '',
                'city': community.community_city if community else ''
            },
            'houseInfo': {
                'id': house.id if house else None,
                'fullName': house.house_full_name if house else '',
                'districtNumber': house.district_number if house else '',
                'buildingNumber': house.building_number if house else '',
                'unitNumber': house.unit_number if house else '',
                'roomNumber': house.room_number if house else ''
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
        logger.error(f"获取业主详细信息失败: {str(e)}")
        return jsonify({'success': False, 'message': f'获取业主详细信息失败: {str(e)}'}), 500

# 更新业主信息
@mobile_api_bp.route('/api/mobile/owners/<int:owner_id>', methods=['PUT'])
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
        logger.error(f"更新业主信息失败: {str(e)}")
        return jsonify({'success': False, 'message': f'更新业主信息失败: {str(e)}'}), 500

# 上传人脸图像
@mobile_api_bp.route('/api/mobile/owners/<int:owner_id>/face', methods=['POST'])
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
        upload_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'uploads', 'faces')
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
        logger.error(f"上传人脸图像失败: {str(e)}")
        return jsonify({'success': False, 'message': f'上传人脸图像失败: {str(e)}'}), 500

# 获取社区列表
@mobile_api_bp.route('/api/mobile/communities', methods=['GET'])
def get_communities():
    try:
        communities = db.session.query(CommunityInfo).all()
        result = []
        
        for community in communities:
            result.append({
                'id': community.id,
                'name': community.community_name,
                'address': community.community_city
            })
            
        return jsonify({
            'success': True,
            'communities': result
        })
    except Exception as e:
        logger.error(f"获取社区列表失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'获取社区列表失败: {str(e)}'
        })

# 提交房屋绑定申请
@mobile_api_bp.route('/api/mobile/housing-application', methods=['POST'])
def submit_housing_application():
    data = request.form
    owner_id = data.get('ownerId')
    community_id = data.get('communityId')
    building_name = data.get('buildingName')
    unit_name = data.get('unitName')
    house_number = data.get('houseNumber')
    id_card = data.get('idCard')
    
    try:
        # 校验必填项
        if not all([owner_id, community_id, building_name, unit_name, house_number, id_card]):
            return jsonify({
                'success': False,
                'message': '请填写所有必要信息'
            })
        
        # 查找用户
        owner = db.session.query(OwnerInfo).filter_by(id=owner_id).first()
        if not owner:
            return jsonify({
                'success': False,
                'message': '用户不存在'
            })
        
        # 自动校验房屋是否存在
        house = db.session.query(HouseInfo).filter_by(
            community_id=community_id,
            building_number=building_name,
            unit_number=unit_name,
            room_number=house_number
        ).first()
        house_exists = house is not None
        house_id = house.id if house_exists else None
        
        # 创建申请记录
        application = HousingApplication(
            community_id=community_id,
            house_id=house_id,  # 如果存在则写入house_id，否则为None
            name=owner.name,
            gender=owner.gender,
            id_card=id_card,
            phone_number=owner.phone_number,
            application_status='待审核',
            owner_type='业主',
            application_time=db.func.current_timestamp()
        )
        application.building_name = building_name
        application.unit_name = unit_name  
        application.house_number = house_number
        
        db.session.add(application)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '申请已提交，请等待物业审核',
            'applicationId': application.id,
            'houseExists': house_exists,
            'houseId': house_id
        })
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"提交房屋绑定申请失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'提交申请失败: {str(e)}'
        })

# 获取用户申请记录
@mobile_api_bp.route('/api/mobile/housing-applications/<int:owner_id>', methods=['GET'])
def get_housing_applications(owner_id):
    try:
        # 查找用户
        owner = db.session.query(OwnerInfo).filter_by(id=owner_id).first()
        if not owner:
            return jsonify({
                'success': False,
                'message': '用户不存在'
            })
        
        # 查询该用户的申请记录
        applications = db.session.query(HousingApplication).filter_by(
            phone_number=owner.phone_number
        ).order_by(HousingApplication.application_time.desc()).all()
        
        result = []
        for app in applications:
            result.append({
                'id': app.id,
                'communityId': app.community_id,
                'communityName': app.community.community_name if app.community else '',
                'buildingName': app.building_name,
                'unitName': app.unit_name,
                'houseNumber': app.house_number,
                'status': app.application_status,
                'applicationTime': app.application_time.strftime('%Y-%m-%d %H:%M:%S'),
                'callbackMessage': app.callback_message
            })
        
        return jsonify({
            'success': True,
            'applications': result
        })
        
    except Exception as e:
        logger.error(f"获取房屋绑定申请失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'获取申请记录失败: {str(e)}'
        })

# 上传申请证明材料
@mobile_api_bp.route('/api/mobile/housing-application/<int:application_id>/proof', methods=['POST'])
def upload_application_proof(application_id):
    try:
        if 'image' not in request.files:
            return jsonify({'success': False, 'message': '未上传图片'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'success': False, 'message': '文件名为空'}), 400
        
        # 查找申请记录
        application = db.session.query(HousingApplication).filter_by(id=application_id).first()
        if not application:
            return jsonify({'success': False, 'message': '申请不存在'}), 404
        
        # 保存图片
        filename = f'application_proof_{application_id}_{int(time.time())}.jpg'
        upload_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'uploads', 'proofs')
        os.makedirs(upload_folder, exist_ok=True)
        
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        
        # 更新申请信息
        application.information_photo = f'/static/uploads/proofs/{filename}'
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'message': '证明材料上传成功'
        })
    except Exception as e:
        db.session.rollback()
        logger.error(f"上传申请证明材料失败: {str(e)}")
        return jsonify({'success': False, 'message': f'上传失败: {str(e)}'}), 500

# 获取小区下所有楼栋
@mobile_api_bp.route('/api/mobile/buildings', methods=['GET'])
def get_buildings():
    community_id = request.args.get('communityId')
    if not community_id:
        return jsonify({'success': False, 'message': '缺少communityId'}), 400
    buildings = db.session.query(HouseInfo).filter_by(community_id=community_id, house_level=2).all()
    result = [{'id': b.id, 'buildingNumber': b.building_number, 'name': b.house_full_name} for b in buildings]
    return jsonify({'success': True, 'buildings': result})

# 获取楼栋下所有单元
@mobile_api_bp.route('/api/mobile/units', methods=['GET'])
def get_units():
    building_id = request.args.get('buildingId')
    if not building_id:
        return jsonify({'success': False, 'message': '缺少buildingId'}), 400
    units = db.session.query(HouseInfo).filter_by(parent_id=building_id, house_level=3).all()
    result = [{'id': u.id, 'unitNumber': u.unit_number, 'name': u.house_full_name} for u in units]
    return jsonify({'success': True, 'units': result})

# 获取单元下所有房间
@mobile_api_bp.route('/api/mobile/rooms', methods=['GET'])
def get_rooms():
    unit_id = request.args.get('unitId')
    if not unit_id:
        return jsonify({'success': False, 'message': '缺少unitId'}), 400
    rooms = db.session.query(HouseInfo).filter_by(parent_id=unit_id, house_level=4).all()
    result = [{'id': r.id, 'roomNumber': r.room_number, 'name': r.house_full_name} for r in rooms]
    return jsonify({'success': True, 'rooms': result}) 