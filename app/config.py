"""应用配置：全部从环境变量读取，禁止硬编码敏感信息。"""
import os
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()


class Config:
    """基础配置类。"""

    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = os.getenv("FLASK_DEBUG", "0") == "1"
    # 避免 MySQL 空闲断连导致 500
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 280,
    }

    DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
    DB_PORT = int(os.getenv("DB_PORT", "3306"))
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME", "office_backend")

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
    )

    JWT_SECRET = os.getenv("JWT_SECRET", "jwt-dev-secret")
    JWT_EXPIRE_SECONDS = int(os.getenv("JWT_EXPIRE_SECONDS", "7200"))
    JWT_EXPIRE_DELTA = timedelta(seconds=JWT_EXPIRE_SECONDS)

    LOG_DIR = os.getenv("LOG_DIR", "logs")
    LOG_FILE = os.getenv("LOG_FILE", "api.log")
