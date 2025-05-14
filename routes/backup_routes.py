import os
import json
import configparser
from flask import Blueprint, render_template, redirect, url_for, flash
from database.models import Session, Base
from sqlalchemy.inspection import inspect
import firebase_admin
from firebase_admin import credentials, db as firebase_db

backup_bp = Blueprint('backup_bp', __name__, url_prefix='/backup')

FIREBASE_CREDENTIALS_PATH = 'cs233-project-448b1-firebase-adminsdk-fbsvc-b0509b8418.json'

# Read the databaseURL from the .json key file
def get_firebase_db_url(json_path):
    with open(json_path, 'r') as f:
        key_data = json.load(f)
    project_id = key_data.get('project_id')
    return f'https://{project_id}-default-rtdb.asia-southeast1.firebasedatabase.app/'

FIREBASE_DATABASE_URL = get_firebase_db_url(FIREBASE_CREDENTIALS_PATH)
BACKUP_ROOT_NODE = 'postgres_backup'

cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {'databaseURL': FIREBASE_DATABASE_URL})

firebase_ref = firebase_db.reference(BACKUP_ROOT_NODE)

def serialize_row(row):
    result = {}
    for c in inspect(row).mapper.column_attrs:
        value = getattr(row, c.key)
        if hasattr(value, 'isoformat'):
            result[c.key] = value.isoformat()
        else:
            result[c.key] = str(value) if value is not None and not isinstance(value, (int, float, str, bool)) else value
    return result

def backup_all_tables():
    session = Session()
    all_data = {}
    for cls in Base.__subclasses__():
        if hasattr(cls, '__tablename__'):
            table_name = cls.__tablename__
            rows = session.query(cls).all()
            all_data[table_name] = [serialize_row(row) for row in rows]
    session.close()
    firebase_ref.set(all_data)
    return True

@backup_bp.route('/to_firebase', methods=['POST'])
def backup_to_firebase():
    try:
        backup_all_tables()
        flash('Database backup to Firebase successful!', 'success')
        return render_template('backup_status.html', status='success')
    except Exception as e:
        flash(f'Backup failed: {e}', 'danger')
        return render_template('backup_status.html', status='error', error=str(e))
