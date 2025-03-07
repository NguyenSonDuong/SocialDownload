from dotenv import load_dotenv
import os

# Load biến môi trường ngay khi import file này
load_dotenv()

BASE_YOUTUBE_URL = os.getenv("BASE_YOUTUBE_URL")
API_KEY = os.getenv("API_KEY")
USER_AGENT = os.getenv("USER_AGENT")
REFERER = os.getenv("REFERER")
SOCIAL_CONFIG = os.getenv("SOCIAL_CONFIG")
KEY_SOCIAL = os.getenv("KEY_SOCIAL")