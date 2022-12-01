import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

TG_TOKEN = os.getenv('TG_TOKEN')

BASE_DIR = Path(__file__).resolve().parent.parent

ADMIN_ID = os.getenv('ADMIN_ID')

SQLITE_CONNECT = 'sqlite:///' + str(BASE_DIR) + '/db.sqlite'

PG_CONNECT = os.getenv('DB_CONNECT')
