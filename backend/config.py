import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # PostgreSQL
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    # Gemini
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    # MongoDB
    MONGO_URI = os.getenv("MONGO_URI")