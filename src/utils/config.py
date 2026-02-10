"""
Configuration management for Douyin Viral Analyzer
"""
import yaml
from pathlib import Path
from typing import Dict, Any

class Config:
    """Configuration loader and manager"""
    
    def __init__(self, config_path: str = "config/config.yaml"):
        self.config_path = Path(config_path)
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        if not self.config_path.exists():
            return self._default_config()
        
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def _default_config(self) -> Dict[str, Any]:
        """Return default configuration"""
        return {
            'scraper': {
                'source': 'mock',
                'batch_size': 50,
                'interval': 3600
            },
            'analyzer': {
                'enable_ai': False,
                'dimensions': ['duration', 'tags', 'music', 'category']
            },
            'reporter': {
                'formats': ['text', 'charts'],
                'charts': ['duration_dist', 'tag_cloud', 'music_trend', 'category_pie']
            },
            'database': {
                'path': 'viral_videos.db'
            }
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by dot notation key"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        
        return value if value is not None else default
    
    def save(self):
        """Save current configuration to file"""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.config_path, 'w', encoding='utf-8') as f:
            yaml.dump(self.config, f, allow_unicode=True, default_flow_style=False)
