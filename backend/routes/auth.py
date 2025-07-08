from models import db, user_datastore
from flask import request, jsonify, make_response
from flask_restful import Resource

# @app.route('/register', methods=['POST'])
# def register():
class RegisterResource(Resource):
    def post(self):
        data = request.json
        email = data.get('email')
        if not email:
            return make_response(jsonify({'message': 'Email is required'}), 400)
        password = data.get('password')
        if not password:
            return make_response(jsonify({'message': 'Password is required'}), 400)
        username = data.get('username')

        if user_datastore.find_user(email=email):
            return make_response(jsonify({'message': 'User already exists'}), 400)
        
        if username and user_datastore.find_user(username=username):
            return make_response(jsonify({'message': 'Username already exists'}), 400)
        
        try:
            user = user_datastore. create_user(
                email=email,
                password=password,
                username=username
            )
            user_datastore.add_role_to_user(user, user_datastore.find_role('user'))
            db.session.commit()
            return make_response(jsonify({'message': 'User registered successfully', 'user_id': user.id}), 201)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'message': f'An error occurred: {e}'}), 500)
    
# @app.route('/login', methods=['POST'])
# def login():
class LoginResource(Resource):
    def post(self):
        data = request.json
        email = data.get('email')
        if not email:
            return make_response(jsonify({'message': 'Email is required'}), 400)
        password = data.get('password')
        if not password:
            return make_response(jsonify({'message': 'Password is required'}), 400)
        
        user = user_datastore.find_user(email=email)
        if not user:
            return make_response(jsonify({'message': 'Email is not registered with us'}), 404)
        if not user.active:
            return make_response(jsonify({'message': 'User is not active'}), 403)
        if user.password == password:
            return make_response(jsonify({
                'message': 'Login successful', 
                'user_id': user.id, 
                'user_email': user.email, 'user_role': user.roles[0].name,
                'authToken': user.get_auth_token()
                }), 200)
    