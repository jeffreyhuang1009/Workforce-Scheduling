from flask import Blueprint, jsonify, request
from sqlalchemy.orm import sessionmaker
from models import Request
from utils.db import get_engine, get_session

requests_bp = Blueprint('requests', __name__)

# Set up the database session
engine = get_engine()
DBSession = sessionmaker(bind=engine)
session = get_session()

@requests_bp.route('/requests', methods=['GET'])
def get_requests():
    requests = session.query(Request).all()
    return jsonify([{
        'request_id': r.request_id,
        'csr_id': r.csr_id,
        'shift_def_id': r.shift_def_id,
        'status': r.status,
        'requested_date': r.requested_date.isoformat(),
        'notes': r.notes
    } for r in requests])

@requests_bp.route('/requests/<int:id>', methods=['GET'])
def get_request(id):
    request_obj = session.query(Request).get(id)
    if not request_obj:
        return jsonify({'error': 'Request not found'}), 404

    return jsonify({
        'request_id': request_obj.request_id,
        'csr_id': request_obj.csr_id,
        'shift_def_id': request_obj.shift_def_id,
        'status': request_obj.status,
        'requested_date': request_obj.requested_date.isoformat(),
        'notes': request_obj.notes
    })

@requests_bp.route('/requests', methods=['POST'])
def add_request():
    data = request.json
    new_request = Request(
        csr_id=data.get('csr_id'),
        shift_def_id=data.get('shift_def_id'),
        status=data.get('status'),
        requested_date=data.get('requested_date'),
        notes=data.get('notes')
    )
    session.add(new_request)
    session.commit()
    return jsonify({'message': 'Request added successfully'}), 201

@requests_bp.route('/requests/<int:id>', methods=['PUT'])
def update_request(id):
    data = request.json
    request_obj = session.query(Request).get(id)
    if not request_obj:
        return jsonify({'error': 'Request not found'}), 404

    request_obj.csr_id = data.get('csr_id', request_obj.csr_id)
    request_obj.shift_def_id = data.get('shift_def_id', request_obj.shift_def_id)
    request_obj.status = data.get('status', request_obj.status)
    request_obj.requested_date = data.get('requested_date', request_obj.requested_date)
    request_obj.notes = data.get('notes', request_obj.notes)

    session.commit()
    return jsonify({'message': 'Request updated successfully'}), 200

@requests_bp.route('/requests/<int:id>', methods=['DELETE'])
def delete_request(id):
    request_obj = session.query(Request).get(id)
    if not request_obj:
        return jsonify({'error': 'Request not found'}), 404

    session.delete(request_obj)
    session.commit()
    return jsonify({'message': 'Request deleted successfully'}), 200
