"""Central configuration for the complaint management system."""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_DIR = BASE_DIR / "datasets"
MODEL_DIR = BASE_DIR / "ml_models" / "artifacts"
DB_PATH = BASE_DIR / "database" / "complaint_system.db"

DATA_FILE = DATASET_DIR / "datas.xlsx"
QUERY_FILE = DATASET_DIR / "queries.xlsx"

SIMILARITY_THRESHOLD = 0.45
URGENT_KEYWORDS = {"urgent", "deadline", "tomorrow", "emergency", "immediately"}
RETRAIN_RECORD_THRESHOLD = 100

MODEL_DIR.mkdir(parents=True, exist_ok=True)
