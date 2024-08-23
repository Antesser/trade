from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
SECRET_KEY = os.environ.get("SECRET")
MANAGER_SECRET = os.environ.get("MANAGER_SECRET")
SMTP_USER = os.environ.get("SMTP_USER")
SMTP_RECIPIENT = os.environ.get("SMTP_RECIPIENT")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")