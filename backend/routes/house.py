from flask import Blueprint, jsonify, request
from backend.models import HouseInfo, CommunityInfo, OwnerInfo
from backend.db import db

house_bp = Blueprint('house', __name__)

@house_bp.route('/api/houses', methods=['GET'])
def get_houses():
    try:
        community_id = request.args.get('communityId')
        parent_id = request.args.get('parentId')
        parent_ids = request.args.get('parentIds')
        room_id = request.args.get('roomId')
        keyword = request.args.get('keyword', '')
        
        # 新增过滤字段
        district_number = request.args.get('districtNumber', '')
        building_number = request.args.get('buildingNumber', '')
        unit_number = request.args.get('unitNumber', '')
        room_number = request.args.get('roomNumber', '')
        
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('pageSize', 10))
        
        # 构建基础查询
        query = HouseInfo.query
        
        # 应用过滤条件
        if community_id:
            query = query.filter(HouseInfo.community_id == community_id)
            
        if room_id:
            query = query.filter(HouseInfo.id == room_id)
        elif parent_ids:
            parent_id_list = [int(pid) for pid in parent_ids.split(',')]
            query = query.filter(HouseInfo.parent_id.in_(parent_id_list))
        elif parent_id:
            query = query.filter(HouseInfo.parent_id == parent_id)
        elif not any([keyword, district_number, building_number, unit_number, room_number]):
            # 如果没有任何搜索条件，则只显示顶层(区)
            query = query.filter(HouseInfo.house_level == 1)
        
        # 关键字搜索增强 - 在房屋全名中查找
        if keyword:
            query = query.filter(HouseInfo.house_full_name.like(f'%{keyword}%'))
        
        # 新增字段过滤条件
        if district_number:
            query = query.filter(HouseInfo.district_number.like(f'%{district_number}%'))
        if building_number:
            query = query.filter(HouseInfo.building_number.like(f'%{building_number}%'))
        if unit_number:
            query = query.filter(HouseInfo.unit_number.like(f'%{unit_number}%'))
        if room_number:
            query = query.filter(HouseInfo.room_number.like(f'%{room_number}%'))
            
        # 计算总数
        total = query.count()
        
        # 分页
        houses = query.offset((page - 1) * page_size).limit(page_size).all()
        
        # 打印调试信息
        print(f"查询到 {len(houses)} 条房屋信息")
        
        return jsonify({
            'success': True,
            'data': {
                'items': [house.to_dict() for house in houses],
                'total': total
            }
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
        if 'roomNumber' in data:
            house.room_number = data['roomNumber']
        if 'fullName' in data:
            house.house_full_name = data['fullName']
        if 'level' in data:
            house.house_level = data['level']
        if 'parentId' in data:
            house.parent_id = data['parentId']
            
        # 在 update_house 方法中添加调试输出
        print("接收到的数据:", data)
        print("房间号字段:", data.get('roomNumber'))
        
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
        
        # 检查是否有关联的业主
        owners = OwnerInfo.query.filter_by(house_id=id).all()
        if owners:
            return jsonify({'error': f'该房屋下有{len(owners)}个关联业主，请先移除业主关联后再删除'}), 400
            
        db.session.delete(house)
        db.session.commit()
        return jsonify({'success': True})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@house_bp.route('/api/houses/tree/<int:community_id>', methods=['GET'])
def get_house_tree(community_id):
    try:
        # 先检查社区是否存在
        community = CommunityInfo.query.get(community_id)
        if not community:
            return jsonify({
                'success': False,
                'error': '社区不存在'
            }), 404
            
        # 获取所有区
        districts = HouseInfo.query.filter_by(
            community_id=community_id,
            house_level=1
        ).all()
        
        result = []
        # 如果没有任何区域数据，返回一个空的树结构也是可以的
        if not districts:
            return jsonify({
                'success': True,
                'data': []
            })
        
        for district in districts:
            district_dict = district.to_dict()
            district_dict['children'] = []
            
            # 获取区下的所有楼栋
            buildings = HouseInfo.query.filter_by(
                parent_id=district.id,
                house_level=2
            ).all()
            
            for building in buildings:
                building_dict = building.to_dict()
                building_dict['children'] = []
                
                # 获取楼栋下的所有单元
                units = HouseInfo.query.filter_by(
                    parent_id=building.id,
                    house_level=3
                ).all()
                
                for unit in units:
                    unit_dict = unit.to_dict()
                    unit_dict['children'] = []
                    
                    # 获取单元下的所有房间
                    rooms = HouseInfo.query.filter_by(
                        parent_id=unit.id,
                        house_level=4
                    ).all()
                    
                    unit_dict['children'] = [room.to_dict() for room in rooms]
                    building_dict['children'].append(unit_dict)
                
                district_dict['children'].append(building_dict)
            
            result.append(district_dict)
        
        return jsonify({
            'success': True,
            'data': result
        })
        
    except Exception as e:
        print(f"获取房屋树结构失败: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500