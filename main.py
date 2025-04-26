from sqlalchemy import create_engine, Column, Integer, String, Date, Numeric, ForeignKey, Boolean, Text, Enum
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
    role = Column(Enum('admin', 'user', name='user_roles'), default='user')

class Meal(Base):
    __tablename__ = 'meals'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    time = Column(Enum('breakfast', 'lunch', 'dinner', name='meal_times'), nullable=False)
    price = Column(Numeric(10,2), nullable=False)
    inventory = Column(Integer, nullable=False)  # Can later link to Inventory table if you want

class Attendance(Base):
    __tablename__ = 'attendance'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    meal_id = Column(Integer, ForeignKey('meals.id', ondelete='CASCADE'))
    date = Column(Date, nullable=False)
    status = Column(Enum('present', 'absent', name='attendance_status'))

    user = relationship('User', backref='attendances')
    meal = relationship('Meal', backref='attendances')

Base.metadata.create_all(engine)