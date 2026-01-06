"""
配置管理模組

載入和管理系統配置檔案。
"""

import yaml
from pathlib import Path
from typing import Dict, Any


class Config:
    """配置管理類別"""
    
    def __init__(self, config_path: str = "configs/config.yaml"):
        """
        初始化配置管理器
        
        Args:
            config_path: 配置檔案路徑
        """
        self.config_path = Path(config_path)
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """載入配置檔案"""
        if not self.config_path.exists():
            raise FileNotFoundError(f"配置檔案不存在: {self.config_path}")
        
        with open(self.config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        return config
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        取得配置值（支援巢狀鍵，例如 'system.device'）
        
        Args:
            key: 配置鍵（使用 . 分隔巢狀鍵）
            default: 預設值
            
        Returns:
            配置值
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        
        return value
    
    def __getitem__(self, key: str) -> Any:
        """支援字典式存取"""
        return self.get(key)
    
    def __repr__(self) -> str:
        return f"Config({self.config_path})"


# 建立全域配置實例
_config = None


def get_config(config_path: str = "configs/config.yaml") -> Config:
    """
    取得全域配置實例
    
    Args:
        config_path: 配置檔案路徑
        
    Returns:
        Config 實例
    """
    global _config
    if _config is None:
        _config = Config(config_path)
    return _config
