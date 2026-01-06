import sys
import time
import os
import yaml
from pathlib import Path
from loguru import logger

# 添加 src 到路徑
sys.path.insert(0, str(Path(__file__).parent / "src"))

from capture import ScreenCapture
from vision import TemplateMatcher
from automation import ADBController

def run_bot():
    logger.info("=" * 60)
    logger.info("🤖 運氣突擊隊 - 自動開始 Bot")
    logger.info("=" * 60)
    
    # 1. 載入配置
    try:
        with open("configs/config.yaml", "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
            region = config['capture']['region']
            resize = config['capture'].get('resize')
            if resize:
                resize = tuple(resize)
            adb_config = config['automation']['adb']
    except Exception as e:
        logger.error(f"❌ 無法讀取配置: {e}")
        return

    # 2. 初始化模組
    logger.info("正在初始化模組...")
    
    # ADB
    adb = ADBController(
        host=adb_config.get('host', '127.0.0.1'),
        port=adb_config.get('port', 5555)
    )
    if not adb.connect():
        logger.error("❌ 無法連接 ADB，請檢查模擬器")
        return
    
    # 螢幕擷取
    capturer = ScreenCapture(region=region, resize=resize)
    
    # 視覺識別
    matcher = TemplateMatcher(threshold=0.8)
    matcher.load_template('button_start', 'data/templates/button_start.png')
    
    logger.success("✅ 系統就緒，開始監控畫面...")
    logger.info("按 Ctrl+C 停止")
    
    try:
        while True:
            # 抓取畫面
            frame = capturer.capture()
            
            # 尋找開始按鈕
            match = matcher.match(frame, 'button_start')
            
            if match:
                x, y, conf = match
                logger.success(f"🎯 發現開始按鈕! (信心度: {conf:.2f}) - 圖片座標: ({x}, {y})")
                
                # 獲取螢幕解析度
                # 注意：wm size 顯示 1280x720，但直立模式下座標系應為 720x1280
                # 我們假設模擬器是 720x1280 (DPI 可能不同，但邏輯座標通常是這樣)
                
                # 視窗 (Capture) 解析度
                win_w = 545
                win_h = 970
                
                # 模擬器目標解析度
                target_w = 720
                target_h = 1280
                
                # 計算映射後的座標
                # 先減去 Crop 的偏移量 (因為 x, y 是相對於 Crop 區域的)
                # 但我們的 x, y 已經是 Crop 區域內的點
                
                # 公式：
                # 1. 還原到視窗相對座標: (x, y) 就是相對於 Crop 左上角的座標
                # 2. 如果 Crop 是整個模擬器畫面，那比例就是 target_w / win_w
                
                scale_x = target_w / win_w
                scale_y = target_h / win_h
                
                mapped_x = int(x * scale_x)
                mapped_y = int(y * scale_y)
                
                logger.info(f"座標映射: ({x}, {y}) -> ({mapped_x}, {mapped_y}) [Scale: {scale_x:.2f}, {scale_y:.2f}]")
                
                # 再次嘗試點擊
                adb.tap(mapped_x, mapped_y)
                # 保險起見也 swipe 一下
                # adb.swipe(mapped_x, mapped_y, mapped_x, mapped_y, 100)
                
                logger.info("✅ 點擊指令已發送")
                time.sleep(3) 
                
            else:
                # 沒找到，稍微等待再試
                time.sleep(0.5)
                # 可以在這裡加入一個 spinner 用來顯示 "正在搜尋..."
                
    except KeyboardInterrupt:
        logger.info("\n🛑 Bot 已停止")
    except Exception as e:
        logger.error(f"❌ 發生錯誤: {e}")
    finally:
        capturer.close()
        adb.disconnect()

if __name__ == "__main__":
    run_bot()
