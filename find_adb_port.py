import socket
import subprocess
import os

def check_port(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex(('127.0.0.1', port))
    sock.close()
    return result == 0

def scan_adb_ports():
    print("🔍 開始掃描常見 ADB 埠號...")
    
    # 常見模擬器埠號範圍
    common_ports = [5555, 5557, 5559, 5561, 5563,  # LDPlayer / BlueStacks (Hyper-V off)
                    62001, 62025, 62026, 62027,    # Nox / 夜神
                    21503, 21513, 21523,           # Memu / 逍遙
                    7555]                          # MuMu / 網易
                    
    found_ports = []
    
    for port in common_ports:
        if check_port(port):
            print(f"✅ 發現開放埠號: {port}")
            found_ports.append(port)
        else:
            print(f"❌ {port} 未開放")
            
    # 也掃描 5555-5585 範圍 (覆蓋多開)
    print("\n🔍 掃描 5555-5585 範圍...")
    for port in range(5555, 5585):
        if port not in common_ports and check_port(port):
            print(f"✅ 發現開放埠號: {port}")
            found_ports.append(port)

    print("\n" + "="*30)
    if found_ports:
        print(f"🎉 找到可能的 ADB 埠號: {found_ports}")
        print("正在嘗試使用 ADB 連接這些埠號...")
        
        adb_path = r"D:\cheat\luck-raiders-ai-bot\tools\platform-tools\adb.exe"
        if not os.path.exists(adb_path):
            adb_path = "adb"
            
        for port in found_ports:
            print(f"\n嘗試連接 127.0.0.1:{port} ...")
            try:
                cmd = f'"{adb_path}" connect 127.0.0.1:{port}'
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=5)
                print(result.stdout)
                
                if "connected" in result.stdout.lower():
                    print(f"✨ 成功連接到埠號: {port} ✨")
                    print(f"請在 config.yaml 中設定 port: {port}")
                    break
            except Exception as e:
                print(f"連接失敗: {e}")
    else:
        print("❌ 未找到任何開放的 ADB 埠號。")
        print("請確認模擬器已啟動，且 'ADB 調試' 已設定為 '開啟本地連接'。")

if __name__ == "__main__":
    scan_adb_ports()
