from flask_seeder import Seeder
from app.models.feature import Feature
from app.models.role import Role
from app.models.feature_role import FeatureRole

class FeatureRoleSeeder(Seeder):
  def __init__(self, db=None):
    super().__init__(db=db)
    self.priority = 3

  def run(self):
    user_resource = Feature.query.filter_by(name = 'user_resource').first()
    admin   = Role.query.filter_by(name = 'admin').first()
    # Upload access
    user_admin = FeatureRole(feature = user_resource, role = admin)
    self.db.session.add(user_admin)