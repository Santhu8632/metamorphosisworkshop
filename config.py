import os
from datetime import timedelta

class Config:
    SECRET_KEY = 'metamorphosis-workshop-secure-key-2024-change-in-production'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///metamorphosis.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'static/videos/'
    IMAGE_UPLOAD_FOLDER = 'static/images/'
    ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'mov', 'avi', 'wmv', 'mkv'}
    ALLOWED_IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'webp'}
    MAX_CONTENT_LENGTH = 500 * 1024 * 1024  # 500MB max file size
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)