from flask import Blueprint, jsonify, request, session
from backend.models.house import HouseInfo
from backend.models.community_info import CommunityInfo
from backend.models.owner import OwnerInfo
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
        
        # 权限过滤：非超级管理员只查自己有权限的小区
        if 'username' in session and session.get('role') != '超级管理员':
            query = query.filter(HouseInfo.community_id == session.get('community_id'))
        
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
        
        # 验证必要字段
        required_fields = ['communityId', 'level']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'缺少必要字段: {field}'
                }), 400
        
        # 获取父级房屋信息
        parent_house = None
        if data.get('parentId'):
            parent_house = HouseInfo.query.get(data['parentId'])
            if parent_house:
                # 智能继承父级房屋的区号、楼栋号、单元号信息
                if not data.get('districtNumber') and parent_house.district_number:
                    data['districtNumber'] = parent_house.district_number
                    print(f"从父节点继承区号: {data['districtNumber']}")
                    
                if not data.get('buildingNumber') and parent_house.building_number:
                    data['buildingNumber'] = parent_house.building_number
                    print(f"从父节点继承楼栋号: {data['buildingNumber']}")
                    
                if not data.get('unitNumber') and parent_house.unit_number:
                    data['unitNumber'] = parent_house.unit_number
                    print(f"从父节点继承单元号: {data['unitNumber']}")
        
        # 根据房屋级别验证必要字段
        level = data['level']
        if level == 1:  # 区级
            if not data.get('districtNumber'):
                return jsonify({
                    'success': False,
                    'error': '区级房屋必须提供区号'
                }), 400
        elif level == 2:  # 楼栋级
            if not data.get('districtNumber') or not data.get('buildingNumber'):
                return jsonify({
                    'success': False,
                    'error': '楼栋级房屋必须提供区号和楼栋号'
                }), 400
        elif level == 3:  # 单元级
            if not data.get('districtNumber') or not data.get('buildingNumber') or not data.get('unitNumber'):
                return jsonify({
                    'success': False,
                    'error': '单元级房屋必须提供区号、楼栋号和单元号'
                }), 400
        elif level == 4:  # 房间级
            if not data.get('districtNumber') or not data.get('buildingNumber') or not data.get('unitNumber') or not data.get('roomNumber'):
                return jsonify({
                    'success': False,
                    'error': '房间级房屋必须提供区号、楼栋号、单元号和房间号'
                }), 400
        
        # 构建完整名称
        full_name = ''
        if parent_house and level == 4:  # 只有房间级才需要特殊处理
            parent_name_parts = parent_house.house_full_name.split('单元')[0]
            full_name = f"{parent_name_parts}单元{data['roomNumber']}室"
        elif not data.get('fullName'):
            # 根据级别构建默认的完整名称
            community_name = ''
            try:
                from backend.models.community_info import CommunityInfo
                community = CommunityInfo.query.get(data['communityId'])
                if community:
                    community_name = community.community_name
            except Exception as e:
                print(f"获取社区名称失败: {str(e)}")
            
            if level == 1:
                full_name = f"{community_name}{data['districtNumber']}区"
            elif level == 2:
                full_name = f"{community_name}{data['districtNumber']}区{data['buildingNumber']}栋"
            elif level == 3:
                full_name = f"{community_name}{data['districtNumber']}区{data['buildingNumber']}栋{data['unitNumber']}单元"
            elif level == 4:
                full_name = f"{community_name}{data['districtNumber']}区{data['buildingNumber']}栋{data['unitNumber']}单元{data['roomNumber']}室"
        
        new_house = HouseInfo(
            community_id=data['communityId'],
            parent_id=data.get('parentId'),
            district_number=data.get('districtNumber'),
            building_number=data.get('buildingNumber'),
            unit_number=data.get('unitNumber'),
            room_number=data.get('roomNumber'),
            house_full_name=full_name or data.get('fullName', ''),
            house_level=level
        )
        
        db.session.add(new_house)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': new_house.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"添加房屋失败: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

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
            return jsonify({
                'success': False,
                'error': '房屋不存在'
            }), 404
            
        # 检查是否有子节点
        children = HouseInfo.query.filter_by(parent_id=id).first()
        if children:
            return jsonify({
                'success': False,
                'error': '该节点下还有子节点，请先删除子节点'
            }), 400
        
        # 检查是否有关联的业主
        owners = OwnerInfo.query.filter_by(house_id=id).first()
        if owners:
            return jsonify({
                'success': False,
                'error': '该房屋下有关联业主，请先解除关联'
            }), 400
            
        db.session.delete(house)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '删除成功'
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"删除房屋失败: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

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