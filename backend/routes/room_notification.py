from flask import Blueprint, jsonify, request
from backend.models.room_notification import RoomNotification
from backend.db import db
from datetime import datetime

room_notification_bp = Blueprint('room_notification', __name__)

@room_notification_bp.route('/api/room-notifications', methods=['GET'])
def get_notifications():
    try:
        page = int(request.args.get('page', 1))
        size = int(request.args.get('size', 10))
        community_id = request.args.get('communityId')
        title = request.args.get('title')
        start_date = request.args.get('startDate')
        end_date = request.args.get('endDate')
        
        query = RoomNotification.query
        
        if community_id:
            query = query.filter(RoomNotification.community_id == community_id)
        if title:
            query = query.filter(RoomNotification.title.like(f'%{title}%'))
        if start_date:
            query = query.filter(RoomNotification.display_start_time >= start_date)
        if end_date:
            query = query.filter(RoomNotification.display_end_time <= end_date)
            
        total = query.count()
        notifications = query.order_by(RoomNotification.created_at.desc())\
            .offset((page - 1) * size)\
            .limit(size)\
            .all()
            
        return jsonify({
            'records': [notification.to_dict() for notification in notifications],
            'total': total
        })
        
    except Exception as e:
        print(f"获取房间通知列表失败: {str(e)}")
        return jsonify({'error': str(e)}), 500

@room_notification_bp.route('/api/room-notifications', methods=['POST'])
def create_notification():
    try:
        data = request.json
        notification = RoomNotification(
            community_id=data['communityId'],
            house_id=data.get('houseId'),
            title=data['title'],
            content=data['content'],
            display_start_time=datetime.strptime(data['displayStartTime'], '%Y-%m-%d').date() if data.get('displayStartTime') else None,
            display_end_time=datetime.strptime(data['displayEndTime'], '%Y-%m-%d').date() if data.get('displayEndTime') else None
        )
        
        db.session.add(notification)
        db.session.commit()
        
        return jsonify({'message': '创建成功', 'data': notification.to_dict()})
        
    except Exception as e:
        db.session.rollback()
        print(f"创建房间通知失败: {str(e)}")
        return jsonify({'error': str(e)}), 500

@room_notification_bp.route('/api/room-notifications/<int:notification_id>', methods=['DELETE'])
def delete_notification(notification_id):
    try:
        notification = RoomNotification.query.get(notification_id)
        if not notification:
            return jsonify({'error': '通知不存在'}), 404
            
        db.session.delete(notification)
        db.session.commit()
        
        return jsonify({'message': '删除成功'})
        
    except Exception as e:
        db.session.rollback()
        print(f"删除房间通知失败: {str(e)}")
        return jsonify({'error': str(e)}), 500 