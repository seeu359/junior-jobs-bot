import os
from pathlib import Path

TG_TOKEN = os.environ['TG_TOKEN']
DATABASE_NAME = 'database.sqlite'
BASE_DIR = Path(__file__).resolve().parent.parent
PATH_TO_BASE = os.path.join(BASE_DIR, DATABASE_NAME)
ADMIN_ID = os.environ['ADMIN_ID']
