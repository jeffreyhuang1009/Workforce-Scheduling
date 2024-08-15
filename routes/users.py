from flask import Blueprint, jsonify, request
from sqlalchemy.orm import sessionmaker
from models import User
from utils.db import get_engine, get_session

users_bp = Blueprint('users', __name__)

# Set up the database session
engine = get_engine()
DBSession = sessionmaker(bind=engine)
session = get_session()

@users_bp.route('/users', methods=['GET'])
def get_users():
    users = session.query(User).all()
    return jsonify([{
        'user_id': u.user_id,
        'name': u.name,
        'email': u.email,
        'role': u.role
    } for u in users])

@users_bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = session.query(User).get(id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({
        'user_id': user.user_id,
        'name': user.name,
        'email': user.email,
        'role': user.role
    })

@users_bp.route('/users', methods=['POST'])
def add_user():
    data = request.json
    new_user = User(
        name=data.get('name'),
        email=data.get('email'),
        role=data.get('role')
    )
    session.add(new_user)
    session.commit()
    return jsonify({'message': 'User added successfully'}), 201

@users_bp.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.json
    user = session.query(User).get(id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    user.role = data.get('role', user.role)

    session.commit()
    return jsonify({'message': 'User updated successfully'}), 200

@users_bp.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = session.query(User).get(id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    session.delete(user)
    session.commit()
    return jsonify({'message': 'User deleted successfully'}), 200
