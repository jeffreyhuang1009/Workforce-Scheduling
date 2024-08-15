from flask import Blueprint, jsonify, request
from sqlalchemy.orm import sessionmaker
from models import ShiftDefinition
from utils.db import get_engine, get_session

shift_definitions_bp = Blueprint('shift_definitions', __name__)

# Set up the database session
engine = get_engine()
DBSession = sessionmaker(bind=engine)
session = get_session()

@shift_definitions_bp.route('/shift_definitions', methods=['GET'])
def get_shift_definitions():
    shift_definitions = session.query(ShiftDefinition).all()
    return jsonify([{
        'shift_def_id': s.shift_def_id,
        'type': s.type,
        'name': s.name,
        'periods': s.periods
    } for s in shift_definitions])

@shift_definitions_bp.route('/shift_definitions', methods=['POST'])
def add_shift_definition():
    data = request.json
    new_shift_definition = ShiftDefinition(
        type=data.get('type'),
        name=data.get('name'),
        periods=data.get('periods')
    )
    session.add(new_shift_definition)
    session.commit()
    return jsonify({'message': 'Shift definition added successfully'}), 201

@shift_definitions_bp.route('/shift_definitions/<int:id>', methods=['PUT'])
def update_shift_definition(id):
    data = request.json
    shift_definition = session.query(ShiftDefinition).get(id)
    if not shift_definition:
        return jsonify({'error': 'Shift definition not found'}), 404

    shift_definition.type = data.get('type', shift_definition.type)
    shift_definition.name = data.get('name', shift_definition.name)
    shift_definition.periods = data.get('periods', shift_definition.periods)

    session.commit()
    return jsonify({'message': 'Shift definition updated successfully'}), 200

@shift_definitions_bp.route('/shift_definitions/<int:id>', methods=['DELETE'])
def delete_shift_definition(id):
    shift_definition = session.query(ShiftDefinition).get(id)
    if not shift_definition:
        return jsonify({'error': 'Shift definition not found'}), 404

    session.delete(shift_definition)
    session.commit()
    return jsonify({'message': 'Shift definition deleted successfully'}), 200

@shift_definitions_bp.route('/shift_definitions/<int:id>', methods=['GET'])
def get_shift_definition(id):
    shift_definition = session.query(ShiftDefinition).get(id)
    if not shift_definition:
        return jsonify({'error': 'Shift definition not found'}), 404

    return jsonify({
        'shift_def_id': shift_definition.shift_def_id,
        'type': shift_definition.type,
        'name': shift_definition.name,
        'periods': shift_definition.periods
    })
