from flask import Blueprint, jsonify, request, session
from backend.db import db
from backend.models.housing_application import HousingApplication
from backend.models.house_info import HouseInfo
from backend.models.owner import OwnerInfo
import logging

# 配置日志
logger = logging.getLogger(__name__)

# 创建蓝图
housing_application_bp = Blueprint('housing_application', __name__)

# 获取所有房屋绑定申请
@housing_application_bp.route('/api/housing-applications', methods=['GET'])
def get_all_housing_applications():
    if 'username' not in session:
        return jsonify({'error': '未登录'}), 401
    
    try:
        page = int(request.args.get('page', 1))
        size = int(request.args.get('size', 10))
        status = request.args.get('status')
        
        query = db.session.query(HousingApplication)
        if status:
            query = query.filter_by(application_status=status)
        
        # 计算总数并分页
        total = query.count()
        applications = query.order_by(HousingApplication.application_time.desc())\
                           .offset((page - 1) * size)\
                           .limit(size)\
                           .all()
        
        result = []
        for app in applications:
            result.append({
                'id': app.id,
                'name': app.name,
                'phoneNumber': app.phone_number,
                'idCard': app.id_card,
                'communityId': app.community_id,
                'communityName': app.community.community_name if app.community else '',
                'buildingName': app.building_name,
                'unitName': app.unit_name,
                'houseNumber': app.house_number,
                'status': app.application_status,
                'applicationTime': app.application_time.strftime('%Y-%m-%d %H:%M:%S'),
                'informationPhoto': app.information_photo
            })
        
        return jsonify({
            'applications': result,
            'total': total
        })
        
    except Exception as e:
        logger.error(f"获取所有房屋绑定申请失败: {str(e)}")
        return jsonify({'error': f'获取申请记录失败: {str(e)}'}), 500

# 获取单个申请详情
@housing_application_bp.route('/api/housing-applications/<int:application_id>', methods=['GET'])
def get_housing_application(application_id):
    if 'username' not in session:
        return jsonify({'error': '未登录'}), 401
    
    try:
        application = db.session.query(HousingApplication).filter_by(id=application_id).first()
        if not application:
            return jsonify({'error': '申请不存在'}), 404
        
        result = {
            'id': application.id,
            'name': application.name,
            'phoneNumber': application.phone_number,
            'idCard': application.id_card,
            'communityId': application.community_id,
            'communityName': application.community.community_name if application.community else '',
            'buildingName': application.building_name,
            'unitName': application.unit_name,
            'houseNumber': application.house_number,
            'status': application.application_status,
            'applicationTime': application.application_time.strftime('%Y-%m-%d %H:%M:%S'),
            'informationPhoto': application.information_photo,
            'callbackMessage': application.callback_message,
            'ownerType': application.owner_type
        }
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"获取房屋绑定申请详情失败: {str(e)}")
        return jsonify({'error': f'获取申请详情失败: {str(e)}'}), 500

# 审批申请
@housing_application_bp.route('/api/housing-applications/<int:application_id>/approve', methods=['POST'])
def approve_housing_application(application_id):
    if 'username' not in session:
        return jsonify({'error': '未登录'}), 401
    
    try:
        application = db.session.query(HousingApplication).filter_by(id=application_id).first()
        if not application:
            return jsonify({'error': '申请不存在'}), 404
        
        # 查找或创建对应的房屋记录
        house = db.session.query(HouseInfo).filter_by(
            community_id=application.community_id,
            building_number=application.building_name,
            unit_number=application.unit_name,
            room_number=application.house_number
        ).first()
        
        if not house:
            # 查找district_number和parent_id
            district_number = None
            parent_id = None
            # 先查找楼栋级（level=2）
            building = db.session.query(HouseInfo).filter_by(
                community_id=application.community_id,
                building_number=application.building_name,
                house_level=2
            ).first()
            if building:
                district_number = building.district_number
            # 再查找单元级（level=3）
            unit = db.session.query(HouseInfo).filter_by(
                community_id=application.community_id,
                building_number=application.building_name,
                unit_number=application.unit_name,
                house_level=3
            ).first()
            if unit:
                parent_id = unit.id
            house = HouseInfo(
                community_id=application.community_id,
                district_number=district_number,
                building_number=application.building_name,
                unit_number=application.unit_name,
                room_number=application.house_number,
                house_full_name=f"{application.building_name}-{application.unit_name}-{application.house_number}",
                house_level=4,
                parent_id=parent_id,
                created_at=db.func.current_timestamp()
            )
            db.session.add(house)
            db.session.commit()
        
        # 更新申请状态
        application.application_status = '已审核'
        application.house_id = house.id
        
        # 查找并更新业主信息
        owner = db.session.query(OwnerInfo).filter_by(phone_number=application.phone_number).first()
        if owner:
            owner.community_id = application.community_id
            owner.house_id = house.id
            owner.id_card = application.id_card
            owner.owner_type = '业主'  # 更新为正式业主
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': '申请已审核通过'})
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"审批房屋绑定申请失败: {str(e)}")
        return jsonify({'error': f'审批失败: {str(e)}'}), 500

# 拒绝申请
@housing_application_bp.route('/api/housing-applications/<int:application_id>/reject', methods=['POST'])
def reject_housing_application(application_id):
    if 'username' not in session:
        return jsonify({'error': '未登录'}), 401
    
    data = request.json
    callback_message = data.get('callbackMessage', '申请被拒绝')
    
    try:
        application = db.session.query(HousingApplication).filter_by(id=application_id).first()
        if not application:
            return jsonify({'error': '申请不存在'}), 404
        
        # 更新申请状态
        application.application_status = '已拒绝'
        application.callback_message = callback_message
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': '申请已拒绝'})
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"拒绝房屋绑定申请失败: {str(e)}")
        return jsonify({'error': f'操作失败: {str(e)}'}), 500 