"""数据源模块 - 统一接口"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseSource(ABC):
    """数据源基类"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.name = config.get("name", "Unknown")
        self.enabled = config.get("enabled", True)
    
    @abstractmethod
    def fetch(self) -> List[Dict[str, Any]]:
        """获取数据，返回统一格式的列表"""
        pass
    
    def is_enabled(self) -> bool:
        return self.enabled
