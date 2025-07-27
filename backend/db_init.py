from app import create_app
from models import db, User, Role
from flask_security.utils import hash_password

def create_admin_user():
    admin_role = Role.query.filter_by(name='admin').first()
    if not admin_role:
        admin_role = Role(name='admin')
        db.session.add(admin_role)

    user = User.query.filter_by(email='admin@abc.com').first()
    if not user:
        user = User(
            name='admin',
            email='admin@abc.com',
            password=hash_password('admin123'),
            active=True
        )
        user.roles.append(admin_role)
        db.session.add(user)

    db.session.commit()
    print("✅ Admin created")

# 👇 Use app context and initialize DB here
app = create_app()
with app.app_context():
    db.create_all()
    create_admin_user()
