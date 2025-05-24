from flask import Blueprint, jsonify, request, session
from backend.models.community_info import CommunityInfo
from backend.db import db
from datetime import datetime
from backend.models.house import HouseInfo

community_bp = Blueprint('community', __name__)

@community_bp.route('/api/communities', methods=['GET'])
def get_communities():
    try:
        # 获取查询参数
        keyword = request.args.get('keyword', '')
        location = request.args.get('location', '')
        access_card_type = request.args.get('accessCardType', '')
        is_enabled = request.args.get('isEnabled')
        app_record_face = request.args.get('appRecordFace')
        is_record_upload = request.args.get('isRecordUpload')
        is_same_step = request.args.get('isSameStep')
        page = int(request.args.get('page', 1))
        size = int(request.args.get('size', 10))
        
        # 构建查询
        query = CommunityInfo.query

        # 关键字搜索（小区名称或编号）
        if keyword:
            query = query.filter(
                db.or_(
                    CommunityInfo.community_name.like(f'%{keyword}%'),
                    CommunityInfo.community_number.like(f'%{keyword}%')
                )
            )
        
        # 城市搜索
        if location:
            query = query.filter(CommunityInfo.community_city == location)
            
        # 门禁卡类型过滤
        if access_card_type:
            query = query.filter(CommunityInfo.access_card_type == access_card_type)
            
        # 启用状态过滤
        if is_enabled is not None:
            query = query.filter(CommunityInfo.is_enabled == int(is_enabled))
            
        # APP人脸录入过滤
        if app_record_face is not None:
            query = query.filter(CommunityInfo.app_record_face == int(app_record_face))
            
        # 记录上传开关过滤
        if is_record_upload is not None:
            query = query.filter(CommunityInfo.is_record_upload == int(is_record_upload))
            
        # 配置同步状态过滤
        if is_same_step is not None:
            query = query.filter(CommunityInfo.is_same_step == int(is_same_step))
            
        # 权限过滤：非超级管理员只查自己有权限的小区
        if 'username' in session and session.get('role') != '超级管理员':
            query = query.filter(CommunityInfo.id == session.get('community_id'))
            
        # 计算总数
        total = query.count()
        
        # 添加排序（按创建时间倒序）
        query = query.order_by(CommunityInfo.created_at.desc())
        
        # 分页查询
        communities = query.offset((page-1)*size).limit(size).all()
        
        return jsonify({
            'total': total,
            'items': [community.to_dict() for community in communities]
        })
        
    except Exception as e:
        print(f"发生错误: {str(e)}")
        return jsonify({
            'error': '查询失败',
            'message': str(e)
        }), 500

@community_bp.route('/api/communities', methods=['POST'])
def add_community():
    try:
        data = request.json
        
        new_community = CommunityInfo(
            community_number=f'CM{datetime.now().strftime("%Y%m%d%H%M%S")}',
            community_name=data['name'],
            community_city=data['location'],
            creation_time=datetime.now(),
            is_enabled=1,
            management_machine_quantity=data.get('managerMachineCount', 0),
            indoor_machine_quantity=data.get('indoorMachineCount', 0),
            access_card_type=data.get('accessCardType', 'NFC'),
            app_record_face=data.get('appRecordFace', 1),
            is_same_step=data.get('isSameStep', 1),
            is_record_upload=data.get('isRecordUpload', 1),
            community_password=data.get('password', '123456')
        )
        
        db.session.add(new_community)
        db.session.commit()
        
        return jsonify({'success': True, 'data': new_community.to_dict()})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@community_bp.route('/api/communities/<int:id>', methods=['PUT'])
def update_community(id):
    try:
        community = CommunityInfo.query.get(id)
        if not community:
            return jsonify({'error': '小区不存在'}), 404
            
        data = request.json
        
        if 'name' in data:
            community.community_name = data['name']
        if 'location' in data:
            community.community_city = data['location']
        if 'managerMachineCount' in data:
            community.management_machine_quantity = data['managerMachineCount']
        if 'indoorMachineCount' in data:
            community.indoor_machine_quantity = data['indoorMachineCount']
        if 'accessCardType' in data:
            community.access_card_type = data['accessCardType']
        if 'appRecordFace' in data:
            community.app_record_face = data['appRecordFace']
        if 'isSameStep' in data:
            community.is_same_step = data['isSameStep']
        if 'isRecordUpload' in data:
            community.is_record_upload = data['isRecordUpload']
            
        db.session.commit()
        return jsonify({'success': True, 'data': community.to_dict()})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@community_bp.route('/api/communities/<int:id>', methods=['DELETE'])
def delete_community(id):
    try:
        community = CommunityInfo.query.get(id)
        if not community:
            return jsonify({'error': '小区不存在'}), 404
            
        db.session.delete(community)
        db.session.commit()
        return jsonify({'success': True})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@community_bp.route('/api/districts', methods=['GET'])
def get_districts():
    try:
        page = int(request.args.get('page', 1))
        size = int(request.args.get('size', 10))
        keyword = request.args.get('keyword', '')
        community_id = request.args.get('communityId')

        # 基础查询：只查区（house_level=1）
        query = HouseInfo.query.filter(HouseInfo.house_level == 1)

        # 权限过滤：非超级管理员只查自己有权限的小区
        if 'username' in session and session.get('role') != '超级管理员':
            query = query.filter(HouseInfo.community_id == session.get('community_id'))

        # 关键字搜索（区名/区号/小区名）
        if keyword:
            # 先查出所有小区名匹配的id
            community_ids = []
            if keyword:
                communities = CommunityInfo.query.filter(CommunityInfo.community_name.like(f'%{keyword}%')).all()
                community_ids = [c.id for c in communities]
            query = query.filter(
                db.or_(HouseInfo.house_full_name.like(f'%{keyword}%'),
                       HouseInfo.district_number.like(f'%{keyword}%'),
                       HouseInfo.community_id.in_(community_ids))
            )
        if community_id:
            query = query.filter(HouseInfo.community_id == community_id)

        total = query.count()
        districts = query.order_by(HouseInfo.id.desc()).offset((page-1)*size).limit(size).all()

        # 拼接小区名
        result = []
        for d in districts:
            community = CommunityInfo.query.get(d.community_id)
            result.append({
                'id': d.id,
                'districtNumber': d.district_number,
                'districtName': d.house_full_name,
                'communityId': d.community_id,
                'communityName': community.community_name if community else '',
                'communityCity': community.community_city if community else '',
            })
        return jsonify({'total': total, 'items': result})
    except Exception as e:
        print(f"获取区列表失败: {str(e)}")
        return jsonify({'error': '获取区列表失败', 'message': str(e)}), 500 