import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Date, Text
from datetime import datetime
db = SQLAlchemy()
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    phone = db.Column(db.String(15), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


class Home_content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    content = db.Column(db.String(150), nullable=False, unique=True)

    def __repr__(self):
        return f'<User {self.username}>'


class Class_time_table(db.Model):
    __tablename__ = 'class_time_table'
    id = db.Column(Integer, primary_key=True)
    class_time = Column(Text(10))
    class_title = Column(String(50))
    class_content = Column(String(256))
    class_teacher = Column(String(16))
    class_create_time = Column(DateTime, default=datetime.now())

    def __repr__(self):
        return f'<Class_time_table {self.class_teacher, self.class_content}>'
