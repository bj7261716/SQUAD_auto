"""
基礎自動化腳本範例

這是一個簡單的自動化腳本，展示如何：
1. 連接 ADB
2. 擷取螢幕
3. 識別 UI 元素
4. 執行點擊操作
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from capture import ScreenCapture
from vision import TemplateMatcher
from automation import ADBController
from config import get_config
from loguru import logger


class BasicBot:
    """基礎自動化機器人"""
    
    def __init__(self):
        """初始化"""
        logger.info("初始化機器人...")
        
        # 載入配置
        self.config = get_config()
        
        # 初始化螢幕擷取
        region = self.config.get('capture.region')
        self.capturer = ScreenCapture(
            region=region,
            resize=tuple(self.config.get('capture.resize', [640, 360])),
            fps_limit=self.config.get('capture.fps', 30)
        )
        
        # 初始化 ADB
        adb_config = self.config.get('automation.adb', {})
        self.adb = ADBController(
            host=adb_config.get('host', '127.0.0.1'),
            port=adb_config.get('port', 5555)
        )
        
        # 初始化模板匹配
        self.matcher = TemplateMatcher(threshold=0.75)
        
        # 連接 ADB
        if not self.adb.connect():
            raise ConnectionError("無法連接 ADB")
        
        logger.success("✅ 機器人初始化完成")
    
    def find_and_click(self, template_name: str, timeout: float = 5.0) -> bool:
        """
        尋找模板並點擊
        
        Args:
            template_name: 模板名稱
            timeout: 超時時間（秒）
            
        Returns:
            是否成功
        """
        logger.info(f"尋找並點擊: {template_name}")
        
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            # 擷取螢幕
            frame = self.capturer.capture()
            
            # 尋找模板
            match = self.matcher.match(frame, template_name)
            
            if match:
                x, y, confidence = match
                logger.success(f"✅ 找到 {template_name} at ({x}, {y})")
                
                # 點擊（需要將截圖座標轉換為實際螢幕座標）
                # 這裡假設沒有縮放，實際使用時需要調整
                self.adb.tap(x, y)
                
                return True
            
            time.sleep(0.5)
        
        logger.warning(f"⚠️  未找到 {template_name}（超時）")
        return False
    
    def wait_for_template(self, template_name: str, timeout: float = 10.0) -> bool:
        """
        等待模板出現
        
        Args:
            template_name: 模板名稱
            timeout: 超時時間（秒）
            
        Returns:
            是否找到
        """
        logger.info(f"等待模板出現: {template_name}")
        
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            frame = self.capturer.capture()
            match = self.matcher.match(frame, template_name)
            
            if match:
                logger.success(f"✅ 模板出現: {template_name}")
                return True
            
            time.sleep(0.5)
        
        logger.warning(f"⚠️  模板未出現: {template_name}（超時）")
        return False
    
    def run_simple_loop(self):
        """執行簡單的循環邏輯"""
        logger.info("開始執行自動化循環...")
        logger.info("這是一個示範，實際邏輯需要根據遊戲調整")
        
        try:
            loop_count = 0
            
            while True:
                loop_count += 1
                logger.info(f"\n===== 循環 {loop_count} =====")
                
                # 示範邏輯（需要根據實際遊戲調整）
                
                # 1. 等待並點擊「開始戰鬥」按鈕
                logger.info("步驟 1: 尋找開始戰鬥按鈕...")
                # if self.find_and_click('start_battle', timeout=10):
                #     logger.success("✅ 點擊開始戰鬥")
                # else:
                #     logger.warning("未找到開始戰鬥按鈕，跳過")
                
                # 2. 等待戰鬥載入
                logger.info("步驟 2: 等待戰鬥載入...")
                time.sleep(3)
                
                # 3. 執行戰鬥操作
                logger.info("步驟 3: 執行戰鬥...")
                for i in range(5):
                    logger.info(f"  戰鬥動作 {i+1}/5")
                    # 這裡可以加入實際的戰鬥邏輯
                    time.sleep(1)
                
                # 4. 等待戰鬥結束
                logger.info("步驟 4: 等待戰鬥結束...")
                time.sleep(5)
                
                # 5. 點擊領取獎勵
                logger.info("步驟 5: 領取獎勵...")
                # if self.find_and_click('claim_reward', timeout=5):
                #     logger.success("✅ 領取獎勵")
                
                logger.success(f"✅ 循環 {loop_count} 完成")
                
                # 暫停一下
                time.sleep(2)
                
                # 示範模式只執行 3 次
                if loop_count >= 3:
                    logger.info("示範模式，停止循環")
                    break
        
        except KeyboardInterrupt:
            logger.info("\n⚠️  使用者中斷")
    
    def cleanup(self):
        """清理資源"""
        logger.info("清理資源...")
        self.capturer.close()
        self.adb.disconnect()
        logger.success("✅ 清理完成")


def main():
    """主程式"""
    logger.info("=" * 60)
    logger.info("🤖 基礎自動化腳本")
    logger.info("=" * 60)
    
    try:
        # 建立機器人
        bot = BasicBot()
        
        # 執行循環
        bot.run_simple_loop()
        
    except Exception as e:
        logger.error(f"❌ 發生錯誤: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # 清理
        if 'bot' in locals():
            bot.cleanup()
    
    logger.info("=" * 60)
    logger.info("程式結束")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
