"""
Configuration file for Research Paper Tracker Application
Handles environment variables and database connection settings
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file (for local development)
# In Azure, environment variables are set in App Settings
load_dotenv()

class Config:
    """Base configuration class"""
    
    # Secret key for session management and CSRF protection
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Azure SQL Database Configuration
    # In Azure, these are set as App Settings
    DB_SERVER = os.getenv('DB_SERVER') or os.getenv('SQLSERVER') or os.getenv('SQLAZURECONNSTR_SERVER')
    DB_NAME = os.getenv('DB_NAME') or os.getenv('SQLDATABASE') or os.getenv('SQLAZURECONNSTR_DATABASE')
    DB_USER = os.getenv('DB_USER') or os.getenv('SQLUSER') or os.getenv('SQLAZURECONNSTR_UID')
    DB_PASSWORD = os.getenv('DB_PASSWORD') or os.getenv('SQLPASSWORD') or os.getenv('SQLAZURECONNSTR_PASSWORD')
    
    # SQLAlchemy Connection String for Azure SQL with ODBC Driver 18
    # Format: mssql+pyodbc://<username>:<password>@<server>/<database>?driver=ODBC+Driver+18+for+SQL+Server&Encrypt=yes&TrustServerCertificate=yes
    SQLALCHEMY_DATABASE_URI = (
        f"mssql+pyodbc://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}/{DB_NAME}"
        "?driver=ODBC+Driver+18+for+SQL+Server"
        "&Encrypt=yes"
        "&TrustServerCertificate=yes"
        "&Connection Timeout=30"
        "&Timeout=30"
    )
    
    # SQLAlchemy settings
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False  # Set to True for SQL query debugging
    
    # Connection pool settings for Azure
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 5,
        'max_overflow': 10,
        'pool_timeout': 30,
        'pool_recycle': 3600,  # Recycle connections every hour
        'pool_pre_ping': True,  # Test connections before using
    }
    
    # Session configuration
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour in seconds


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SESSION_COOKIE_SECURE = True


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
