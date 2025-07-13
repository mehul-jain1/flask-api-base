from flask_seeder import Seeder

from app.models.feature import Feature


class FeatureSeeder(Seeder):
    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 1

    def run(self):
        user_resource = Feature(name="user_resource")
        self.db.session.add(user_resource)
