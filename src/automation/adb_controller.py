"""
ADB 控制器模組

使用 ADB 控制 Android 模擬器。
"""

import subprocess
import time
import os
import sys
from typing import Tuple, Optional
from loguru import logger
import yaml

class ADBController:
    """ADB 控制器類別"""
    
    def __init__(self, host: str = "127.0.0.1", port: int = 5555, adb_path: Optional[str] = None):
        """
        初始化 ADB 控制器
        
        Args:
            host: ADB 主機位址
            port: ADB 埠號
            adb_path: 自訂 ADB 執行檔路徑 (如果不指定，嘗試從 config 讀取，或使用預設)
        """
        self.host = host
        self.port = port
        self.device = f"{host}:{port}"
        self.connected = False
        
        # 決定 ADB 路徑
        if adb_path:
            self.adb_path = adb_path
        else:
            # 嘗試從 config.yaml 讀取
            try:
                with open("configs/config.yaml", "r", encoding="utf-8") as f:
                    config = yaml.safe_load(f)
                    self.adb_path = config.get("automation", {}).get("adb", {}).get("path", "adb")
            except Exception:
                self.adb_path = "adb"

        if self.adb_path != "adb" and not os.path.exists(self.adb_path):
             logger.warning(f"⚠️ 自訂 ADB 路徑不存在: {self.adb_path}，將使用系統 'adb'")
             self.adb_path = "adb"

        logger.info(f"初始化 ADB 控制器: {self.device} (使用 ADB: {self.adb_path})")
    
    def _run_cmd(self, cmd: str, timeout: int = 10) -> Tuple[bool, str]:
        """
        執行 Shell 指令並處理編碼
        
        Returns:
            (success, output)
        """
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                timeout=timeout
            )
            # 嘗試解碼 stdout
            try:
                output = result.stdout.decode('utf-8', errors='replace')
            except Exception:
                output = str(result.stdout)
                
            if result.returncode != 0:
                # 嘗試解碼 stderr
                try:
                    error = result.stderr.decode('utf-8', errors='replace')
                except Exception:
                    error = str(result.stderr)
                return False, output + "\n" + error
                
            return True, output
        except subprocess.TimeoutExpired:
            return False, "Timeout"
        except Exception as e:
            return False, str(e)

    def connect(self) -> bool:
        """
        連接到 ADB 設備
        
        Returns:
            是否連接成功
        """
        try:
            # 嘗試連接
            cmd = f'"{self.adb_path}" connect {self.device}'
            success, output = self._run_cmd(cmd)
            
            if success and "connected" in output.lower():
                self.connected = True
                logger.success(f"✅ ADB 連接成功: {self.device}")
                return True
            else:
                logger.error(f"❌ ADB 連接失敗: {output.strip()}")
                return False
                
        except Exception as e:
            logger.error(f"❌ ADB 連接錯誤: {e}")
            return False
    
    def disconnect(self):
        """斷開 ADB 連接"""
        try:
            cmd = f'"{self.adb_path}" disconnect {self.device}'
            self._run_cmd(cmd)
            self.connected = False
            logger.info(f"ADB 已斷開: {self.device}")
        except Exception as e:
            logger.error(f"斷開連接時發生錯誤: {e}")
    
    def is_connected(self) -> bool:
        """
        檢查是否已連接
        
        Returns:
            是否已連接
        """
        try:
            cmd = f'"{self.adb_path}" devices'
            success, output = self._run_cmd(cmd)
            
            return success and self.device in output
            
        except Exception as e:
            logger.error(f"檢查連接狀態時發生錯誤: {e}")
            return False
    
    def tap(self, x: int, y: int, delay: float = 0.1) -> bool:
        """
        點擊指定座標
        
        Args:
            x: X 座標
            y: Y 座標
            delay: 點擊後的延遲（秒）
            
        Returns:
            是否成功
        """
        if not self.connected:
            logger.warning("ADB 未連接，嘗試重新連接...")
            if not self.connect():
                return False
        
        try:
            cmd = f'"{self.adb_path}" -s {self.device} shell input tap {x} {y}'
            self._run_cmd(cmd, timeout=5)
            
            logger.debug(f"點擊座標: ({x}, {y})")
            
            if delay > 0:
                time.sleep(delay)
            
            return True
            
        except Exception as e:
            logger.error(f"點擊失敗: {e}")
            return False
    
    def swipe(
        self,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        duration: int = 300,
        delay: float = 0.3
    ) -> bool:
        """
        滑動
        
        Args:
            x1, y1: 起始座標
            x2, y2: 結束座標
            duration: 滑動持續時間（毫秒）
            delay: 滑動後的延遲（秒）
            
        Returns:
            是否成功
        """
        if not self.connected:
            logger.warning("ADB 未連接，嘗試重新連接...")
            if not self.connect():
                return False
        
        try:
            cmd = f'"{self.adb_path}" -s {self.device} shell input swipe {x1} {y1} {x2} {y2} {duration}'
            self._run_cmd(cmd, timeout=10)
            
            logger.debug(f"滑動: ({x1}, {y1}) -> ({x2}, {y2})")
            
            if delay > 0:
                time.sleep(delay)
            
            return True
            
        except Exception as e:
            logger.error(f"滑動失敗: {e}")
            return False
    
    def input_text(self, text: str, delay: float = 0.1) -> bool:
        """
        輸入文字
        
        Args:
            text: 要輸入的文字
            delay: 輸入後的延遲（秒）
            
        Returns:
            是否成功
        """
        if not self.connected:
            if not self.connect():
                return False
        
        try:
            # 替換空格為 %s
            text = text.replace(" ", "%s")
            
            cmd = f'"{self.adb_path}" -s {self.device} shell input text "{text}"'
            self._run_cmd(cmd, timeout=5)
            
            logger.debug(f"輸入文字: {text}")
            
            if delay > 0:
                time.sleep(delay)
            
            return True
            
        except Exception as e:
            logger.error(f"輸入文字失敗: {e}")
            return False
    
    def press_key(self, key_code: int, delay: float = 0.1) -> bool:
        """
        按下按鍵
        
        Args:
            key_code: 按鍵代碼（例如：3=HOME, 4=BACK）
            delay: 按鍵後的延遲（秒）
            
        Returns:
            是否成功
        """
        if not self.connected:
            if not self.connect():
                return False
        
        try:
            cmd = f'"{self.adb_path}" -s {self.device} shell input keyevent {key_code}'
            self._run_cmd(cmd, timeout=5)
            
            logger.debug(f"按下按鍵: {key_code}")
            
            if delay > 0:
                time.sleep(delay)
            
            return True
            
        except Exception as e:
            logger.error(f"按鍵失敗: {e}")
            return False
    
    def home(self):
        """回到主畫面"""
        return self.press_key(3)
    
    def back(self):
        """返回"""
        return self.press_key(4)
    
    def get_screen_size(self) -> Optional[Tuple[int, int]]:
        """
        取得螢幕解析度
        
        Returns:
            (width, height) 或 None
        """
        try:
            cmd = f'"{self.adb_path}" -s {self.device} shell wm size'
            success, output = self._run_cmd(cmd, timeout=5)
            
            if not success:
                return None
            
            # 解析輸出: "Physical size: 1280x720"
            output = output.strip()
            if "x" in output:
                size_str = output.split(":")[-1].strip()
                width, height = map(int, size_str.split("x"))
                logger.info(f"螢幕解析度: {width}x{height}")
                return (width, height)
            
            return None
            
        except Exception as e:
            logger.error(f"取得螢幕解析度失敗: {e}")
            return None
    
    def screenshot(self, save_path: str = "/sdcard/screenshot.png") -> bool:
        """
        截圖（儲存在設備上）
        
        Args:
            save_path: 儲存路徑（設備上）
            
        Returns:
            是否成功
        """
        if not self.connected:
            if not self.connect():
                return False
        
        try:
            cmd = f'"{self.adb_path}" -s {self.device} shell screencap -p {save_path}'
            self._run_cmd(cmd, timeout=10)
            
            logger.debug(f"截圖已儲存至設備: {save_path}")
            return True
            
        except Exception as e:
            logger.error(f"截圖失敗: {e}")
            return False
    
    def pull_file(self, device_path: str, local_path: str) -> bool:
        """
        從設備拉取檔案
        
        Args:
            device_path: 設備上的檔案路徑
            local_path: 本地儲存路徑
            
        Returns:
            是否成功
        """
        try:
            cmd = f'"{self.adb_path}" -s {self.device} pull {device_path} {local_path}'
            success, output = self._run_cmd(cmd, timeout=30)
            
            if success:
                logger.debug(f"檔案已拉取: {device_path} -> {local_path}")
                return True
            else:
                logger.error(f"拉取檔案失敗: {output}")
                return False
                
        except Exception as e:
            logger.error(f"拉取檔案錯誤: {e}")
            return False
    
    def __repr__(self) -> str:
        status = "已連接" if self.connected else "未連接"
        return f"ADBController({self.device}, {status})"
    
    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()


# 常用按鍵代碼
class KeyCode:
    """Android 按鍵代碼"""
    HOME = 3
    BACK = 4
    MENU = 82
    ENTER = 66
    DEL = 67
    VOLUME_UP = 24
    VOLUME_DOWN = 25
    POWER = 26


if __name__ == "__main__":
    # 測試程式碼
    from loguru import logger
    
    logger.info("測試 ADB 控制器...")
    
    with ADBController() as adb:
        if adb.is_connected():
            logger.success("✅ ADB 連接成功")
            
            # 取得螢幕解析度
            size = adb.get_screen_size()
            if size:
                logger.info(f"螢幕解析度: {size[0]}x{size[1]}")
            
            # 測試點擊（中心點）
            if size:
                center_x = size[0] // 2
                center_y = size[1] // 2
                logger.info(f"測試點擊中心點: ({center_x}, {center_y})")
                adb.tap(center_x, center_y)
        else:
            logger.error("❌ ADB 連接失敗")
            logger.info("請確認:")
            logger.info("1. 模擬器正在執行")
            logger.info("2. ADB 已正確安裝")
            logger.info("3. 埠號正確（預設 5555）")
