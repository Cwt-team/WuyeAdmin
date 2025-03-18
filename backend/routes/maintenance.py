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
        unit_number = request.args.get('unitNumber')
        
        print("\n=== 开始查询房间号 ===")
        print(f"请求参数:")
        print(f"- 社区ID: {community_id}, 类型: {type(community_id)}")
        print(f"- 区号: {district_number}, 类型: {type(district_number)}")
        print(f"- 楼栋号: {building_number}, 类型: {type(building_number)}")
        print(f"- 单元号: {unit_number}, 类型: {type(unit_number)}")
        
        if not all([community_id, building_number, district_number, unit_number]):
            print("参数验证失败，缺少必要参数")
            return jsonify([])
            
        # 修改查询语句
        sql = text("""
            SELECT DISTINCT
                h.id,
                h.room_number,
                h.unit_number,
                h.house_full_name
            FROM house_info h
            WHERE h.community_id = :community_id
            AND h.district_number = :district_number
            AND h.building_number = :building_number
            AND h.unit_number = :unit_number
            AND h.house_level = 4
            ORDER BY CAST(SUBSTRING(h.room_number, 1, 2) AS SIGNED),
                     CAST(SUBSTRING(h.room_number, 3, 2) AS SIGNED)
        """)
        
        print("\n=== 执行SQL查询 ===")
        params = {
            'community_id': community_id,
            'district_number': district_number,
            'building_number': building_number,
            'unit_number': unit_number
        }
        print(f"查询参数: {params}")
        
        result = db.session.execute(sql, params)
        rooms = result.fetchall()
        
        print(f"\n=== 查询结果 ===")
        print(f"总共查询到 {len(rooms)} 个房间")
        
        if rooms:
            print("第一个房间信息:")
            print(f"- ID: {rooms[0].id}")
            print(f"- 房间号: {rooms[0].room_number}")
            print(f"- 单元号: {rooms[0].unit_number}")
            print(f"- 房间名: {rooms[0].house_full_name}")
        
        return jsonify([{
            'id': row.id,
            'room_number': row.room_number,
            'unit_number': row.unit_number,
            'house_full_name': row.house_full_name
        } for row in rooms])
        
    except Exception as e:
        print("\n=== 查询出错 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        db.session.rollback()
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

@maintenance_bp.route('/api/maintenance/debug/rooms', methods=['GET'])
def debug_rooms():
    try:
        # 获取并打印请求参数
        community_id = request.args.get('communityId', type=int)
        building_number = request.args.get('buildingNumber')
        district_number = request.args.get('districtNumber')
        unit_number = request.args.get('unitNumber')
        
        print("\n=== 开始调试房间查询 ===")
        print(f"请求参数:")
        print(f"- 社区ID: {community_id}, 类型: {type(community_id)}")
        print(f"- 区号: {district_number}, 类型: {type(district_number)}")
        print(f"- 楼栋号: {building_number}, 类型: {type(building_number)}")
        print(f"- 单元号: {unit_number}, 类型: {type(unit_number)}")
        
        # 查询所有匹配条件的房间
        sql = text("""
            SELECT 
                h.*
            FROM house_info h
            WHERE h.community_id = :community_id
            AND h.district_number = :district_number
            AND h.building_number = :building_number
            AND h.unit_number = :unit_number
        """)
        
        result = db.session.execute(sql, {
            'community_id': community_id,
            'district_number': district_number,
            'building_number': building_number,
            'unit_number': unit_number
        })
        
        rooms = result.fetchall()
        print(f"\n=== 查询结果 ===")
        print(f"总共查询到 {len(rooms)} 条记录")
        
        # 打印每条记录的详细信息
        for room in rooms:
            print("\n房间信息:")
            print(f"- ID: {room.id}")
            print(f"- 社区ID: {room.community_id}")
            print(f"- 区号: {room.district_number}")
            print(f"- 楼栋号: {room.building_number}")
            print(f"- 单元号: {room.unit_number}")
            print(f"- 房间号: {room.room_number}")
            print(f"- 房间名: {room.house_full_name}")
            print(f"- 房间级别: {room.house_level}")
        
        return jsonify({
            'total': len(rooms),
            'rooms': [{
                'id': row.id,
                'community_id': row.community_id,
                'district_number': row.district_number,
                'building_number': row.building_number,
                'unit_number': row.unit_number,
                'room_number': row.room_number,
                'house_full_name': row.house_full_name,
                'house_level': row.house_level
            } for row in rooms]
        })
        
    except Exception as e:
        print("\n=== 调试查询出错 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        return jsonify({'error': str(e)}), 500