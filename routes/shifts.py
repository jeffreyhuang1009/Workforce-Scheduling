from flask import Blueprint, jsonify, request
from sqlalchemy.orm import sessionmaker
from models import Shift
from utils.db import get_engine, get_session

shifts_bp = Blueprint('shifts', __name__)

# Set up the database session
engine = get_engine()
DBSession = sessionmaker(bind=engine)
session = get_session()

@shifts_bp.route('/shifts', methods=['GET'])
def get_shifts():
    shifts = session.query(Shift).all()
    return jsonify([{
        'shift_id': s.shift_id,
        'csr_id': s.csr_id,
        'shift_def_id': s.shift_def_id,
        'date': s.date.isoformat()
    } for s in shifts])

@shifts_bp.route('/shifts/<int:id>', methods=['GET'])
def get_shift(id):
    shift = session.query(Shift).get(id)
    if not shift:
        return jsonify({'error': 'Shift not found'}), 404

    return jsonify({
        'shift_id': shift.shift_id,
        'csr_id': shift.csr_id,
        'shift_def_id': shift.shift_def_id,
        'date': shift.date.isoformat()
    })



@shifts_bp.route('/shifts/<int:id>', methods=['PUT'])
def update_shift(id):
    data = request.json
    shift = session.query(Shift).get(id)
    if not shift:
        return jsonify({'error': 'Shift not found'}), 404

    shift.csr_id = data.get('csr_id', shift.csr_id)
    shift.shift_def_id = data.get('shift_def_id', shift.shift_def_id)
    shift.date = data.get('date', shift.date)

    session.commit()
    return jsonify({'message': 'Shift updated successfully'}), 200

@shifts_bp.route('/shifts/<int:id>', methods=['DELETE'])
def delete_shift(id):
    shift = session.query(Shift).get(id)
    if not shift:
        return jsonify({'error': 'Shift not found'}), 404

    session.delete(shift)
    session.commit()
    return jsonify({'message': 'Shift deleted successfully'}), 200
