import os
from pathlib import Path

TG_TOKEN = os.environ['TG_TOKEN']
BASE_DIR = Path(__file__).resolve().parent.parent
ADMIN_ID = os.environ['ADMIN_ID']
DB_USERNAME = os.environ['DB_USERNAME']
DB_PASSWORD = os.environ['DB_PASSWORD']
HOST = os.environ['HOST']
PORT = os.environ['PORT']
DATABASE = os.environ['DATABASE']
CONNECT = 'postgresql+psycopg2://%s:%s@%s:%s/%s' % (DB_USERNAME, DB_PASSWORD,
                                                    HOST, PORT,
                                                    DATABASE)
