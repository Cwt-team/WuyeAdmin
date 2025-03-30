from flask import Blueprint, request, jsonify
from models import DistrictInfo, BuildingInfo, UnitInfo, CommunityInfo
import logging
from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy

# 配置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

common_bp = Blueprint('common', __name__)

# 获取社区列表
@common_bp.route('/api/communities', methods=['GET'])
def get_communities():
    try:
        logger.debug("获取社区列表")
        communities = CommunityInfo.query.filter_by(status=1).all()
        result = [{
            'id': c.id, 
            'community_name': c.community_name
        } for c in communities]
        logger.debug(f"获取到{len(result)}个社区")
        return jsonify(result)
    except Exception as e:
        logger.error(f"获取社区列表失败: {str(e)}")
        return jsonify({'error': str(e)}), 500

# 获取区域列表
@common_bp.route('/api/districts', methods=['GET'])
def get_districts():
    try:
        community_id = request.args.get('communityId')
        if not community_id:
            return jsonify([]), 200
            
        districts = DistrictInfo.query.filter_by(
            community_id=community_id,
            status=1
        ).all()
        
        result = [
            {
                'id': d.id, 
                'name': d.district_name,
                'number': d.district_number
            } 
            for d in districts
        ]
        
        logger.debug(f"获取到{len(result)}个区域")
        return jsonify(result)
    except Exception as e:
        logger.error(f"获取区域列表失败: {str(e)}")
        return jsonify([]), 200

# 获取楼栋列表
@common_bp.route('/api/buildings', methods=['GET'])
def get_buildings():
    try:
        community_id = request.args.get('communityId')
        district_number = request.args.get('districtNumber')
        logger.debug(f"获取楼栋列表，社区ID: {community_id}，区域编号: {district_number}")
        
        if not community_id or not district_number:
            return jsonify([]), 200
            
        # 直接从house_info表查询楼栋数据
        sql = text("""
            SELECT 
                h.id,
                h.building_number as number,
                h.house_full_name as name
            FROM house_info h
            WHERE h.community_id = :community_id
            AND h.district_number = :district_number
            AND h.house_level = 2
            ORDER BY CAST(h.building_number AS SIGNED)
        """)
        
        result = db.session.execute(sql, {
            'community_id': community_id,
            'district_number': district_number
        })
        
        buildings = [
            {
                'id': row.id,
                'name': row.name,
                'number': row.number
            }
            for row in result
        ]
        
        logger.debug(f"获取到{len(buildings)}个楼栋")
        return jsonify(buildings)
        
    except Exception as e:
        logger.error(f"获取楼栋列表失败: {str(e)}")
        return jsonify([]), 200

# 获取单元列表
@common_bp.route('/api/units', methods=['GET'])
def get_units():
    try:
        community_id = request.args.get('communityId')
        district_number = request.args.get('districtNumber')
        building_number = request.args.get('buildingNumber')
        logger.debug(f"获取单元列表，社区ID: {community_id}，区域编号: {district_number}，楼栋编号: {building_number}")
        
        if not community_id or not district_number or not building_number:
            return jsonify([]), 200
            
        # 根据区域编号查询区域ID
        district = DistrictInfo.query.filter_by(
            community_id=community_id,
            district_number=district_number,
            status=1
        ).first()
        
        if not district:
            logger.warning(f"未找到区域，社区ID: {community_id}，区域编号: {district_number}")
            return jsonify([]), 200
            
        # 根据楼栋编号查询楼栋ID
        building = BuildingInfo.query.filter_by(
            community_id=community_id,
            district_id=district.id,
            building_number=building_number,
            status=1
        ).first()
        
        if not building:
            logger.warning(f"未找到楼栋，社区ID: {community_id}，区域ID: {district.id}，楼栋编号: {building_number}")
            return jsonify([]), 200
            
        units = UnitInfo.query.filter_by(
            community_id=community_id,
            district_id=district.id,
            building_id=building.id,
            status=1
        ).all()
        
        result = [
            {
                'id': u.id, 
                'name': u.unit_name,
                'number': u.unit_number
            } 
            for u in units
        ]
        
        logger.debug(f"获取到{len(result)}个单元")
        return jsonify(result)
    except Exception as e:
        logger.error(f"获取单元列表失败: {str(e)}")
        return jsonify([]), 200

@common_bp.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'code': 0,
        'message': 'Service is healthy',
        'data': None
    })

print(DistrictInfo)  # 打印 DistrictInfo 模型，确保导入成功 