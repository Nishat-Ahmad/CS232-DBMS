from sqlalchemy import create_engine, Column, Integer, String, Date, Numeric, ForeignKey, Enum, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(Enum('admin', 'student', name='user_roles'), nullable=False)

    type = Column(String(50))
    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': type
    }

class Student(User):
    __tablename__ = 'students'
    id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), primary_key=True)
    roll_number = Column(String(100), unique=True)
    __mapper_args__ = {
        'polymorphic_identity': 'student',
    }

class Admin(User):
    __tablename__ = 'admins'
    id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), primary_key=True)
    admin_level = Column(String(50))
    __mapper_args__ = {
        'polymorphic_identity': 'admin',
    }

class Meal(Base):
    __tablename__ = 'meals'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    time = Column(Enum('breakfast', 'lunch', 'dinner', name='meal_times'), nullable=False)
    price = Column(Numeric(10,2), nullable=False)
    inventory = Column(Integer, nullable=False)

class Attendance(Base):
    __tablename__ = 'attendance'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    meal_id = Column(Integer, ForeignKey('meals.id', ondelete='CASCADE'))
    date = Column(Date, nullable=False)
    status = Column(Enum('present', 'absent', name='attendance_status'))

    user = relationship('User', backref='attendances')
    meal = relationship('Meal', backref='attendances')

class Complaint(Base):
    __tablename__ = 'complaints'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id', ondelete='CASCADE'))
    message = Column(Text, nullable=False)
    status = Column(Enum('pending', 'resolved', name='complaint_status'), default='pending')

    student = relationship('Student', backref='complaints')

class Notification(Base):
    __tablename__ = 'notifications'
    id = Column(Integer, primary_key=True)
    message = Column(Text, nullable=False)
    target_role = Column(Enum('admin', 'student', 'all', name='notification_targets'), nullable=False)
class Menu(Base):
    __tablename__ = 'menus'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)  # e.g., "Week 18 Plan" or "Current Week"
    start_date = Column(Date, nullable=True)  # optional for templates
    is_template = Column(Boolean, default=False)

    days = relationship("MenuDay", back_populates="menu", cascade="all, delete-orphan")

class MenuDay(Base):
    __tablename__ = 'menu_days'

    id = Column(Integer, primary_key=True)
    menu_id = Column(Integer, ForeignKey('menus.id', ondelete="CASCADE"))
    day_of_week = Column(Enum('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', name='weekdays'))

    breakfast_id = Column(Integer, ForeignKey('meals.id'))
    lunch_id = Column(Integer, ForeignKey('meals.id'))
    dinner_id = Column(Integer, ForeignKey('meals.id'))

    menu = relationship("Menu", back_populates="days")
    breakfast = relationship("Meal", foreign_keys=[breakfast_id])
    lunch = relationship("Meal", foreign_keys=[lunch_id])
    dinner = relationship("Meal", foreign_keys=[dinner_id])




class Billing(Base):
    __tablename__ = 'billing'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id', ondelete='CASCADE'))
    month = Column(String(20), nullable=False)
    year = Column(Integer, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)

    student = relationship('Student', backref='bills')

Base.metadata.create_all(engine)
