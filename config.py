# config.py
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env


class Config:
    SECRET_KEY = (
        os.environ.get("SECRET_KEY") or "a_default_secret_key"
    )  # Flask secret key for sessions, etc. (you can change this)
    TWITTER_API_KEY = os.environ.get("TWITTER_API_KEY")
    TWITTER_API_SECRET = os.environ.get("TWITTER_API_SECRET")
    TWITTER_BEARER_TOKEN = os.environ.get("TWITTER_BEARER_TOKEN")
    # Add other configuration variables as needed
