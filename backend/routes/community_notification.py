from flask import Blueprint, jsonify, request
from backend.models.community_notification import CommunityNotification
from backend.db import db
from datetime import datetime

community_notification_bp = Blueprint('community_notification', __name__)

@community_notification_bp.route('/api/community-notices', methods=['GET'])
def get_notices():
    try:
        page = int(request.args.get('page', 1))
        size = int(request.args.get('size', 10))
        title = request.args.get('title')
        start_date = request.args.get('startDate')
        end_date = request.args.get('endDate')
        
        query = CommunityNotification.query
        
        if title:
            query = query.filter(CommunityNotification.title.like(f'%{title}%'))
        if start_date:
            query = query.filter(CommunityNotification.display_start_time >= start_date)
        if end_date:
            query = query.filter(CommunityNotification.display_end_time <= end_date)
            
        total = query.count()
        notices = query.order_by(CommunityNotification.created_at.desc())\
            .offset((page - 1) * size)\
            .limit(size)\
            .all()
            
        return jsonify({
            'records': [notice.to_dict() for notice in notices],
            'total': total
        })
        
    except Exception as e:
        print(f"获取小区通知列表失败: {str(e)}")
        return jsonify({'error': str(e)}), 500

@community_notification_bp.route('/api/community-notices', methods=['POST'])
def create_notice():
    try:
        data = request.json
        notice = CommunityNotification(
            community_id=data['communityId'],
            title=data['title'],
            content=data['content'],
            display_start_time=datetime.strptime(data['displayStartTime'], '%Y-%m-%d').date() if data.get('displayStartTime') else None,
            display_end_time=datetime.strptime(data['displayEndTime'], '%Y-%m-%d').date() if data.get('displayEndTime') else None
        )
        
        db.session.add(notice)
        db.session.commit()
        
        return jsonify({'message': '创建成功', 'data': notice.to_dict()})
        
    except Exception as e:
        db.session.rollback()
        print(f"创建小区通知失败: {str(e)}")
        return jsonify({'error': str(e)}), 500

@community_notification_bp.route('/api/community-notices/<int:notice_id>', methods=['DELETE'])
def delete_notice(notice_id):
    try:
        notice = CommunityNotification.query.get(notice_id)
        if not notice:
            return jsonify({'error': '通知不存在'}), 404
            
        db.session.delete(notice)
        db.session.commit()
        
        return jsonify({'message': '删除成功'})
        
    except Exception as e:
        db.session.rollback()
        print(f"删除小区通知失败: {str(e)}")
        return jsonify({'error': str(e)}), 500 