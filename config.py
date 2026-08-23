from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
DB_NAME = "library.db"
DB_FILE = BASE_DIR / DB_NAME
DB_TABLENAME = "books"
HOST = "127.0.0.1"
PORT = 5000
DEBUG = True