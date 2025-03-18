from flask import Blueprint, jsonify, request
from db import db
from datetime import datetime
import logging
from models.maintenance_request import MaintenanceRequest
from models.community import CommunityInfo
from models.house import HouseInfo
from sqlalchemy import text

# 配置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

maintenance_bp = Blueprint('maintenance', __name__)

@maintenance_bp.route('/api/maintenance', methods=['GET'])
def get_maintenance_list():
    logger.info("开始处理维修列表请求")
    logger.info(f"请求参数: {request.args}")
    
    try:
        # 获取请求参数
        page = int(request.args.get('page', 1))
        size = int(request.args.get('size', 10))
        community = request.args.get('community')
        status = request.args.get('status')
        start_date = request.args.get('startDate')
        end_date = request.args.get('endDate')
        
        logger.debug(f"处理后的参数: page={page}, size={size}, community={community}, status={status}")
        
        # 构建查询
        query = MaintenanceRequest.query\
            .join(CommunityInfo, MaintenanceRequest.community_id == CommunityInfo.id)\
            .join(HouseInfo, MaintenanceRequest.house_id == HouseInfo.id)\
            .filter(MaintenanceRequest.is_deleted == 0)
            
        if community:
            query = query.filter(MaintenanceRequest.community_id == community)
        if status:
            query = query.filter(MaintenanceRequest.status == status)
        if start_date:
            query = query.filter(MaintenanceRequest.report_time >= start_date)
        if end_date:
            query = query.filter(MaintenanceRequest.report_time <= end_date)
            
        # 计算总数
        total = query.count()
        
        # 获取分页数据
        items = query.order_by(MaintenanceRequest.report_time.desc())\
            .offset((page - 1) * size)\
            .limit(size)\
            .all()
            
        logger.debug(f"查询到 {len(items)} 条记录")
        
        return jsonify({
            'items': [item.to_dict() for item in items],
            'total': total
        })
        
    except Exception as e:
        logger.error(f"获取报修列表失败: {str(e)}", exc_info=True)
        return jsonify({'message': '获取报修列表失败', 'error': str(e)}), 500 

# 获取社区列表
@maintenance_bp.route('/api/maintenance/communities', methods=['GET'])
def get_communities():
    try:
        # 查询社区信息
        sql = text("""
            SELECT 
                id,
                community_name
            FROM community_info 
            ORDER BY id
        """)
        
        result = db.session.execute(sql)
        communities = result.fetchall()
        
        if not communities:
            logging.warning("未查询到社区数据")
            return jsonify([])
            
        logging.info(f"查询到 {len(communities)} 个社区")
        
        return jsonify([{
            'id': row.id,
            'community_name': row.community_name  # 确保返回社区名称
        } for row in communities])
        
    except Exception as e:
        logging.error(f"获取社区列表失败: {str(e)}")
        return jsonify({
            'error': '获取社区列表失败',
            'message': str(e)
        }), 500

# 获取楼栋列表
@maintenance_bp.route('/api/maintenance/buildings/<int:community_id>', methods=['GET'])
def get_buildings(community_id):
    try:
        # 添加调试日志
        print(f"正在查询社区ID: {community_id} 的楼栋数据")
        
        # 检查社区是否存在
        community = db.session.query(CommunityInfo).filter_by(id=community_id).first()
        if not community:
            print(f"社区ID {community_id} 不存在")
            return jsonify({'error': '社区不存在'}), 404
            
        # 主查询
        sql = text("""
            SELECT DISTINCT 
                h.id,
                h.building_number,
                h.house_full_name,
                h.district_number
            FROM house_info h
            WHERE h.community_id = :community_id
            AND h.house_level = 2
            AND h.building_number IS NOT NULL
            ORDER BY 
                CAST(h.district_number AS SIGNED),
                CAST(h.building_number AS SIGNED)
        """)
        
        try:
            result = db.session.execute(sql, {
                'community_id': community_id
            })
            buildings = result.fetchall()
            
            # 打印调试信息
            print(f"查询到 {len(buildings)} 条楼栋数据")
            for building in buildings:
                print(f"楼栋信息: ID={building.id}, 区号={building.district_number}, "
                      f"栋号={building.building_number}, 名称={building.house_full_name}")
            
            return jsonify([{
                'id': row.id,
                'building_number': row.building_number,
                'house_full_name': row.house_full_name,
                'district_number': row.district_number
            } for row in buildings])
            
        except Exception as e:
            print(f"执行主查询时出错: {str(e)}")
            return jsonify({'error': '数据库查询失败'}), 500
            
    except Exception as e:
        print(f"获取楼栋列表失败: {str(e)}")
        return jsonify({'error': '获取楼栋列表失败'}), 500

# 获取房间号列表
@maintenance_bp.route('/api/maintenance/rooms', methods=['GET'])
def get_rooms():
    try:
        community_id = request.args.get('communityId', type=int)
        building_number = request.args.get('buildingNumber')
        district_number = request.args.get('districtNumber')
        
        print(f"正在查询房间号，社区ID: {community_id}, 区号: {district_number}, 楼栋号: {building_number}")
        
        if not all([community_id, building_number]):
            return jsonify([])
            
        # 先检查数据是否存在
        check_sql = text("""
            SELECT COUNT(*) as count
            FROM house_info h
            WHERE h.community_id = :community_id
            AND h.building_number = :building_number
            AND h.district_number = :district_number
        """)
        
        count_result = db.session.execute(check_sql, {
            'community_id': community_id,
            'building_number': building_number,
            'district_number': district_number
        }).scalar()
        
        print(f"找到 {count_result} 条房屋数据")
        
        # 主查询
        sql = text("""
            SELECT DISTINCT
                h.id,
                h.room_number,
                h.unit_number,
                h.house_full_name,
                h.house_level
            FROM house_info h
            WHERE h.community_id = :community_id
            AND h.building_number = :building_number
            AND h.district_number = :district_number
            AND h.house_level = 3
            ORDER BY 
                CAST(h.unit_number AS SIGNED),
                CAST(h.room_number AS SIGNED)
        """)
        
        result = db.session.execute(sql, {
            'community_id': community_id,
            'building_number': building_number,
            'district_number': district_number
        })
        
        rooms = result.fetchall()
        print(f"查询到 {len(rooms)} 个房间")
        
        if not rooms:
            # 检查是否存在单元数据
            unit_sql = text("""
                SELECT DISTINCT
                    h.id,
                    h.unit_number,
                    h.house_full_name
                FROM house_info h
                WHERE h.community_id = :community_id
                AND h.building_number = :building_number
                AND h.district_number = :district_number
                AND h.house_level = 3
            """)
            
            unit_result = db.session.execute(unit_sql, {
                'community_id': community_id,
                'building_number': building_number,
                'district_number': district_number
            })
            
            units = unit_result.fetchall()
            print(f"查询到 {len(units)} 个单元")
            
            if units:
                # 如果有单元数据，为每个单元生成房间
                rooms = []
                for unit in units:
                    for floor in range(1, 19):  # 假设18层
                        for room in range(1, 3):  # 假设每层2户
                            room_number = f"{floor:02d}{room:02d}"
                            rooms.append({
                                'id': None,
                                'room_number': room_number,
                                'unit_number': unit.unit_number,
                                'house_full_name': f"{unit.house_full_name}{room_number}室"
                            })
        
        return jsonify([{
            'id': row.id if hasattr(row, 'id') else None,
            'room_number': row.room_number if hasattr(row, 'room_number') else row['room_number'],
            'unit_number': row.unit_number if hasattr(row, 'unit_number') else row['unit_number'],
            'house_full_name': row.house_full_name if hasattr(row, 'house_full_name') else row['house_full_name']
        } for row in rooms])
        
    except Exception as e:
        print(f"获取房间号列表失败: {str(e)}")
        return jsonify({'error': '获取房间号列表失败'}), 500

# 获取单元列表
@maintenance_bp.route('/api/maintenance/units', methods=['GET'])
def get_units():
    try:
        community_id = request.args.get('communityId', type=int)
        building_number = request.args.get('buildingNumber')
        district_number = request.args.get('districtNumber')
        
        print(f"正在查询单元，社区ID: {community_id}, 区号: {district_number}, 楼栋号: {building_number}")
        
        if not all([community_id, building_number, district_number]):
            return jsonify([])
            
        sql = text("""
            SELECT DISTINCT
                h.id,
                h.unit_number,
                h.house_full_name
            FROM house_info h
            WHERE h.community_id = :community_id
            AND h.building_number = :building_number
            AND h.district_number = :district_number
            AND h.house_level = 3
            ORDER BY CAST(h.unit_number AS SIGNED)
        """)
        
        result = db.session.execute(sql, {
            'community_id': community_id,
            'building_number': building_number,
            'district_number': district_number
        })
        
        units = result.fetchall()
        print(f"查询到 {len(units)} 个单元")
        
        if not units:
            # 如果没有单元数据，默认生成两个单元
            units = [
                {'id': None, 'unit_number': '1', 'house_full_name': '1单元'},
                {'id': None, 'unit_number': '2', 'house_full_name': '2单元'}
            ]
        
        return jsonify([{
            'id': row.id if hasattr(row, 'id') else row['id'],
            'unit_number': row.unit_number if hasattr(row, 'unit_number') else row['unit_number'],
            'house_full_name': row.house_full_name if hasattr(row, 'house_full_name') else row['house_full_name']
        } for row in units])
        
    except Exception as e:
        print(f"获取单元列表失败: {str(e)}")
        return jsonify({'error': '获取单元列表失败'}), 500