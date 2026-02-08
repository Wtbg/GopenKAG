import yaml
import os
from pathlib import Path

def load_config(config_path: str = "config/config.yaml") -> dict:
    """Load configuration from a YAML file."""
    # Find the project root
    # Assuming this is called from somewhere within the project, e.g. src/extract/extractor.py
    # We try to find config/config.yaml relative to current working directory or absolute path
    
    # Try current directory first
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
            
    # Try looking 1 or 2 levels up
    p = Path(os.getcwd())
    for i in range(3):
        curr_path = p / config_path
        if curr_path.exists():
             with open(curr_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        p = p.parent
        
    # Fallback to absolute path relative to this file's location in src/utils.py -> ../../config/config.yaml
    base_dir = Path(__file__).parent.parent
    abs_config_path = base_dir / "config" / "config.yaml"
    if abs_config_path.exists():
        with open(abs_config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
            
    raise FileNotFoundError(f"Config file not found at {config_path} or parent directories.")

def get_project_root() -> Path:
    return Path(__file__).parent.parent
