from flask import Blueprint, jsonify, request
from sqlalchemy.orm import sessionmaker 
from models import Demand
from utils.db import get_engine, get_session

demands_bp = Blueprint('demands', __name__)

# Set up the database session
engine = get_engine()
DBSession = sessionmaker(bind=engine)
session = get_session()

@demands_bp.route('/demands', methods=['GET'])
def get_demands():
    demands = session.query(Demand).all()
    return jsonify([{
        'id': d.id,
        'date': d.date.isoformat(),
        'demand': d.demand
    } for d in demands])

@demands_bp.route('/demands/<int:id>', methods=['GET'])
def get_demand(id):
    demand = session.query(Demand).get(id)
    if not demand:
        return jsonify({'error': 'Demand not found'}), 404

    return jsonify({
        'id': demand.id,
        'date': demand.date.isoformat(),
        'demand': demand.demand
    })

@demands_bp.route('/demands', methods=['POST'])
def add_demand():
    data = request.json
    new_demand = Demand(
        date=data.get('date'),
        demand=data.get('demand')
    )
    session.add(new_demand)
    session.commit()
    return jsonify({'message': 'Demand added successfully'}), 201

@demands_bp.route('/demands/<int:id>', methods=['PUT'])
def update_demand(id):
    data = request.json
    demand = session.query(Demand).get(id)
    if not demand:
        return jsonify({'error': 'Demand not found'}), 404

    demand.date = data.get('date', demand.date)
    demand.demand = data.get('demand', demand.demand)

    session.commit()
    return jsonify({'message': 'Demand updated successfully'}), 200

@demands_bp.route('/demands/<int:id>', methods=['DELETE'])
def delete_demand(id):
    demand = session.query(Demand).get(id)
    if not demand:
        return jsonify({'error': 'Demand not found'}), 404

    session.delete(demand)
    session.commit()
    return jsonify({'message': 'Demand deleted successfully'}), 200
