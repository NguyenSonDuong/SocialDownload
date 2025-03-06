from dotenv import load_dotenv
import os

# Load biến môi trường ngay khi import file này
load_dotenv()

BASE_YOUTUBE_URL = os.getenv("BASE_YOUTUBE_URL")
API_KEY = os.getenv("API_KEY")