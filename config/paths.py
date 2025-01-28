from pathlib import Path

# Project root is one level up from config directory
PROJECT_ROOT = Path(__file__).parent.parent

# Data directories
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PARTIAL_DATA_DIR = DATA_DIR / "partial"
