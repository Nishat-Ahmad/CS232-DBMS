from sqlalchemy import create_engine, Column, Integer, String, Date, Numeric, ForeignKey, Enum, Text, Boolean, func, select, text, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
import os
import configparser

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), '..', 'db_config.ini'))
db_cfg = config['postgresql']
DATABASE_URL = f"postgresql://{db_cfg['user']}:{db_cfg['password']}@{db_cfg['host']}:{db_cfg['port']}/{db_cfg['database']}"
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
    
    admin_id = Column(Integer, ForeignKey('admins.id', ondelete='SET NULL'), nullable=True)  # new field
    admin = relationship('Admin', backref='notifications')

class NotificationRead(Base):
    __tablename__ = 'notification_reads'
    id = Column(Integer, primary_key=True)
    notification_id = Column(Integer, ForeignKey('notifications.id', ondelete='CASCADE'))
    student_id = Column(Integer, ForeignKey('students.id', ondelete='CASCADE'))

    notification = relationship('Notification', backref='reads')
    student = relationship('Student', backref='read_notifications')

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
    status = Column(Enum('paid', 'unpaid', 'pending', name='billing_status'), default='unpaid', nullable=False)

    student = relationship('Student', backref='bills')

class DeletedMeal(Base):
    __tablename__ = 'deleted_meals'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    time = Column(Enum('breakfast', 'lunch', 'dinner', name='meal_times'), nullable=False)
    price = Column(Numeric(10,2), nullable=False)
    inventory = Column(Integer, nullable=False)
    deleted_at = Column(Date, default=func.now())

class DeletedMenu(Base):
    __tablename__ = 'deleted_menus'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    start_date = Column(Date, nullable=True)
    is_template = Column(Boolean, default=False)
    deleted_at = Column(Date, default=func.now())

class DeletedUser(Base):
    __tablename__ = 'deleted_users'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(Enum('admin', 'student', name='user_roles'), nullable=False)
    type = Column(String(50))
    deleted_at = Column(Date, default=func.now())

class DeletedAttendance(Base):
    __tablename__ = 'deleted_attendance'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    meal_id = Column(Integer)
    date = Column(Date, nullable=False)
    status = Column(Enum('present', 'absent', name='attendance_status'))
    deleted_at = Column(Date, default=func.now())

class StudentMonthlyBilling(Base):
    __table__ = Table(
        'student_monthly_billing', Base.metadata,
        Column('user_id', Integer, primary_key=True),
        Column('user_name', String),
        Column('month', Integer),
        Column('year', Integer),
        Column('total_amount', Numeric),
        autoload_with=engine
    )

# Create triggers, functions, and procedures for archiving on delete
with engine.connect() as conn:
    conn.execute(text('''
    CREATE OR REPLACE VIEW student_monthly_billing AS
    SELECT
        u.id AS user_id,
        u.name AS user_name,
        EXTRACT(MONTH FROM a.date) AS month,
        EXTRACT(YEAR FROM a.date) AS year,
        SUM(m.price) AS total_amount
    FROM attendance a
    JOIN users u ON a.user_id = u.id
    JOIN meals m ON a.meal_id = m.id
    WHERE a.status = 'present'
    GROUP BY u.id, u.name, EXTRACT(YEAR FROM a.date), EXTRACT(MONTH FROM a.date)
    ORDER BY year DESC, month DESC;

    CREATE OR REPLACE FUNCTION archive_meal_before_delete() RETURNS TRIGGER AS $$
    BEGIN
        INSERT INTO deleted_meals SELECT OLD.*, now();
        RETURN OLD;
    END;
    $$ LANGUAGE plpgsql;
    DROP TRIGGER IF EXISTS trigger_archive_meal ON meals;
    CREATE TRIGGER trigger_archive_meal BEFORE DELETE ON meals FOR EACH ROW EXECUTE FUNCTION archive_meal_before_delete();

    CREATE OR REPLACE FUNCTION archive_menu_before_delete() RETURNS TRIGGER AS $$
    BEGIN
        INSERT INTO deleted_menus SELECT OLD.*, now();
        RETURN OLD;
    END;
    $$ LANGUAGE plpgsql;
    DROP TRIGGER IF EXISTS trigger_archive_menu ON menus;
    CREATE TRIGGER trigger_archive_menu BEFORE DELETE ON menus FOR EACH ROW EXECUTE FUNCTION archive_menu_before_delete();

    CREATE OR REPLACE PROCEDURE archive_user_proc() LANGUAGE plpgsql AS $$
    BEGIN
        INSERT INTO deleted_users SELECT *, now() FROM users WHERE id = (SELECT id FROM users ORDER BY id DESC LIMIT 1);
    END;
    $$;
    CREATE OR REPLACE FUNCTION archive_user_before_delete() RETURNS TRIGGER AS $$
    BEGIN
        CALL archive_user_proc();
        RETURN OLD;
    END;
    $$ LANGUAGE plpgsql;
    DROP TRIGGER IF EXISTS trigger_archive_user ON users;
    CREATE TRIGGER trigger_archive_user BEFORE DELETE ON users FOR EACH ROW EXECUTE FUNCTION archive_user_before_delete();

    CREATE OR REPLACE FUNCTION archive_attendance_before_delete() RETURNS TRIGGER AS $$
    BEGIN
        INSERT INTO deleted_attendance SELECT OLD.*, now();
        RETURN OLD;
    END;
    $$ LANGUAGE plpgsql;
    DROP TRIGGER IF EXISTS trigger_archive_attendance ON attendance;
    CREATE TRIGGER trigger_archive_attendance BEFORE DELETE ON attendance FOR EACH ROW EXECUTE FUNCTION archive_attendance_before_delete();
    
    -- DO $$
    -- BEGIN
    --     IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'billing_status') THEN
    --         CREATE TYPE billing_status AS ENUM ('paid', 'unpaid', 'pending');
    --     END IF;
    -- END$$;

    -- ALTER TABLE billing ADD COLUMN status billing_status DEFAULT 'unpaid' NOT NULL;
    '''))

Base.metadata.create_all(engine)
