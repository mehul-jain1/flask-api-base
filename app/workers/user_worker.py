from app import celery
from app.models.user import User
from app.support.mailer import Mailer


@celery.task(acks_late=True)
def user_email_worker(id):
    print("printing inside worker")
    user = User.query.get(id)
    if user:
        # Mailer.send_welcome_email(user)
        return True
    else:
        return False

    return True
