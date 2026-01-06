"""
完整系統示範

展示如何整合螢幕擷取、模板匹配和 ADB 控制。
"""

import sys
import time
import cv2
from pathlib import Path

# 添加 src 到路徑
# 添加 src 到路徑
sys.path.insert(0, str(Path(__file__).parent / "src"))

from capture import ScreenCapture
from vision import TemplateMatcher
from automation import ADBController
from config import get_config
from loguru import logger


def main():
    """主程式"""
    logger.info("=" * 60)
    logger.info("🎮 運氣突擊隊 AI Bot - 系統示範")
    logger.info("=" * 60)
    
    # 載入配置
    try:
        config = get_config()
        logger.success("✅ 配置檔案載入成功")
    except Exception as e:
        logger.error(f"❌ 無法載入配置檔案: {e}")
        return
    
    # 初始化螢幕擷取
    logger.info("\n初始化螢幕擷取...")
    region = config.get('capture.region')
    
    # 處理 resize 設定
    resize = config.get('capture.resize')
    if resize:
        resize = tuple(resize)
    
    fps = config.get('capture.fps', 30)
    
    capturer = ScreenCapture(
        region=region,
        resize=resize,
        fps_limit=fps
    )
    
    # 初始化 ADB 控制器（可選）
    logger.info("\n初始化 ADB 控制器...")
    adb_config = config.get('automation.adb', {})
    adb = ADBController(
        host=adb_config.get('host', '127.0.0.1'),
        port=adb_config.get('port', 5555)
    )
    
    use_adb = False
    if adb.connect():
        logger.success("✅ ADB 連接成功，將使用 ADB 控制")
        use_adb = True
    else:
        logger.warning("⚠️  ADB 連接失敗，僅展示螢幕擷取")
    
    # 初始化模板匹配器（可選）
    logger.info("\n初始化模板匹配器...")
    matcher = TemplateMatcher(threshold=0.8)
    
    # 嘗試載入模板
    templates_dir = Path("data/templates")
    if templates_dir.exists():
        count = matcher.load_templates_from_dir(str(templates_dir))
        logger.info(f"載入了 {count} 個模板")
    else:
        logger.warning(f"模板目錄不存在: {templates_dir}")
        logger.info("建立模板目錄...")
        templates_dir.mkdir(parents=True, exist_ok=True)
    
    logger.info("\n" + "=" * 60)
    logger.info("系統初始化完成！")
    logger.info("=" * 60)
    logger.info("\n操作說明:")
    logger.info("  按 'q' - 退出")
    logger.info("  按 's' - 截圖")
    logger.info("  按 'c' - 測試點擊（需要 ADB）")
    logger.info("  按 't' - 測試模板匹配（需要已載入模板）")
    logger.info("\n開始運行...\n")
    
    frame_count = 0
    screenshot_count = 0
    
    try:
        while True:
            # 擷取螢幕
            frame = capturer.capture()
            frame_count += 1
            
            # 顯示 FPS
            fps_current = capturer.get_fps()
            cv2.putText(
                frame,
                f"FPS: {fps_current}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )
            
            # 顯示狀態
            status = "ADB: ON" if use_adb else "ADB: OFF"
            cv2.putText(
                frame,
                status,
                (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 255) if use_adb else (0, 0, 255),
                2
            )
            
            # 顯示視窗
            cv2.imshow("Luck Raiders AI Bot - Demo", frame)
            
            # 鍵盤事件
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q'):
                logger.info("退出程式...")
                break
            
            elif key == ord('s'):
                screenshot_count += 1
                filename = f"data/screenshots/demo_{screenshot_count}.png"
                cv2.imwrite(filename, frame)
                logger.success(f"✅ 截圖已儲存: {filename}")
            
            elif key == ord('c'):
                if use_adb:
                    # 測試點擊螢幕中心
                    size = adb.get_screen_size()
                    if size:
                        x, y = size[0] // 2, size[1] // 2
                        logger.info(f"測試點擊: ({x}, {y})")
                        adb.tap(x, y)
                else:
                    logger.warning("ADB 未連接")
            
            elif key == ord('t'):
                # 測試模板匹配
                template_names = matcher.get_template_names()
                if template_names:
                    logger.info(f"正在測試所有模板 ({len(template_names)} 個)...")
                    for template_name in template_names:
                        match = matcher.match(frame, template_name)
                        if match:
                            x, y, conf = match
                            logger.success(
                                f"✅ 找到模板 '{template_name}' "
                                f"at ({x}, {y}), confidence={conf:.2f}"
                            )
                            
                            # 在畫面上畫出來給使用者看
                            h, w = matcher.templates[template_name]['shape']
                            # 從中心點轉換回左上角
                            top_left_x = x - w // 2
                            top_left_y = y - h // 2
                            cv2.rectangle(frame, (top_left_x, top_left_y), (top_left_x + w, top_left_y + h), (0, 255, 0), 2)
                            cv2.putText(frame, f"{template_name} ({conf:.2f})", (top_left_x, top_left_y - 10), 
                                      cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                            cv2.imshow("Luck Raiders AI Bot - Demo", frame)
                        else:
                            logger.info(f"未找到模板 '{template_name}'")
                else:
                    logger.warning("沒有已載入的模板")
    
    except KeyboardInterrupt:
        logger.info("\n程式被中斷")
    
    finally:
        # 清理資源
        capturer.close()
        if use_adb:
            adb.disconnect()
        cv2.destroyAllWindows()
        
        logger.info("\n" + "=" * 60)
        logger.info("系統統計:")
        logger.info(f"  總幀數: {frame_count}")
        logger.info(f"  截圖數: {screenshot_count}")
        logger.info("=" * 60)


if __name__ == "__main__":
    main()
