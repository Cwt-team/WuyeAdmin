# udp_server.py
import socket, json, time
import subprocess
import threading


def start_udp_server():
    UDP_IP = "0.0.0.0"
    UDP_PORT = 7998
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind((UDP_IP, UDP_PORT))
    print(f"UDP 服务已启动，监听 {UDP_PORT} 端口")

    while True:
        try:
            data, addr = udp_socket.recvfrom(1024)
            message = json.loads(data.decode("utf-8"))
            print(f"收到来自 {addr} 的数据: {message}")
            if message.get("cmd") == "heart":
                response = json.dumps({"result": "0", "message": "心跳发送成功", "cmd": "heartack"})
                udp_socket.sendto(response.encode("utf-8"), addr)
        except Exception as e:
            print("UDP 处理错误:", e)


def check_device_network(ip_address):
    try:
        # 执行 ping 命令
        if ip_address == "localhost" or ip_address == "127.0.0.1":
            return True
            
        # Windows 系统使用 -n 参数
        ping_param = '-n' if subprocess.os.name == 'nt' else '-c'
        result = subprocess.run(['ping', ping_param, '4', ip_address], 
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE,
                               timeout=5)
        return result.returncode == 0
    except Exception as e:
        print(f"测试网络连接失败: {e}")
        return False


def simulate_device():
    """模拟一个门禁设备，接收心跳包并回复"""
    UDP_IP = "0.0.0.0"  # 监听所有网卡
    UDP_PORT = 7998
    
    # 创建 UDP 套接字
    device_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    device_socket.bind((UDP_IP, UDP_PORT))
    print(f"模拟设备已启动，监听 {UDP_PORT} 端口")
    
    while True:
        try:
            # 接收数据
            data, addr = device_socket.recvfrom(1024)
            try:
                message = json.loads(data.decode('utf-8'))
                print(f"模拟设备收到来自 {addr} 的数据: {message}")
                
                # 如果是心跳包请求
                if message.get("cmd") == "heart":
                    # 构造响应数据
                    response = {
                        "result": "0",
                        "message": "心跳接收成功",
                        "cmd": "heartack",
                        "deviceStatus": "normal"
                    }
                    
                    # 发送响应
                    device_socket.sendto(json.dumps(response).encode('utf-8'), addr)
                    print(f"模拟设备已回复心跳包到 {addr}")
            except json.JSONDecodeError:
                print(f"收到非JSON数据: {data}")
        except Exception as e:
            print(f"模拟设备错误: {e}")


def send_test_heartbeat(target_ip, target_port=7998):
    """发送测试心跳包到指定IP和端口"""
    try:
        # 创建 UDP 套接字
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # 设置超时
        udp_socket.settimeout(5)
        
        # 构造心跳包数据
        heartbeat_data = {
            "communityId": "123456",
            "deviceCode": "200111",
            "cmd": "heart",
            "softVer": "1.02.03.04",
            "name": "测试设备",
            "deviceSn": "TEST123456"
        }
        
        # 转换为 JSON 字符串并编码
        message = json.dumps(heartbeat_data).encode('utf-8')
        
        # 发送心跳包
        udp_socket.sendto(message, (target_ip, target_port))
        print(f"已发送测试心跳包到 {target_ip}:{target_port}")
        
        # 等待响应
        response, addr = udp_socket.recvfrom(1024)
        response_data = json.loads(response.decode('utf-8'))
        
        print(f"收到来自 {addr} 的响应: {response_data}")
        return True
    except socket.timeout:
        print("等待响应超时")
        return False
    except Exception as e:
        print(f"发送测试心跳包失败: {e}")
        return False
    finally:
        udp_socket.close()


if __name__ == '__main__':
    # 启动模式选择
    import sys
    
    if len(sys.argv) > 1:
        mode = sys.argv[1]
        if mode == "server":
            # 启动UDP服务器
            start_udp_server()
        elif mode == "device":
            # 启动模拟设备
            simulate_device()
        elif mode == "test":
            # 测试模式
            if len(sys.argv) > 2:
                target_ip = sys.argv[2]
                target_port = int(sys.argv[3]) if len(sys.argv) > 3 else 7998
                send_test_heartbeat(target_ip, target_port)
            else:
                print("用法: python udp_server.py test <target_ip> [target_port]")
        else:
            print("未知模式，请使用 server, device 或 test")
    else:
        # 默认启动UDP服务器
        start_udp_server()
