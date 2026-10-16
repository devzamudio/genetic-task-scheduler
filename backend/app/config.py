"""config.py: Configuraciones de la aplicación, MongoDB y Celery."""
import os

class Config:
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongodb:27017/genetic_scheduler")
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
    CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0")
    FLASK_ENV = os.getenv("FLASK_ENV", "production")