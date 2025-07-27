from celery_redis import celery
from models import db, User, Reservation
from flask_mail import Mail, Message
from flask import Flask
from datetime import datetime, date

app = Flask(__name__)
app.config.from_object('config.devConfig')
mail = Mail(app)

@celery.task(name='tasks.reminders.send_daily_reminder')
def send_daily_reminder():
    with app.app_context():
        users = User.query.all()
        today = date.today()

        for user in users:
            has_booked_today = Reservation.query.filter_by(user_id=user.id).filter(
                db.func.date(Reservation.parking_timestamp) == today
            ).first()

            if not has_booked_today:
                msg = Message(
                    subject="🅿 Daily Parking Reminder",
                    sender="your_email@example.com",
                    recipients=[user.email],
                    body=f"Hi {user.name},\n\nYou haven't booked a parking spot today. Reserve one if needed!\n\n- Parking App"
                )
                mail.send(msg)
