from database.models import Billing, Attendance, Meal, Notification
from sqlalchemy import func

def calculate_student_monthly_bill(session, student_id, month, year):
    total = session.query(func.sum(Meal.price)) \
        .join(Attendance, Attendance.meal_id == Meal.id) \
        .filter(Attendance.user_id == student_id) \
        .filter(Attendance.status == 'present') \
        .filter(func.extract('month', Attendance.date) == month) \
        .filter(func.extract('year', Attendance.date) == year) \
        .scalar()
    return total or 0

def update_billing_and_notify(session, student_id, date, meal_id, threshold=10000):
    month = date.strftime('%B')
    year = date.year
    meal_price = session.query(Meal.price).filter(Meal.id == meal_id).scalar() or 0
    bill = session.query(Billing).filter_by(student_id=student_id, month=month, year=year).first()
    if bill:
        bill.amount += meal_price
    else:
        bill = Billing(student_id=student_id, month=month, year=year, amount=meal_price)
        session.add(bill)
    session.flush()  # Ensure bill.amount is updated
    if bill.amount > threshold:
        msg = f'Your monthly bill has exceeded {threshold}.'
        notification = Notification(message=msg, target_role='student', admin_id=None)
        session.add(notification)
    session.commit()
