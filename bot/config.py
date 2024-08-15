import os

from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
FLASK_LOGIN_URL = os.getenv("FLASK_LOGIN_URL")
FLASK_BOOKING_TODAY_URL = os.getenv("FLASK_BOOKING_TODAY_URL")