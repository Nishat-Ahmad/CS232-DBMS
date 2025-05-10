from flask import Blueprint, render_template, request, redirect, url_for, flash, g
from database.models import Session, Billing
from utils.auth_decorators import login_required, admin_required

billing_bp = Blueprint('billing_bp', __name__, url_prefix='/billing')

@billing_bp.route('/my')
@login_required
def my_billing():
    db = Session()
    bills = db.query(Billing).filter_by(student_id=g.user.id).all()
    db.close()
    return render_template('my_billing.html', bills=bills)

@billing_bp.route('/pay/<int:bill_id>', methods=['POST'])
@login_required
def pay_bill(bill_id):
    db = Session()
    bill = db.query(Billing).filter_by(id=bill_id, student_id=g.user.id).first()
    if bill and bill.status == 'unpaid':
        bill.status = 'pending'
        db.commit()
        flash('Payment request submitted. Awaiting admin approval.', 'info')
    else:
        flash('Invalid bill or already paid/pending.', 'error')
    db.close()
    return redirect(url_for('billing_bp.my_billing'))

@billing_bp.route('/pending')
@login_required
@admin_required
def pending_bills():
    # Only allow admin to view
    if not g.user or g.user.role != 'admin':
        flash('Access denied.', 'error')
        return redirect(url_for('index'))
    db = Session()
    bills = db.query(Billing).filter_by(status='pending').all()
    db.close()
    return render_template('pending_bills.html', bills=bills)

@billing_bp.route('/approve/<int:bill_id>', methods=['POST'])
@login_required
@admin_required
def approve_bill(bill_id):
    # Only allow admin to approve
    if not g.user or g.user.role != 'admin':
        flash('Access denied.', 'error')
        return redirect(url_for('index'))
    db = Session()
    bill = db.query(Billing).filter_by(id=bill_id).first()
    if bill and bill.status == 'pending':
        bill.status = 'paid'
        db.commit()
        flash('Bill approved and marked as paid.', 'success')
    else:
        flash('Invalid bill or already approved.', 'error')
    db.close()
    return redirect(url_for('billing_bp.pending_bills'))

@billing_bp.route('/all')
@login_required
@admin_required
def all_bills():
    db = Session()
    from sqlalchemy.orm import joinedload
    bills = db.query(Billing).options(joinedload(Billing.student)).all()
    db.close()
    return render_template('all_bills.html', bills=bills)