from flask import Blueprint, request, jsonify
from models.complaint import Complaint
from models.community_info import CommunityInfo
from db import db
from sqlalchemy import text
from datetime import datetime
import logging
from sqlalchemy.orm import joinedload

complaint_bp = Blueprint('complaint', __name__)

@complaint_bp.route('/api/complaints', methods=['GET'])
def get_complaints():
    """获取投诉建议列表"""
    try:
        # 获取查询参数
        page = int(request.args.get('page', 1))
        size = int(request.args.get('size', 10))
        community_id = request.args.get('communityId')
        type = request.args.get('type')
        status = request.args.get('status')
        start_date = request.args.get('startDate')
        end_date = request.args.get('endDate')
        
        # 构建查询
        query = Complaint.query\
            .options(joinedload(Complaint.community))\
            .options(joinedload(Complaint.user))
        
        # 应用过滤条件
        if community_id:
            query = query.filter(Complaint.community_id == community_id)
        if type:
            query = query.filter(Complaint.type == type)
        if status:
            query = query.filter(Complaint.status == status)
        if start_date:
            query = query.filter(Complaint.created_at >= start_date)
        if end_date:
            query = query.filter(Complaint.created_at <= end_date)
            
        # 计算总数
        total = query.count()
        
        # 获取分页数据
        complaints = query.order_by(Complaint.created_at.desc())\
            .offset((page - 1) * size)\
            .limit(size)\
            .all()
            
        # 添加日志
        logging.info(f"查询参数: community_id={community_id}, type={type}, status={status}")
        logging.info(f"查询到总记录数: {total}")
        logging.info(f"返回记录数: {len(complaints)}")
        
        # 添加更详细的日志
        for complaint in complaints:
            logging.debug(f"处理投诉建议记录: ID={complaint.id}")
            logging.debug(f"关联数据: community={complaint.community}, user={complaint.user}")
            
        result = {
            'code': 200,
            'message': '获取成功',
            'total': total,
            'items': [complaint.to_dict() for complaint in complaints]
        }
        logging.debug(f"返回数据: {result}")
        return jsonify(result)
        
    except Exception as e:
        logging.error(f"获取投诉建议列表失败: {str(e)}", exc_info=True)
        return jsonify({
            'code': 500,
            'message': '获取投诉建议列表失败',
            'error': str(e)
        }), 500

@complaint_bp.route('/api/complaints/<int:id>/reply', methods=['POST'])
def reply_complaint(id):
    """回复投诉建议"""
    try:
        data = request.get_json()
        reply_content = data.get('reply')
        
        if not reply_content:
            return jsonify({
                'code': 400,
                'message': '回复内容不能为空'
            })

        complaint = Complaint.query.get(id)
        if not complaint:
            return jsonify({
                'code': 404,
                'message': '未找到该投诉建议'
            })

        complaint.reply = reply_content
        complaint.reply_time = datetime.now()
        complaint.status = 'completed'  # 更新状态为已处理
        
        db.session.commit()
        
        return jsonify({
            'code': 200,
            'message': '回复成功'
        })

    except Exception as e:
        db.session.rollback()
        logging.error(f"回复投诉建议失败: {str(e)}")
        return jsonify({
            'code': 500,
            'message': '回复失败',
            'error': str(e)
        }), 500

@complaint_bp.route('/api/complaints/<int:id>/status', methods=['PUT'])
def update_complaint_status(id):
    """更新投诉建议状态"""
    try:
        data = request.get_json()
        new_status = data.get('status')
        
        if not new_status:
            return jsonify({
                'code': 400,
                'message': '状态不能为空'
            })

        complaint = Complaint.query.get(id)
        if not complaint:
            return jsonify({
                'code': 404,
                'message': '未找到该投诉建议'
            })

        complaint.status = new_status
        complaint.updated_at = datetime.now()
        
        db.session.commit()
        
        return jsonify({
            'code': 200,
            'message': '状态更新成功'
        })

    except Exception as e:
        db.session.rollback()
        logging.error(f"更新投诉建议状态失败: {str(e)}")
        return jsonify({
            'code': 500,
            'message': '状态更新失败',
            'error': str(e)
        }), 500

@complaint_bp.route('/api/complaints/communities', methods=['GET'])
def get_communities():
    """获取社区列表"""
    try:
        # 查询启用的社区
        communities = CommunityInfo.query\
            .filter_by(is_enabled=1)\
            .order_by(CommunityInfo.id)\
            .all()
        
        if not communities:
            logging.warning("未查询到社区数据")
            return jsonify({
                'code': 200,
                'message': '获取成功',
                'items': []
            })
            
        logging.info(f"查询到 {len(communities)} 个社区")
        
        return jsonify({
            'code': 200,
            'message': '获取成功',
            'items': [{
                'id': community.id,
                'name': community.community_name,  # 前端使用 name 字段
                'label': community.community_name  # 为了兼容 el-select 的显示
            } for community in communities]
        })
        
    except Exception as e:
        logging.error(f"获取社区列表失败: {str(e)}")
        return jsonify({
            'code': 500,
            'message': '获取社区列表失败',
            'error': str(e)
        }), 500 