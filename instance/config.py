"""This module contains the various app configurations"""
import os

class Config():
    """Base config (other configs inherit from this base)"""
    DEBUG=False
    SECRET=os.getenv('SECRET')

class DevelopmentConfig(Config):
    """Development Config"""
    DEBUG=True

class TestingConfig(Config):
    """Testing Config"""
    TESTING=True
    DEBUG=True

class ProductionConfig(Config):
    """Production Config"""
    DEBUG=False
    TESTIN=False

app_configuration = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}