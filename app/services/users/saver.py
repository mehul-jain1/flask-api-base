from app.factory import db
from app.models.role import Role
from app.models.user import User


class UserSaver:
    def __init__(self, user_data):
        self.user_data = user_data
        self.errors = []

    def save(self):
        try:
            print(f"saving user {self.user_data}")
            user = User(
                name=self.user_data["name"],
                email=self.user_data["email"],
            )
            user.role = self.get_role(self.user_data["role"])
            db.session.add(user)
            db.session.commit()
            db.session.refresh(user)
            return user
        except Exception as e:
            db.session.rollback()
            print(f"error saving user {e}")
            self.errors.append(str(e))
            return None

    def get_role(self, role_name):
        return Role.query.filter_by(name=role_name).first()
