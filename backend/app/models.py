from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Teacher(db.Model):
    __tablename__ = 'teacher'
    id            = db.Column(db.Integer, primary_key=True)
    full_name     = db.Column(db.String(255), nullable=False)
    experience    = db.Column(db.Integer, nullable=False)
    specialty     = db.Column(db.String(255), nullable=False)
    department    = db.Column(db.String(255), nullable=False)

    # связь «1 → N» на Course
    courses = db.relationship(
        'Course',
        backref='teacher',
        cascade='all, delete-orphan',
        lazy=True
    )

    def __str__(self):
        return self.full_name

class Course(db.Model):
    __tablename__ = 'course'
    id            = db.Column(db.Integer, primary_key=True)
    title         = db.Column(db.String(255), nullable=False)
    teacher_id    = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)
    student_limit = db.Column(db.Integer, nullable=False)
    requests = db.relationship(
        'Request',
        backref='course',
        cascade='all, delete-orphan',
        lazy=True
    )

    def __str__(self):
        return self.title

class Student(db.Model):
    __tablename__ = 'student'
    id         = db.Column(db.Integer, primary_key=True)
    full_name  = db.Column(db.String(255), nullable=False)
    email      = db.Column(db.String(255), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __str__(self):
        return self.full_name

class Request(db.Model):
    __tablename__ = 'request'
    id          = db.Column(db.Integer, primary_key=True)
    course_id   = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    student_id  = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    description = db.Column(db.Text)
    status      = db.Column(
        db.String(50),
        default='pending',
        nullable=False,
        server_default='pending'
    )
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

    student = db.relationship(
        'Student',
        backref=db.backref('requests', cascade='all, delete-orphan', lazy=True),
        lazy=True
    )

    def __str__(self):
        return self.id