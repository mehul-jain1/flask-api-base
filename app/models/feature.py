from app.factory import db
from datetime import datetime

class Feature(db.Model):
  __tablename__ = 'features'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(120), index=True, unique=True, nullable=False)
  created_at = db.Column(db.DateTime, default=datetime.utcnow)
  updated_at = db.Column(db.DateTime, default=datetime.utcnow)
  feature_roles = db.relationship('FeatureRole', backref='feature', lazy='dynamic')

  def __repr__(self):
        return '<Feature {}>'.format(self.name)

  @property
  def serialize(self):
      return {
        'id': self.id,
        'name': self.name,
        'created_at': self.created_at.strftime("%Y/%m/%d %H:%M:%S"),
        'updated_at': self.updated_at.strftime("%Y/%m/%d %H:%M:%S")
      }