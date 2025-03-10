import socket
import json
import time

# 配置服务器 IP 和端口
UDP_IP = "0.0.0.0"  # 监听所有网卡
UDP_PORT = 7998

def send_heartbeat(server_ip, server_port):
    # 创建 UDP 套接字
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # 设置超时
    udp_socket.settimeout(5)
    
    try:
        while True:
            try:
                # 构造心跳包数据（与接口文档要求一致）
                heartbeat_data = {
                    "communityId": "123456",
                    "deviceCode": "200111",
                    "cmd": "heart",  # 必须是 "heart"
                    "softVer": "1.02.03.04",
                    "name": "阳光花园",
                    "deviceSn": "asjkdfiouasdjk123"
                }
                message = json.dumps(heartbeat_data).encode('utf-8')  # 转换为 JSON 字符串并编码
                
                # 发送心跳包前先关闭之前的连接并创建新连接
                udp_socket.close()
                udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                udp_socket.settimeout(5)
                
                # 发送心跳包
                udp_socket.sendto(message, (server_ip, server_port))
                print(f"已发送心跳包到 {server_ip}:{server_port}")
                
                # 等待服务器响应
                response, addr = udp_socket.recvfrom(1024)
                response_data = json.loads(response.decode('utf-8'))
                
                # 检查返回的 result 和 cmd 字段
                if response_data.get("result") == "0" and response_data.get("cmd") == "heartack":
                    print("心跳发送成功:", response_data.get("message"))
                else:
                    print("心跳发送失败:", response_data.get("message"))
            except socket.timeout:
                print("等待服务器响应超时")
            except ConnectionResetError:
                print("连接被重置，可能是远程主机关闭了连接")
            except Exception as e:
                print(f"发送心跳包失败: {e}")
                
            # 等待 10 秒后再次发送
            time.sleep(10)
    finally:
        udp_socket.close()

if __name__ == '__main__':
    # 根据接口文档要求设置服务器地址和端口
    server_ip = '127.0.0.1'  # 先测试本地回环地址
    server_port = 7998       # 端口号为 7998
    
    # 如果提供了命令行参数，则使用命令行参数
    import sys
    if len(sys.argv) > 1:
        server_ip = sys.argv[1]
    if len(sys.argv) > 2:
        server_port = int(sys.argv[2])
        
    print(f"开始向 {server_ip}:{server_port} 发送心跳包...")
    send_heartbeat(server_ip, server_port)
