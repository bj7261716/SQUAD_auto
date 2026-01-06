"""
螢幕擷取測試腳本

測試 MSS 函式庫是否能正常擷取螢幕，並顯示視窗。
"""

import cv2
import mss
import numpy as np
import time


def test_screen_capture():
    """測試螢幕擷取功能"""
    print("=" * 60)
    print("📸 螢幕擷取測試")
    print("=" * 60)
    print()
    
    print("ℹ️  操作說明:")
    print("   - 按 'q' 鍵退出")
    print("   - 按 's' 鍵截圖並儲存")
    print("   - 視窗會顯示即時螢幕擷取")
    print()
    print("⚠️  請確保模擬器視窗可見，稍後需要調整擷取區域")
    print()
    
    input("按 Enter 開始測試...")
    
    # 預設擷取區域（全螢幕）
    with mss.mss() as sct:
        # 列出所有螢幕
        print(f"偵測到 {len(sct.monitors)} 個螢幕:")
        for i, monitor in enumerate(sct.monitors):
            if i == 0:
                print(f"  Monitor {i}: 所有螢幕組合")
            else:
                print(f"  Monitor {i}: {monitor}")
        print()
        
        # 使用主螢幕（monitor 1）
        monitor = sct.monitors[1]
        
        print(f"開始擷取螢幕 1...")
        print(f"解析度: {monitor['width']}x{monitor['height']}")
        print()
        
        # FPS 計算
        fps_start_time = time.time()
        fps_frame_count = 0
        fps = 0
        
        screenshot_count = 0
        
        while True:
            # 擷取螢幕
            img = sct.grab(monitor)
            
            # 轉換為 numpy array
            frame = np.array(img)
            
            # 轉換色彩空間 (BGRA -> BGR)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
            
            # 縮小顯示（避免視窗太大）
            display_width = 1280
            display_height = int(frame.shape[0] * (display_width / frame.shape[1]))
            frame_resized = cv2.resize(frame, (display_width, display_height))
            
            # 計算 FPS
            fps_frame_count += 1
            if time.time() - fps_start_time > 1.0:
                fps = fps_frame_count
                fps_frame_count = 0
                fps_start_time = time.time()
            
            # 顯示 FPS 和說明
            cv2.putText(
                frame_resized,
                f"FPS: {fps}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )
            
            cv2.putText(
                frame_resized,
                "Press 'q' to quit, 's' to save screenshot",
                (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )
            
            # 顯示視窗
            cv2.imshow("Screen Capture Test", frame_resized)
            
            # 鍵盤事件
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q'):
                print("退出測試...")
                break
            elif key == ord('s'):
                screenshot_count += 1
                filename = f"screenshot_{screenshot_count}.png"
                cv2.imwrite(filename, frame)
                print(f"✅ 截圖已儲存: {filename}")
        
        cv2.destroyAllWindows()
    
    print()
    print("=" * 60)
    print("✅ 螢幕擷取測試完成")
    print("=" * 60)
    print()
    print("📝 下一步:")
    print("   1. 打開模擬器並啟動「運氣突擊隊」")
    print("   2. 執行 python tests/test_region_capture.py")
    print("   3. 手動調整擷取區域以對準遊戲視窗")


def test_region_capture():
    """測試指定區域擷取"""
    print("=" * 60)
    print("📸 區域擷取測試")
    print("=" * 60)
    print()
    
    # 預設區域
    region = {
        "top": 100,
        "left": 100,
        "width": 1280,
        "height": 720
    }

    # 嘗試從 config 讀取
    try:
        import yaml
        with open("configs/config.yaml", "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
            if 'capture' in config and 'region' in config['capture']:
                cfg_region = config['capture']['region']
                region['top'] = cfg_region.get('top', 100)
                region['left'] = cfg_region.get('left', 100)
                region['width'] = cfg_region.get('width', 1280)
                region['height'] = cfg_region.get('height', 720)
                print("✅ 已載入 config.yaml 中的設定")
    except Exception as e:
        print(f"⚠️ 無法讀取 config.yaml: {e}")
    
    print("⚠️  請根據你的模擬器位置調整以下座標:")
    print(f"   Top: {region['top']}")
    print(f"   Left: {region['left']}")
    print(f"   Width: {region['width']}")
    print(f"   Height: {region['height']}")
    print()
    
    # 讓使用者調整座標
    try:
        print("提示: 直接按 Enter 使用預設值")
        top = input(f"Top [{region['top']}]: ").strip()
        if top:
            region['top'] = int(top)
        
        left = input(f"Left [{region['left']}]: ").strip()
        if left:
            region['left'] = int(left)
        
        width = input(f"Width [{region['width']}]: ").strip()
        if width:
            region['width'] = int(width)
        
        height = input(f"Height [{region['height']}]: ").strip()
        if height:
            region['height'] = int(height)
    except ValueError:
        print("❌ 輸入無效，使用預設值")
    
    print()
    print(f"使用區域: {region}")
    print()
    
    with mss.mss() as sct:
        print("開始擷取指定區域...")
        print("按 'q' 鍵退出")
        print()
        
        while True:
            # 擷取指定區域
            img = sct.grab(region)
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
            
            # 顯示邊框（幫助對齊）
            cv2.rectangle(
                frame,
                (0, 0),
                (frame.shape[1] - 1, frame.shape[0] - 1),
                (0, 255, 0),
                3
            )
            
            cv2.putText(
                frame,
                "Adjust region in configs/config.yaml",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )
            
            cv2.imshow("Region Capture Test", frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cv2.destroyAllWindows()
    
    print()
    print("✅ 區域擷取測試完成")
    print()
    print("📝 請將以下座標更新到 configs/config.yaml:")
    print(f"""
capture:
  region:
    left: {region['left']}
    top: {region['top']}
    width: {region['width']}
    height: {region['height']}
""")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--region":
        test_region_capture()
    else:
        test_screen_capture()
