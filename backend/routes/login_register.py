# routes/user_routes.py
from flask import Blueprint, request, jsonify, session
from models import db, User
from flask_security.utils import verify_and_update_password, hash_password
from flask_login  import login_user

login_register = Blueprint("login_register", __name__)

@login_register.route('/api/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')

    if not email or not password:
        return jsonify({'message': 'Email and password required'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already registered'}), 400

    if name and User.query.filter_by(name=name).first():
        return jsonify({'message': 'Username already exists'}), 400

    user = User(email=email, password=hash_password(password), name=name)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

@login_register.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if user and verify_and_update_password(password, user):
        session['user_id'] = user.id
        print("✅ Logged in user ID:", session.get('user_id'))
        print("✅ User role:", user.roles[0].name if user.roles else 'user')
        login_user(user)
        return jsonify({'message': 'Login successful', 'role': user.roles[0].name if user.roles else 'user', 'user_id': user.id})
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

@login_register.route('/api/logout', methods=['POST'])
def logout():
    print("Logging out user:", session.get('user_id'))
    session.clear()
    return jsonify({'message': 'Logged out successfully'}), 200
