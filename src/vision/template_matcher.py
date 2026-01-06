"""
模板匹配模組

使用 OpenCV 進行模板匹配，識別 UI 元素。
"""

import cv2
import numpy as np
from typing import Optional, Tuple, List
from pathlib import Path
from loguru import logger


class TemplateMatcher:
    """模板匹配類別"""
    
    def __init__(self, threshold: float = 0.8):
        """
        初始化模板匹配器
        
        Args:
            threshold: 匹配信心閾值（0-1）
        """
        self.threshold = threshold
        self.templates = {}
        
        logger.info(f"模板匹配器初始化完成 (threshold={threshold})")
    
    def load_template(self, name: str, template_path: str) -> bool:
        """
        載入模板圖片
        
        Args:
            name: 模板名稱
            template_path: 模板圖片路徑
            
        Returns:
            是否成功載入
        """
        try:
            template = cv2.imread(template_path)
            
            if template is None:
                logger.error(f"無法載入模板: {template_path}")
                return False
            
            # 轉換為灰階
            template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
            
            self.templates[name] = {
                'image': template,
                'gray': template_gray,
                'shape': template.shape[:2]  # (height, width)
            }
            
            logger.success(f"✅ 載入模板: {name} ({template.shape[1]}x{template.shape[0]})")
            return True
            
        except Exception as e:
            logger.error(f"載入模板失敗: {e}")
            return False
    
    def load_templates_from_dir(self, directory: str) -> int:
        """
        從目錄載入所有模板
        
        Args:
            directory: 模板目錄路徑
            
        Returns:
            成功載入的模板數量
        """
        dir_path = Path(directory)
        
        if not dir_path.exists():
            logger.error(f"目錄不存在: {directory}")
            return 0
        
        count = 0
        for file_path in dir_path.glob("*.png"):
            name = file_path.stem
            if self.load_template(name, str(file_path)):
                count += 1
        
        logger.info(f"從 {directory} 載入了 {count} 個模板")
        return count
    
    def match(
        self,
        screen: np.ndarray,
        template_name: str,
        method: int = cv2.TM_CCOEFF_NORMED
    ) -> Optional[Tuple[int, int, float]]:
        """
        在螢幕上尋找模板
        
        Args:
            screen: 螢幕截圖（BGR 格式）
            template_name: 模板名稱
            method: 匹配方法
            
        Returns:
            (x, y, confidence) 或 None
        """
        if template_name not in self.templates:
            logger.error(f"模板不存在: {template_name}")
            return None
        
        try:
            template_data = self.templates[template_name]
            template_gray = template_data['gray']
            
            # 轉換螢幕截圖為灰階
            screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
            
            # 模板匹配
            result = cv2.matchTemplate(screen_gray, template_gray, method)
            
            # 取得最佳匹配位置
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
            # 根據方法選擇位置
            if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
                match_loc = min_loc
                confidence = 1 - min_val
            else:
                match_loc = max_loc
                confidence = max_val
            
            # 檢查信心度
            if confidence >= self.threshold:
                # 計算中心點
                h, w = template_data['shape']
                center_x = match_loc[0] + w // 2
                center_y = match_loc[1] + h // 2
                
                logger.debug(
                    f"✅ 找到模板 '{template_name}' "
                    f"at ({center_x}, {center_y}), "
                    f"confidence={confidence:.2f}"
                )
                
                return (center_x, center_y, confidence)
            else:
                logger.debug(
                    f"未找到模板 '{template_name}' "
                    f"(confidence={confidence:.2f} < {self.threshold})"
                )
                return None
                
        except Exception as e:
            logger.error(f"模板匹配失敗: {e}")
            return None
    
    def match_all(
        self,
        screen: np.ndarray,
        template_name: str,
        method: int = cv2.TM_CCOEFF_NORMED
    ) -> List[Tuple[int, int, float]]:
        """
        在螢幕上尋找所有匹配的模板位置
        
        Args:
            screen: 螢幕截圖（BGR 格式）
            template_name: 模板名稱
            method: 匹配方法
            
        Returns:
            [(x, y, confidence), ...] 列表
        """
        if template_name not in self.templates:
            logger.error(f"模板不存在: {template_name}")
            return []
        
        try:
            template_data = self.templates[template_name]
            template_gray = template_data['gray']
            h, w = template_data['shape']
            
            # 轉換螢幕截圖為灰階
            screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
            
            # 模板匹配
            result = cv2.matchTemplate(screen_gray, template_gray, method)
            
            # 找出所有超過閾值的位置
            locations = np.where(result >= self.threshold)
            
            matches = []
            for pt in zip(*locations[::-1]):
                center_x = pt[0] + w // 2
                center_y = pt[1] + h // 2
                confidence = result[pt[1], pt[0]]
                matches.append((center_x, center_y, float(confidence)))
            
            logger.debug(f"找到 {len(matches)} 個匹配的 '{template_name}'")
            
            return matches
            
        except Exception as e:
            logger.error(f"批量模板匹配失敗: {e}")
            return []
    
    def visualize_match(
        self,
        screen: np.ndarray,
        template_name: str,
        output_path: Optional[str] = None
    ) -> Optional[np.ndarray]:
        """
        視覺化匹配結果
        
        Args:
            screen: 螢幕截圖
            template_name: 模板名稱
            output_path: 輸出圖片路徑（None 表示不儲存）
            
        Returns:
            標記後的圖片或 None
        """
        match = self.match(screen, template_name)
        
        if match is None:
            logger.warning(f"未找到匹配: {template_name}")
            return None
        
        x, y, confidence = match
        template_data = self.templates[template_name]
        h, w = template_data['shape']
        
        # 複製圖片
        result_img = screen.copy()
        
        # 繪製矩形
        top_left = (x - w // 2, y - h // 2)
        bottom_right = (x + w // 2, y + h // 2)
        cv2.rectangle(result_img, top_left, bottom_right, (0, 255, 0), 2)
        
        # 繪製中心點
        cv2.circle(result_img, (x, y), 5, (0, 0, 255), -1)
        
        # 添加文字
        text = f"{template_name}: {confidence:.2f}"
        cv2.putText(
            result_img,
            text,
            (x + 10, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )
        
        # 儲存圖片
        if output_path:
            cv2.imwrite(output_path, result_img)
            logger.info(f"視覺化結果已儲存: {output_path}")
        
        return result_img
    
    def get_template_names(self) -> List[str]:
        """取得所有已載入的模板名稱"""
        return list(self.templates.keys())
    
    def __repr__(self) -> str:
        return f"TemplateMatcher(templates={len(self.templates)}, threshold={self.threshold})"


if __name__ == "__main__":
    # 測試程式碼
    logger.info("測試模板匹配模組...")
    
    matcher = TemplateMatcher(threshold=0.8)
    
    # 示範如何使用
    logger.info("使用方式:")
    logger.info("1. matcher.load_template('button_start', 'templates/start_button.png')")
    logger.info("2. match = matcher.match(screen, 'button_start')")
    logger.info("3. if match: x, y, confidence = match")
