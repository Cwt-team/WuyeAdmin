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
        # 简化查询，只获取基本字段
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
            'community_name': row.community_name
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
        sql = """
            SELECT DISTINCT id, building_number, house_full_name
            FROM house_info
            WHERE community_id = :community_id
            AND house_level = 2
            AND is_deleted = 0
            ORDER BY CAST(building_number AS SIGNED)
        """
        buildings = db.session.execute(sql, {'community_id': community_id}).fetchall()
        return jsonify([{
            'id': b.id,
            'building_number': b.building_number,
            'house_full_name': b.house_full_name
        } for b in buildings])
    except Exception as e:
        logging.error(f"获取楼栋列表失败: {str(e)}")
        return jsonify({'error': '获取楼栋列表失败'}), 500

# 获取房间列表
@maintenance_bp.route('/api/maintenance/rooms/<int:community_id>/<string:building_number>', methods=['GET'])
def get_rooms(community_id, building_number):
    try:
        sql = """
            SELECT id, room_number, house_full_name, owner_name, owner_phone
            FROM house_info
            WHERE community_id = :community_id
            AND building_number = :building_number
            AND house_level = 4
            AND is_deleted = 0
            ORDER BY CAST(room_number AS SIGNED)
        """
        rooms = db.session.execute(sql, {
            'community_id': community_id,
            'building_number': building_number
        }).fetchall()
        return jsonify([{
            'id': r.id,
            'room_number': r.room_number,
            'house_full_name': r.house_full_name,
            'owner_name': r.owner_name,
            'owner_phone': r.owner_phone
        } for r in rooms])
    except Exception as e:
        logging.error(f"获取房间列表失败: {str(e)}")
        return jsonify({'error': '获取房间列表失败'}), 500