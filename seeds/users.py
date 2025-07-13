from flask_seeder import Seeder

from app.models.role import Role
from app.models.user import User


class UserSeeder(Seeder):
    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 4

    def run(self):
        admin = Role.query.filter_by(name="admin").first()
        user = User(name="admin", email="admin@test.com", role=admin)
        self.db.session.add(user)

        manager = Role.query.filter_by(name="manager").first()
        user = User(name="manager", email="manager@test.com", role=manager)
        self.db.session.add(user)

        agent = Role.query.filter_by(name="agent").first()
        user = User(name="agent", email="agent@test.com", role=agent)
        self.db.session.add(user)
