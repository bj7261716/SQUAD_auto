"""
螢幕擷取模組

使用 MSS 進行高效能螢幕擷取。
"""

import cv2
import mss
import numpy as np
from typing import Tuple, Optional, Dict
import time


class ScreenCapture:
    """螢幕擷取類別"""
    
    def __init__(
        self,
        region: Optional[Dict[str, int]] = None,
        resize: Optional[Tuple[int, int]] = None,
        fps_limit: int = 60
    ):
        """
        初始化螢幕擷取器
        
        Args:
            region: 擷取區域 {"left": x, "top": y, "width": w, "height": h}
            resize: 調整大小 (width, height)，None 表示不調整
            fps_limit: FPS 限制
        """
        self.sct = mss.mss()
        self.region = region or self.sct.monitors[1]  # 預設使用主螢幕
        self.resize = resize
        self.fps_limit = fps_limit
        
        # FPS 控制
        self.frame_time = 1.0 / fps_limit
        self.last_capture_time = 0
        
        # 統計資訊
        self.frame_count = 0
        self.fps = 0
        self.fps_start_time = time.time()
        
        print(f"✅ 螢幕擷取器初始化完成")
        print(f"   區域: {self.region}")
        print(f"   調整大小: {self.resize}")
        print(f"   FPS 限制: {self.fps_limit}")
    
    def capture(self) -> np.ndarray:
        """
        擷取螢幕並返回 numpy array
        
        Returns:
            BGR 格式的圖像 (numpy array)
        """
        # FPS 限制
        current_time = time.time()
        time_since_last_capture = current_time - self.last_capture_time
        if time_since_last_capture < self.frame_time:
            time.sleep(self.frame_time - time_since_last_capture)
        
        # 擷取螢幕
        img = self.sct.grab(self.region)
        
        # 轉換為 numpy array (BGRA -> BGR)
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
        
        # 調整大小
        if self.resize:
            frame = cv2.resize(frame, self.resize)
        
        # 更新統計
        self.last_capture_time = time.time()
        self.frame_count += 1
        
        # 計算 FPS
        if current_time - self.fps_start_time > 1.0:
            self.fps = self.frame_count
            self.frame_count = 0
            self.fps_start_time = current_time
        
        return frame
    
    def capture_rgb(self) -> np.ndarray:
        """
        擷取螢幕並返回 RGB 格式
        
        Returns:
            RGB 格式的圖像 (numpy array)
        """
        frame = self.capture()
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    def get_fps(self) -> int:
        """取得當前 FPS"""
        return self.fps
    
    def close(self):
        """關閉擷取器"""
        self.sct.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
    
    def __repr__(self) -> str:
        return f"ScreenCapture(region={self.region}, resize={self.resize}, fps={self.fps_limit})"


if __name__ == "__main__":
    # 測試程式碼
    print("測試螢幕擷取模組...")
    
    # 建立擷取器
    capturer = ScreenCapture(
        region={"left": 100, "top": 100, "width": 1280, "height": 720},
        resize=(640, 360),
        fps_limit=30
    )
    
    print("按 'q' 鍵退出")
    
    try:
        while True:
            frame = capturer.capture()
            
            # 顯示 FPS
            cv2.putText(
                frame,
                f"FPS: {capturer.get_fps()}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )
            
            cv2.imshow("Screen Capture", frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    finally:
        capturer.close()
        cv2.destroyAllWindows()
    
    print("✅ 測試完成")
