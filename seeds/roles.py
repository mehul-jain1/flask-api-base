from flask_seeder import Seeder

from app.models.role import Role


class RoleSeeder(Seeder):
    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 2

    def run(self):
        admin = Role(name="admin")
        self.db.session.add(admin)

        manager = Role(name="manager")
        self.db.session.add(manager)

        agent = Role(name="agent")
        self.db.session.add(agent)
