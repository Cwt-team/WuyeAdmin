import socket
import json
import time
import threading
import mysql.connector
from datetime import datetime

# 连接 MySQL 数据库
try:
    db = mysql.connector.connect(
        host="localhost",      # 数据库主机地址
        user="root",           # 数据库用户名
        password="password",   # 数据库密码
        database="wuye_admin"  # 数据库名称
    )
    cursor = db.cursor(dictionary=True)
    print("成功连接到 MySQL 数据库")
except mysql.connector.Error as err:
    print(f"MySQL 连接错误: {err}")
    exit(1)

# 创建必要的表
try:
    # 设备表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS equipment (
        id INT AUTO_INCREMENT PRIMARY KEY,
        equipmentId VARCHAR(50) UNIQUE,
        equipmentName VARCHAR(100),
        ip VARCHAR(50),
        port INT DEFAULT 7998,
        communityCode VARCHAR(50),
        status VARCHAR(20) DEFAULT 'unknown',
        lastStatusTime DATETIME
    )
    ''')

    # 设备状态历史表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS equipment_status_history (
        id INT AUTO_INCREMENT PRIMARY KEY,
        equipmentId VARCHAR(50),
        previousStatus VARCHAR(20),
        newStatus VARCHAR(20),
        changeTime DATETIME,
        INDEX (equipmentId)
    )
    ''')
    
    db.commit()
    print("数据库表已创建或已存在")
except mysql.connector.Error as err:
    print(f"创建表错误: {err}")
    exit(1)

def monitor_device(device_id, device_ip, device_port=7998, community_id="000000"):
    """监控特定设备的在线状态"""
    print(f"开始监控设备 {device_id} ({device_ip}:{device_port})")
    
    # 获取设备当前状态
    cursor.execute("SELECT status FROM equipment WHERE equipmentId = %s", (device_id,))
    result = cursor.fetchone()
    last_status = result['status'] if result else None
    
    while True:
        current_status = check_device_status(device_id, device_ip, device_port, community_id)
        
        # 如果状态发生变化，记录到历史记录中
        if last_status != current_status:
            print(f"设备 {device_id} 状态变更: {last_status} -> {current_status}")
            
            # 更新设备状态
            now = datetime.now()
            cursor.execute(
                "UPDATE equipment SET status = %s, lastStatusTime = %s WHERE equipmentId = %s",
                (current_status, now, device_id)
            )
            
            # 记录状态变更历史
            cursor.execute(
                "INSERT INTO equipment_status_history (equipmentId, previousStatus, newStatus, changeTime) VALUES (%s, %s, %s, %s)",
                (device_id, last_status, current_status, now)
            )
            db.commit()
            
            last_status = current_status
        
        # 每30秒检查一次设备状态
        time.sleep(30)

def check_device_status(device_id, device_ip, device_port=7998, community_id="000000"):
    """检查设备状态，返回 'online' 或 'offline'"""
    try:
        # 创建UDP套接字
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.settimeout(3)  # 设置3秒超时
        
        # 构造心跳包
        heartbeat_data = {
            "cmd": "heart",
            "communityId": community_id,
            "deviceCode": device_id
        }
        
        # 发送心跳包
        message = json.dumps(heartbeat_data).encode('utf-8')
        udp_socket.sendto(message, (device_ip, device_port))
        
        # 等待响应
        try:
            response, addr = udp_socket.recvfrom(1024)
            response_data = json.loads(response.decode('utf-8'))
            
            # 检查响应是否成功
            if response_data.get("result") == "0" and response_data.get("cmd") == "heartack":
                return "online"
            else:
                return "offline"
        except socket.timeout:
            return "offline"
    except Exception as e:
        print(f"检查设备 {device_id} 状态时出错: {e}")
        return "offline"
    finally:
        udp_socket.close()

def start_monitoring_all_devices():
    """开始监控所有设备"""
    # 获取所有设备
    cursor.execute("SELECT equipmentId, ip, port, communityCode FROM equipment WHERE ip IS NOT NULL AND ip != ''")
    devices = cursor.fetchall()
    
    if not devices:
        print("没有找到可监控的设备")
        return
    
    # 为每个设备创建监控线程
    for device in devices:
        device_id = device['equipmentId']
        device_ip = device['ip']
        device_port = device['port'] or 7998
        community_id = device['communityCode'] or "000000"
        
        # 创建并启动监控线程
        thread = threading.Thread(
            target=monitor_device,
            args=(device_id, device_ip, device_port, community_id),
            daemon=True
        )
        thread.start()
        print(f"已启动设备 {device_id} ({device_ip}) 的监控线程")

def add_test_device():
    """添加测试设备到数据库"""
    try:
        # 检查设备是否已存在
        cursor.execute("SELECT * FROM equipment WHERE equipmentId = %s", ("200111",))
        if not cursor.fetchone():
            # 添加测试设备
            cursor.execute(
                "INSERT INTO equipment (equipmentId, equipmentName, ip, port, communityCode, status) VALUES (%s, %s, %s, %s, %s, %s)",
                ("200111", "测试门禁设备", "192.168.1.2", 7998, "123456", "unknown")
            )
            db.commit()
            print("已添加测试设备")
        else:
            print("测试设备已存在")
    except mysql.connector.Error as err:
        print(f"添加测试设备错误: {err}")

if __name__ == "__main__":
    # 添加测试设备
    add_test_device()
    
    # 开始监控所有设备
    start_monitoring_all_devices()
    
    # 保持主线程运行
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        print("监控程序已停止")
    finally:
        # 关闭数据库连接
        cursor.close()
        db.close() 