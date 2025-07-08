from models import db, user_datastore
from app import create_app

app, _ = create_app()

def create_roles():
    user_datastore.find_or_create_role(name='admin', description='Administrator')
    user_datastore.find_or_create_role(name='user', description='Regular User')
    db.session.commit()

def create_admin_user():
    if not user_datastore.find_user(email='admin@abc.com'):
        user = user_datastore.create_user(email='admin@abc.com', password='admin')
        user_datastore.add_role_to_user(user, user_datastore.find_role('admin'))
        db.session.commit()

with app.app_context():
    db.create_all()
    create_roles()
    create_admin_user()