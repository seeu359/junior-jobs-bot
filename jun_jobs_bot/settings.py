import os
from pathlib import Path

TG_TOKEN = os.environ['TG_TOKEN']
BASE_DIR = Path(__file__).resolve().parent.parent
ADMIN_ID = os.environ['ADMIN_ID']
DB_CONNECT = os.environ['DB_CONNECT']
