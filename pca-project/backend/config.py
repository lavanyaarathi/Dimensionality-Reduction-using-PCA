"""
Configuration module for PCA project.
Contains all application settings and configurations.
"""

import os

class Config:
    """Base configuration class with default settings"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Upload settings
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'temp_uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Allowed file extensions
    ALLOWED_EXTENSIONS = {
        'tabular': {'csv', 'xlsx', 'xls'},
        'image': {'jpg', 'jpeg', 'png'}
    }
    
    # Session settings
    SESSION_TIMEOUT = 3600  # 1 hour in seconds
    CLEANUP_INTERVAL = 300  # Run cleanup every 5 minutes
    
    # File validation constraints
    MIN_IMAGE_DIMENSION = 10
    MAX_IMAGE_DIMENSION = 4096
    MIN_TABULAR_ROWS = 2


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = False
    TESTING = True
    SESSION_TIMEOUT = 60  # Shorter timeout for tests


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    # Override with environment variables in production
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MAX_CONTENT_LENGTH = 32 * 1024 * 1024  # 32MB for production


# Configuration dictionary for easy selection
config_dict = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
