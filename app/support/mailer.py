from flask_mail import Message
from app.factory import mail

class Mailer:
    @staticmethod
    def send_welcome_email(user):
        msg = Message("Welcome!",
                      recipients=[user.email])
        msg.body = f"Hi {user.name},\n\nWelcome to our application!"
        mail.send(msg)
        print(f"Sent welcome email to {user.email}") 