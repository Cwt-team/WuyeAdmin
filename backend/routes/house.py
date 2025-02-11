from flask import Blueprint, jsonify, request
from models.house import HouseInfo
from db import db

house_bp = Blueprint('house', __name__)

@house_bp.route('/api/houses', methods=['GET'])
def get_houses():
    try:
        community_id = request.args.get('communityId')
        parent_id = request.args.get('parentId')
        keyword = request.args.get('keyword', '')
        
        # 构建基础查询
        query = HouseInfo.query
        
        # 应用过滤条件
        if community_id:
            query = query.filter(HouseInfo.community_id == community_id)
        if parent_id:
            query = query.filter(HouseInfo.parent_id == parent_id)
        elif parent_id is None and not keyword:
            # 如果没有parent_id且没有关键字搜索，则只显示顶层(区)
            query = query.filter(HouseInfo.house_level == 1)
            
        if keyword:
            query = query.filter(HouseInfo.house_full_name.like(f'%{keyword}%'))
            
        houses = query.all()
        
        # 打印调试信息
        print(f"查询到 {len(houses)} 条房屋信息")
        for house in houses:
            print(f"房屋ID: {house.id}, 名称: {house.house_full_name}")
            
        return jsonify({
            'success': True,
            'data': [house.to_dict() for house in houses],
            'total': len(houses)
        })
        
    except Exception as e:
        print(f"获取房屋列表失败: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@house_bp.route('/api/houses', methods=['POST'])
def add_house():
    try:
        data = request.json
        
        new_house = HouseInfo(
            community_id=data['communityId'],
            district_number=data.get('districtNumber'),
            building_number=data.get('buildingNumber'),
            unit_number=data.get('unitNumber'),
            house_full_name=data['fullName'],
            house_level=data['level'],
            parent_id=data.get('parentId')
        )
        
        db.session.add(new_house)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': new_house.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@house_bp.route('/api/houses/<int:id>', methods=['PUT'])
def update_house(id):
    try:
        house = HouseInfo.query.get(id)
        if not house:
            return jsonify({'error': '房屋不存在'}), 404
            
        data = request.json
        
        if 'districtNumber' in data:
            house.district_number = data['districtNumber']
        if 'buildingNumber' in data:
            house.building_number = data['buildingNumber']
        if 'unitNumber' in data:
            house.unit_number = data['unitNumber']
        if 'fullName' in data:
            house.house_full_name = data['fullName']
        if 'level' in data:
            house.house_level = data['level']
        if 'parentId' in data:
            house.parent_id = data['parentId']
            
        db.session.commit()
        return jsonify({
            'success': True,
            'data': house.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@house_bp.route('/api/houses/<int:id>', methods=['DELETE'])
def delete_house(id):
    try:
        house = HouseInfo.query.get(id)
        if not house:
            return jsonify({'error': '房屋不存在'}), 404
            
        # 检查是否有子节点
        if house.children:
            return jsonify({'error': '该节点下还有子节点，无法删除'}), 400
            
        db.session.delete(house)
        db.session.commit()
        return jsonify({'success': True})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500 