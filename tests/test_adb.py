"""
ADB 連接測試腳本

測試 ADB 連接功能並顯示設備資訊。
"""

import sys
from pathlib import Path

# 添加 src 到路徑
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from automation import ADBController
from loguru import logger


def main():
    print("=" * 60)
    print("🔌 ADB 連接測試")
    print("=" * 60)
    print()
    
    # 取得連接資訊
    print("請確認以下資訊:")
    host = input("ADB 主機位址 [127.0.0.1]: ").strip() or "127.0.0.1"
    port = input("ADB 埠號 [5555]: ").strip() or "5555"
    port = int(port)
    
    print()
    print(f"嘗試連接到 {host}:{port}...")
    print()
    
    # 建立控制器
    adb = ADBController(host=host, port=port)
    
    # 嘗試連接
    if not adb.connect():
        print()
        print("❌ 連接失敗！")
        print()
        print ("檢查清單:")
        print("1. 模擬器是否正在執行？")
        print("2. ADB 是否已安裝？（試試執行 'adb version'）")
        print("3. 埠號是否正確？")
        print()
        print("常見模擬器埠號:")
        print("   - LDPlayer: 5555, 5556, 5557...")
        print("   - BlueStacks: 5555")
        print("   - NoxPlayer: 62001")
        sys.exit(1)
    
    print()
    print("✅ 連接成功！")
    print()
    
    # 取得螢幕解析度
    print("📱 設備資訊:")
    size = adb.get_screen_size()
    if size:
        print(f"   螢幕解析度: {size[0]}x{size[1]}")
    
    print()
    print("🧪 測試基本功能...")
    print()
    
    # 測試點擊
    test_click = input("是否測試點擊螢幕中心？(y/n): ").strip().lower()
    if test_click == 'y' and size:
        center_x = size[0] // 2
        center_y = size[1] // 2
        print(f"點擊座標: ({center_x}, {center_y})")
        if adb.tap(center_x, center_y):
            print("✅ 點擊測試成功")
        else:
            print("❌ 點擊測試失敗")
    
    print()
    
    # 測試返回鍵
    test_back = input("是否測試返回鍵？(y/n): ").strip().lower()
    if test_back == 'y':
        if adb.back():
            print("✅ 返回鍵測試成功")
        else:
            print("❌ 返回鍵測試失敗")
    
    print()
    print("=" * 60)
    print("✅ 所有測試完成！")
    print("=" * 60)
    print()
    print("📝 下一步:")
    print("   1. 在模擬器中開啟「運氣突擊隊」")
    print("   2. 執行 python tests/test_screen_capture.py --region")
    print("   3. 調整 configs/config.yaml 中的擷取區域")
    print()
    
    # 斷開連接
    adb.disconnect()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  測試已取消")
        sys.exit(0)
