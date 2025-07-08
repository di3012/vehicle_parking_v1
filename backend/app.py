from flask import Flask, request
from flask_security import Security, auth_required, roles_accepted
from flask_restful import Api

from models import db, test, test1, user_datastore
from config import devConfig

def create_app():
    init_app = Flask(__name__)
    init_app.config.from_object(devConfig)

    db.init_app(init_app)

    Security(init_app, user_datastore)

    init_api = Api(init_app, prefix='/api')
    return init_app, init_api

app, api = create_app()

from routes.auth import RegisterResource, LoginResource
api.add_resource(RegisterResource, '/register')
api.add_resource(LoginResource, '/login')

from routes.test import homeResource
api.add_resource(homeResource, '/', '/<string:name>')

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    if not email:
        return {'message': 'Email is required'}, 400
    password = data.get('password')
    if not password:
        return {'message': 'Password is required'}, 400
    username = data.get('username')

    if user_datastore.find_user(email=email):
        return {'message': 'User already exists'}, 400
    
    if username and user_datastore.find_user(username=username):
        return {'message': 'Username already exists'}, 400
    
    try:
        user = user_datastore. create_user(
            email=email,
            password=password,
            username=username
        )
        user_datastore.add_role_to_user(user, user_datastore.find_role('user'))
        db.session.commit()
        return {'message': 'User registered successfully', 'user_id': user.id}, 201
    except Exception as e:
        db.session.rollback()
        return {'message': f'An error occurred: {e}'}, 500
    
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    if not email:
        return {'message': 'Email is required'}, 400
    password = data.get('password')
    if not password:
        return {'message': 'Password is required'}, 400
    
    user = user_datastore.find_user(email=email)
    if not user:
        return {'message': 'Email is not registered with us'}, 404
    if not user.active:
        return {'message': 'User is not active'}, 403
    if user.password == password:
        return {
            'message': 'Login successful', 
            'user_id': user.id, 
            'user_email': user.email, 'user_role': user.roles[0].name,
            'authToken': user.get_auth_token()
            }, 200

@app.route('/')
def home():
    return "hello world"

@app.route('/about/<name>')
def about1(name):
    return {"name": name}

@app.route('/querydata')
@auth_required('token')
@roles_accepted('admin', 'user')
def querydata():
    data = test.query.all()
    if not data:
        return {'message': 'No data found'}, 404
    dbData = []
    for item in data:
        dbData.append({
            'id': item.id,
            'name': item.name,
            'number': item.number
        })
    print(dbData)
    return {'message': 'Data fetched successfully', 'data': dbData}

@app.route('/savedata', methods=['POST'])
@auth_required('token')
@roles_accepted('admin')
def savedata():
    data = request.json
    name = data.get('name')
    number = data.get('number')
    if not name:
        return {'message': 'Name is required'}, 400
    if not number:
        return {'message': 'Number is required'}, 400
    try:
        new_data = test(name=name, number=number)
        db.session.add(new_data)
        db.session.commit()
        return {'message': 'Data saved successfully', 'data': {'id': new_data.id, 'name': name, 'number': number}}, 201
    except Exception as e:
        db.session.rollback()
        return f"An error occurred: {e}", 500

    
@app.route('/updatedata/<int:id>', methods=['POST'])
@roles_accepted('admin')
@auth_required('token')
def updatedata(id):
    data = test.query.filter_by(id=id).first()
    form_data = request.json
    data.name = form_data.get('name', data.name)
    data.number = form_data.get('number', data.number)
    try:
        db.session.commit()
        return {'message': 'Data updated successfully', 'data': {'id': data.id, 'name': data.name, 'number': data.number}}, 200
    except Exception as e:
        db.session.rollback()
        return f"An error occurred: {e}", 500
    

@app.route('/deletedata/<int:id>', methods=['GET'])
@roles_accepted('admin')
@auth_required('token')
def deletedata(id):
    data = test.query.filter_by(id=id).first()
    if request.method == 'GET':
        try:
            db.session.delete(data)
            db.session.commit()
            return {'message': 'Data deleted successfully'}, 200
        except Exception as e:
            db.session.rollback()
            return f"An error occurred: {e}", 500
        
@app.route('/test1', methods=['POST', 'GET'])
@roles_accepted('admin')
@auth_required('token')
def test1_route():
    if request.method == 'POST':
        data = request.json
        clname = data.get('clname')
        if not clname:
            return {'message': 'clname is required'}, 400
        try:
            new_data = test1(clname=clname)
            db.session.add(new_data)
            db.session.commit()
            return {'message': 'Data saved successfully', 'data': {'clid': new_data.clid, 'clname': clname}}, 201
        except Exception as e:
            db.session.rollback()
            return f"An error occurred: {e}", 500
    if request.method == 'GET':
        data = test1.query.all()
        if not data:
            return {'message': 'No data found'}, 404
        dbData = [{'clid': item.clid, 'clname': item.clname} for item in data]
        return {'message': 'Data fetched successfully', 'data': dbData}

@app.route('/test1/<int:clid>', methods=['PUT', 'GET', 'DELETE'])
@roles_accepted('admin')
@auth_required('token')
def test1_detail(clid):
    data = test1.query.filter_by(clid=clid).first()
    if not data:
        return {'message': 'Data not found'}, 404

    if request.method == 'GET':
        return {'message': 'Data fetched successfully', 'data': {'clid': data.clid, 'clname': data.clname}}

    if request.method == 'PUT':
        form_data = request.json
        data.clname = form_data.get('clname', data.clname)
        try:
            db.session.commit()
            return {'message': 'Data updated successfully', 'data': {'clid': data.clid, 'clname': data.clname}}, 200
        except Exception as e:
            db.session.rollback()
            return f"An error occurred: {e}", 500

    if request.method == 'DELETE':
        try:
            db.session.delete(data)
            db.session.commit()
            return {'message': 'Data deleted successfully'}, 200
        except Exception as e:
            db.session.rollback()
            return f"An error occurred: {e}", 500

if __name__ == '__main__':
    app.run()