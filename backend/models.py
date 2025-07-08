from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin, SQLAlchemyUserDatastore
db = SQLAlchemy()

class test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    number = db.Column(db.String())

class test1(db.Model):
    clid = db.Column(db.Integer, primary_key=True)
    clname = db.Column(db.String(80), nullable=False)

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True) #
    name = db.Column(db.String(80), unique=True, nullable=False) #
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) #
    email = db.Column(db.String(255), unique=True, nullable=False) #
    password = db.Column(db.String(255), nullable=False) #
    username = db.Column(db.String(80), unique=True)

    login_count = db.Column(db.Integer)
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(50))
    current_login_ip = db.Column(db.String(50))

    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False) #
    active = db.Column(db.Boolean()) #
    roles = db.relationship('Role', secondary='user_roles', backref=db.backref('users', lazy='dynamic')) #

class User_Roles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer, primary_key=True) #
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #
    role_id = db.Column(db.Integer, db.ForeignKey('role.id')) #

user_datastore = SQLAlchemyUserDatastore(db, User, Role)