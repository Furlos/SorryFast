import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("BOT_TOKEN")
backend_link = "http://backend:8000"