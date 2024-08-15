from flask import Blueprint, jsonify, request
from sqlalchemy.orm import sessionmaker
from models import Constraint
from utils.db import get_engine, get_session

constraints_bp = Blueprint('constraints', __name__)

# Set up the database session
engine = get_engine()
DBSession = sessionmaker(bind=engine)
session = get_session()

@constraints_bp.route('/constraints', methods=['GET'])
def get_constraints():
    constraints = session.query(Constraint).all()
    return jsonify([{
        'id': c.id,
        'exact_days_off_per_month': c.exact_days_off_per_month,
        'min_days_off': c.min_days_off,
        'max_days_off': c.max_days_off,
        'min_days_off_in_period': c.min_days_off_in_period,
        'max_days_off_in_period': c.max_days_off_in_period,
        'min_morning_shifts': c.min_morning_shifts,
        'max_morning_shifts': c.max_morning_shifts,
        'min_morning_shifts_in_period': c.min_morning_shifts_in_period,
        'max_morning_shifts_in_period': c.max_morning_shifts_in_period,
        'min_afternoon_shifts': c.min_afternoon_shifts,
        'max_afternoon_shifts': c.max_afternoon_shifts,
        'min_afternoon_shifts_in_period': c.min_afternoon_shifts_in_period,
        'max_afternoon_shifts_in_period': c.max_afternoon_shifts_in_period,
        'min_night_shifts': c.min_night_shifts,
        'max_night_shifts': c.max_night_shifts,
        'min_night_shifts_in_period': c.min_night_shifts_in_period,
        'max_night_shifts_in_period': c.max_night_shifts_in_period
    } for c in constraints])

@constraints_bp.route('/constraints/<int:id>', methods=['GET'])
def get_constraint(id):
    constraint = session.query(Constraint).get(id)
    if not constraint:
        return jsonify({'error': 'Constraint not found'}), 404

    return jsonify({
        'id': constraint.id,
        'exact_days_off_per_month': constraint.exact_days_off_per_month,
        'min_days_off': constraint.min_days_off,
        'max_days_off': constraint.max_days_off,
        'min_days_off_in_period': constraint.min_days_off_in_period,
        'max_days_off_in_period': constraint.max_days_off_in_period,
        'min_morning_shifts': constraint.min_morning_shifts,
        'max_morning_shifts': constraint.max_morning_shifts,
        'min_morning_shifts_in_period': constraint.min_morning_shifts_in_period,
        'max_morning_shifts_in_period': constraint.max_morning_shifts_in_period,
        'min_afternoon_shifts': constraint.min_afternoon_shifts,
        'max_afternoon_shifts': constraint.max_afternoon_shifts,
        'min_afternoon_shifts_in_period': constraint.min_afternoon_shifts_in_period,
        'max_afternoon_shifts_in_period': constraint.max_afternoon_shifts_in_period,
        'min_night_shifts': constraint.min_night_shifts,
        'max_night_shifts': constraint.max_night_shifts,
        'min_night_shifts_in_period': constraint.min_night_shifts_in_period,
        'max_night_shifts_in_period': constraint.max_night_shifts_in_period
    })

@constraints_bp.route('/constraints', methods=['POST'])
def add_constraint():
    data = request.json
    new_constraint = Constraint(
        exact_days_off_per_month=data.get('exact_days_off_per_month'),
        min_days_off=data.get('min_days_off'),
        max_days_off=data.get('max_days_off'),
        min_days_off_in_period=data.get('min_days_off_in_period'),
        max_days_off_in_period=data.get('max_days_off_in_period'),
        min_morning_shifts=data.get('min_morning_shifts'),
        max_morning_shifts=data.get('max_morning_shifts'),
        min_morning_shifts_in_period=data.get('min_morning_shifts_in_period'),
        max_morning_shifts_in_period=data.get('max_morning_shifts_in_period'),
        min_afternoon_shifts=data.get('min_afternoon_shifts'),
        max_afternoon_shifts=data.get('max_afternoon_shifts'),
        min_afternoon_shifts_in_period=data.get('min_afternoon_shifts_in_period'),
        max_afternoon_shifts_in_period=data.get('max_afternoon_shifts_in_period'),
        min_night_shifts=data.get('min_night_shifts'),
        max_night_shifts=data.get('max_night_shifts'),
        min_night_shifts_in_period=data.get('min_night_shifts_in_period'),
        max_night_shifts_in_period=data.get('max_night_shifts_in_period')
    )
    session.add(new_constraint)
    session.commit()
    return jsonify({'message': 'Constraint added successfully'}), 201

@constraints_bp.route('/constraints/<int:id>', methods=['PUT'])
def update_constraint(id):
    data = request.json
    constraint = session.query(Constraint).get(id)
    if not constraint:
        return jsonify({'error': 'Constraint not found'}), 404

    constraint.exact_days_off_per_month = data.get('exact_days_off_per_month', constraint.exact_days_off_per_month)
    constraint.min_days_off = data.get('min_days_off', constraint.min_days_off)
    constraint.max_days_off = data.get('max_days_off', constraint.max_days_off)
    constraint.min_days_off_in_period = data.get('min_days_off_in_period', constraint.min_days_off_in_period)
    constraint.max_days_off_in_period = data.get('max_days_off_in_period', constraint.max_days_off_in_period)
    constraint.min_morning_shifts = data.get('min_morning_shifts', constraint.min_morning_shifts)
    constraint.max_morning_shifts = data.get('max_morning_shifts', constraint.max_morning_shifts)
    constraint.min_morning_shifts_in_period = data.get('min_morning_shifts_in_period', constraint.min_morning_shifts_in_period)
    constraint.max_morning_shifts_in_period = data.get('max_morning_shifts_in_period', constraint.max_morning_shifts_in_period)
    constraint.min_afternoon_shifts = data.get('min_afternoon_shifts', constraint.min_afternoon_shifts)
    constraint.max_afternoon_shifts = data.get('max_afternoon_shifts', constraint.max_afternoon_shifts)
    constraint.min_afternoon_shifts_in_period = data.get('min_afternoon_shifts_in_period', constraint.min_afternoon_shifts_in_period)
    constraint.max_afternoon_shifts_in_period = data.get('max_afternoon_shifts_in_period', constraint.max_afternoon_shifts_in_period)
    constraint.min_night_shifts = data.get('min_night_shifts', constraint.min_night_shifts)
    constraint.max_night_shifts = data.get('max_night_shifts', constraint.max_night_shifts)
    constraint.min_night_shifts_in_period = data.get('min_night_shifts_in_period', constraint.min_night_shifts_in_period)
    constraint.max_night_shifts_in_period = data.get('max_night_shifts_in_period', constraint.max_night_shifts_in_period)

    session.commit()
    return jsonify({'message': 'Constraint updated successfully'}), 200

@constraints_bp.route('/constraints/<int:id>', methods=['DELETE'])
def delete_constraint(id):
    constraint = session.query(Constraint).get(id)
    if not constraint:
        return jsonify({'error': 'Constraint not found'}), 404

    session.delete(constraint)
    session.commit()
    return jsonify({'message': 'Constraint deleted successfully'}), 200
