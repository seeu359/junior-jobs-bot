import os
from pathlib import Path

TG_TOKEN = os.getenv('TG_TOKEN')
BASE_DIR = Path(__file__).resolve().parent.parent
ADMIN_ID = os.getenv('ADMIN_ID')
DB_CONNECT = os.getenv('DB_CONNECT')
