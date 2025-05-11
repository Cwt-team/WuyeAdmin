from flask import Blueprint, jsonify, request, current_app
from backend.models.device import Device, DevicePhoto, DeviceFace, SipConfig
from backend.models.community_info import CommunityInfo
from backend.db import db
from datetime import datetime
import time
import os
import logging
import socket


# 创建蓝图
device_bp = Blueprint('device', __name__)
logger = logging.getLogger(__name__)

# 设置UDP服务器
UDP_IP = "0.0.0.0"  # 监听所有网络接口
UDP_PORT = 7998     # 与文档中的端口一致

# 初始化UDP服务器
def init_udp_server(app):
    with app.app_context():
        try:
            # 创建UDP socket
            udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            
            # 设置端口重用选项
            udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            try:
                udp_socket.bind((UDP_IP, UDP_PORT))
                
                # 非阻塞模式
                udp_socket.setblocking(False)
                
                logger.info(f"UDP服务器启动在 {UDP_IP}:{UDP_PORT}")
                
                # 在后台线程中处理UDP消息
                import threading
                udp_thread = threading.Thread(target=handle_udp_messages, args=(udp_socket, app))
                udp_thread.daemon = True
                udp_thread.start()
                
            except OSError as e:
                if e.errno == 10048:  # 端口已被使用
                    logger.info(f"UDP端口 {UDP_PORT} 已被其他进程占用，可能是热重载导致的，忽略此错误")
                else:
                    raise e
            
        except Exception as e:
            logger.error(f"UDP服务器启动失败: {str(e)}")

# 处理UDP消息的函数
def handle_udp_messages(sock, app):
    with app.app_context():
        while True:
            try:
                data, addr = sock.recvfrom(1024)  # 接收数据
                logger.info(f"收到来自 {addr} 的UDP消息: {data}")
                
                # 解析消息
                import json
                try:
                    message = json.loads(data.decode('utf-8'))
                    if message.get('cmd') == 'heart':
                        handle_heartbeat(message, addr, sock)
                except json.JSONDecodeError:
                    logger.error("无法解析JSON消息")
                except Exception as e:
                    logger.error(f"处理UDP消息时出错: {str(e)}")
                    
            except BlockingIOError:
                # 没有消息，休眠一小段时间
                import time
                time.sleep(0.1)
            except Exception as e:
                logger.error(f"UDP接收循环中出错: {str(e)}")
                time.sleep(1)  # 出错后等待一段时间再继续

# 处理心跳包
def handle_heartbeat(message, addr, sock):
    try:
        community_id = message.get('communityId')
        device_code = message.get('deviceCode')
        soft_ver = message.get('softVer')
        name = message.get('name')
        device_sn = message.get('deviceSn')
        
        # 查找或创建设备记录
        device = Device.query.filter_by(device_code=device_code).first()
        
        if device:
            # 更新设备
            device.status = '在线'
            device.last_heart_time = datetime.now()
            if soft_ver:
                device.soft_ver = soft_ver
            if name:
                device.name = name
            if device_sn:
                device.device_sn = device_sn
        else:
            # 创建新设备
            device = Device(
                community_id=community_id,
                device_code=device_code,
                device_sn=device_sn,
                name=name,
                soft_ver=soft_ver,
                status='在线',
                last_heart_time=datetime.now()
            )
            db.session.add(device)
            
        db.session.commit()
        
        # 发送确认响应
        response = {
            "result": "0",
            "message": "心跳发送成功",
            "cmd": "heartack"
        }
        sock.sendto(json.dumps(response).encode('utf-8'), addr)
        
    except Exception as e:
        logger.error(f"处理心跳包时出错: {str(e)}")
        
        # 尝试发送错误响应
        try:
            response = {
                "result": "1",
                "message": f"处理心跳包时出错: {str(e)}",
                "cmd": "heartack"
            }
            sock.sendto(json.dumps(response).encode('utf-8'), addr)
        except:
            pass

# API路由部分

# 获取设备列表
@device_bp.route('/api/sip/devices', methods=['GET'])
def get_devices():
    try:
        page = int(request.args.get('page', 1))
        size = int(request.args.get('size', 10))
        community_id = request.args.get('communityId')
        device_code = request.args.get('deviceCode')
        device_type = request.args.get('deviceType')
        status = request.args.get('status')
        
        query = Device.query
        
        if community_id:
            query = query.filter(Device.community_id == community_id)
        if device_code:
            query = query.filter(Device.device_code.like(f"%{device_code}%"))
        if device_type:
            query = query.filter(Device.device_type == device_type)
        if status:
            query = query.filter(Device.status == status)
            
        total = query.count()
        devices = query.order_by(Device.created_at.desc())\
            .offset((page - 1) * size)\
            .limit(size)\
            .all()
            
        return jsonify({
            'devices': [device.to_dict() for device in devices],
            'total': total
        })
        
    except Exception as e:
        logger.error(f"获取设备列表失败: {str(e)}")
        return jsonify({'error': str(e)}), 500

# 获取设备详情
@device_bp.route('/api/sip/device/<int:device_id>', methods=['GET'])
def get_device(device_id):
    try:
        device = Device.query.get(device_id)
        if not device:
            return jsonify({'error': '设备不存在'}), 404
            
        return jsonify(device.to_dict())
        
    except Exception as e:
        logger.error(f"获取设备详情失败: {str(e)}")
        return jsonify({'error': str(e)}), 500

# 添加/更新设备
@device_bp.route('/api/sip/device', methods=['POST'])
def add_device():
    try:
        data = request.json
        device_code = data.get('deviceCode')
        
        # 检查是否已存在
        device = Device.query.filter_by(device_code=device_code).first()
        
        if device:
            # 更新设备
            device.community_id = data.get('communityId', device.community_id)
            device.device_sn = data.get('deviceSn', device.device_sn)
            device.name = data.get('name', device.name)
            device.soft_ver = data.get('softVer', device.soft_ver)
            device.device_type = data.get('deviceType', device.device_type)
            device.status = data.get('status', device.status)
        else:
            # 创建新设备
            device = Device(
                community_id=data.get('communityId'),
                device_code=data.get('deviceCode'),
                device_sn=data.get('deviceSn'),
                name=data.get('name'),
                soft_ver=data.get('softVer'),
                device_type=data.get('deviceType', '其他'),
                status=data.get('status', '离线')
            )
            db.session.add(device)
            
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '设备保存成功',
            'device': device.to_dict()
        })
        
    except Exception as e:
        logger.error(f"添加/更新设备失败: {str(e)}")
        return jsonify({'error': str(e)}), 500

# 删除设备
@device_bp.route('/api/sip/device/<int:device_id>', methods=['DELETE'])
def delete_device(device_id):
    try:
        device = Device.query.get(device_id)
        if not device:
            return jsonify({'error': '设备不存在'}), 404
            
        db.session.delete(device)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '设备删除成功'
        })
        
    except Exception as e:
        logger.error(f"删除设备失败: {str(e)}")
        return jsonify({'error': str(e)}), 500

# 设备密码校验
@device_bp.route('/api/sip/oneLock', methods=['POST'])
def verify_one_time_password():
    try:
        community_id = request.form.get('communityId')
        device_code = request.form.get('deviceCode')
        one_password = request.form.get('onePassword')
        
        # TODO: 实现一次性密码验证逻辑
        # 这里是一个简单的示例，实际应用中需要查询数据库验证密码
        # 并返回相应的用户信息
        
        # 模拟验证成功
        return jsonify({
            "data": {
                "unitId": "0021",
                "phone": "13533335555",
                "roomNumber": "0101"
            },
            "message": "验证成功",
            "page": None,
            "code": "0000"
        })
        
    except Exception as e:
        logger.error(f"密码校验失败: {str(e)}")
        return jsonify({
            "data": None,
            "message": f"验证失败: {str(e)}",
            "page": None,
            "code": "9999"
        }), 500

# 设备开锁记录
@device_bp.route('/api/sip/unlockCallback', methods=['POST'])
def unlock_callback():
    try:
        community_id = request.form.get('communityId')
        device_code = request.form.get('deviceCode')
        unlock_type = request.form.get('type')
        result = request.form.get('result')
        phone = request.form.get('phone')
        room_number = request.form.get('roomNumber')
        unit_id = request.form.get('unitId')
        file = request.form.get('file')
        
        # TODO: 保存开锁记录到unlock_record表
        # 这里需要根据实际数据库结构实现
        
        return jsonify({
            "data": None,
            "message": "添加成功",
            "page": None,
            "code": "0000"
        })
        
    except Exception as e:
        logger.error(f"保存开锁记录失败: {str(e)}")
        return jsonify({
            "data": None,
            "message": f"保存失败: {str(e)}",
            "page": None,
            "code": "9999"
        }), 500

# 设备开锁照片上传
@device_bp.route('/api/sip/addUpload', methods=['POST'])
def add_upload():
    try:
        if 'uploadFile' not in request.files:
            return jsonify({
                "code": "9999",
                "message": "没有上传文件",
                "page": None,
                "data": None
            }), 400
            
        file = request.files['uploadFile']
        new_name = request.form.get('newName', file.filename)
        
        # 确保上传目录存在
        upload_dir = os.path.join(current_app.static_folder, 'uploadImages')
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
            
        # 保存文件
        file_path = os.path.join(upload_dir, new_name)
        file.save(file_path)
        
        # 返回文件URL
        file_url = f"/data/page/uploadImages/{new_name}"
        
        return jsonify({
            "code": "0000",
            "message": "",
            "page": None,
            "data": file_url
        })
        
    except Exception as e:
        logger.error(f"上传照片失败: {str(e)}")
        return jsonify({
            "code": "9999",
            "message": f"上传失败: {str(e)}",
            "page": None,
            "data": None
        }), 500

# 人脸照片下载
@device_bp.route('/api/sip/updateImage', methods=['POST'])
def update_image():
    try:
        community_id = request.form.get('communityId')
        device_code = request.form.get('deviceCode')
        timestrap = request.form.get('timestrap')  # 时间戳
        state = request.form.get('state')
        
        # 查询设备人脸记录
        query = DeviceFace.query
        
        if community_id:
            query = query.filter(DeviceFace.community_id == community_id)
        if timestrap:
            query = query.filter(DeviceFace.create_time > int(timestrap))
        if state:
            query = query.filter(DeviceFace.state == state)
            
        faces = query.all()
            
        return jsonify({
            "data": [face.to_dict() for face in faces],
            "id": f"msg_{int(time.time())}",
            "message": "查询成功",
            "page": None,
            "code": "0000"
        })
        
    except Exception as e:
        logger.error(f"获取人脸照片失败: {str(e)}")
        return jsonify({
            "data": None,
            "id": f"msg_{int(time.time())}",
            "message": f"查询失败: {str(e)}",
            "page": None,
            "code": "9999"
        }), 500

# 人脸照片检测结果
@device_bp.route('/api/sip/authImage', methods=['POST'])
def auth_image():
    try:
        phone = request.form.get('phone')
        state = request.form.get('state')
        if_file = request.form.get('iffile')
        
        # 处理文件上传
        if if_file == '1' and 'file' in request.files:
            file = request.files['file']
            # TODO: 处理人脸特征码文件
            
        # 更新人脸状态
        if phone and state:
            faces = DeviceFace.query.filter_by(phone=phone).all()
            for face in faces:
                face.state = state
            db.session.commit()
            
        return jsonify({
            "code": "0000",
            "message": "验证结果接收成功",
            "data": {}
        })
        
    except Exception as e:
        logger.error(f"人脸照片验证结果处理失败: {str(e)}")
        return jsonify({
            "code": "9999",
            "message": f"验证结果处理失败: {str(e)}",
            "data": {}
        }), 500

# 获取SIP电话信息
@device_bp.route('/api/sip/getPhone', methods=['GET'])
def get_phone():
    try:
        unit_id = request.args.get('unitId')  # 固定4位
        community_id_str = request.args.get('communityId')  # 固定6位
        room_number = request.args.get('roomNumber')  # 固定4位
        device_code = request.args.get('deviceCode')  # 固定6位
        
        logger.info(f"获取SIP电话信息请求: unitId={unit_id}, communityId={community_id_str}, roomNumber={room_number}, deviceCode={device_code}")
        
        # 将字符串的communityId转换为数据库中的INT类型
        # 方法1: 直接查询community_info表中是否存在对应的community_number
        community = db.session.query(CommunityInfo).filter_by(community_number=community_id_str).first()
        
        if not community:
            logger.warning(f"未找到匹配的小区: communityId={community_id_str}")
            return jsonify({
                "SIPPassWD": "",
                "SIPUser": "",
                "phone": "",
                "SIPPort": "",
                "SIPHost": ""
            }), 404
            
        community_id = community.id
        
        # 使用SipConfig模型查询数据
        query = SipConfig.query.filter_by(
            community_id=community_id,
            unit_id=unit_id,
            room_number=room_number,
            is_enabled=True
        )
        
        # 如果提供了设备代码，添加到查询条件中
        if device_code:
            query = query.filter(SipConfig.device_code == device_code)
            
        sip_config = query.first()
        
        if not sip_config:
            logger.warning(f"未找到匹配的SIP配置: unitId={unit_id}, communityId={community_id}, roomNumber={room_number}")
            return jsonify({
                "SIPPassWD": "",
                "SIPUser": "",
                "phone": "",
                "SIPPort": "",
                "SIPHost": ""
            }), 404
        
        # 构建响应数据
        response_data = {
            "SIPPassWD": sip_config.sip_password,
            "SIPUser": sip_config.sip_user,
            "phone": sip_config.phone,
            "SIPPort": sip_config.sip_port,
            "SIPHost": sip_config.sip_host
        }
        
        # 返回成功响应
        return jsonify(response_data), 200
        
    except Exception as e:
        logger.error(f"获取SIP电话信息失败: {str(e)}")
        return jsonify({
            "SIPPassWD": "",
            "SIPUser": "",
            "phone": "",
            "SIPPort": "",
            "SIPHost": ""
        }), 500 