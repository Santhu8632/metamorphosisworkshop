from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)

class Enquiry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    college = db.Column(db.String(200))
    program = db.Column(db.String(100))
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='New')  # New, Contacted, Completed
    notes = db.Column(db.Text)  # Admin notes about enquiry

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    filename = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    thumbnail = db.Column(db.String(200))  # Thumbnail image
    duration = db.Column(db.String(20))  # Video duration
    category = db.Column(db.String(50), default='Training')  # Training, Testimonial, Workshop
    views = db.Column(db.Integer, default=0)  # View counter
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    is_featured = db.Column(db.Boolean, default=False)

class Statistic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    value = db.Column(db.String(50), nullable=False)
    icon = db.Column(db.String(50))
    color = db.Column(db.String(20))
    display_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)