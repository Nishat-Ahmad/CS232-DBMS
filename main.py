from sqlalchemy import create_engine, Column, Integer, String, Date, Numeric, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import os
from dotenv import load_dotenv

load_dotenv()

# Database setup using SQLAlchemy
DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

# Create engine
engine = create_engine(DATABASE_URL)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

# 🍽️ Users
class User(Base):
    __tablename__ = 'Users'

    user_id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    role = Column(String(50))
    password = Column(String(255))

# 📆 Weekly Menu (Template)
class WeeklyMenu(Base):
    __tablename__ = 'WeeklyMenu'

    menu_id = Column(Integer, primary_key=True)
    weekday = Column(String(10), nullable=False)
    meal_type = Column(String(50), nullable=False)
    items = Column(String)

# 🍛 Meal Instance (Actual meal on a real date)
class MealInstance(Base):
    __tablename__ = 'MealInstance'

    meal_id = Column(Integer, primary_key=True)
    menu_id = Column(Integer, ForeignKey('WeeklyMenu.menu_id'), nullable=False)
    date = Column(Date, nullable=False)

    # Relationship with WeeklyMenu
    weekly_menu = relationship("WeeklyMenu", backref="meal_instances")

# 🙋 Attendance (who showed up for which meal)
class Attendance(Base):
    __tablename__ = 'Attendance'

    attendance_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('Users.user_id'), nullable=False)
    meal_id = Column(Integer, ForeignKey('MealInstance.meal_id'), nullable=False)
    status = Column(String(50))  # 'present', 'absent', 'cancelled'

    # Relationships
    user = relationship("User", backref="attendances")
    meal_instance = relationship("MealInstance", backref="attendances")

# 💸 Billing (how much each user owes)
class Billing(Base):
    __tablename__ = 'Billing'

    bill_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('Users.user_id'), nullable=False)
    month = Column(String(20), nullable=False)
    total_meals = Column(Integer)
    total_breakfasts = Column(Integer)
    amount = Column(Numeric(10, 2))
    generated_on = Column(Date)
    is_paid = Column(Boolean, default=False)

    # Relationship with Users
    user = relationship("User", backref="billings")

# 📦 Inventory (optional but useful)
class Inventory(Base):
    __tablename__ = 'Inventory'

    item_id = Column(Integer, primary_key=True)
    name = Column(String(255))
    unit = Column(String(50))
    quantity = Column(Integer)
    updated_on = Column(Date)

# Create all tables in the database (if they don't already exist)
Base.metadata.create_all(engine)

