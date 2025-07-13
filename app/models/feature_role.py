from datetime import datetime

from app.factory import db


class FeatureRole(db.Model):
    __tablename__ = "feature_roles"

    id = db.Column(db.Integer, primary_key=True)
    feature_id = db.Column(
        db.Integer(), db.ForeignKey("features.id", ondelete="CASCADE"), nullable=False
    )
    role_id = db.Column(
        db.Integer(), db.ForeignKey("roles.id", ondelete="CASCADE"), nullable=False
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def serialize(self):
        return {
            "id": self.id,
            "feature": self.feature.name,
            "role": self.role.name,
            "created_at": self.created_at.strftime("%Y/%m/%d %H:%M:%S"),
            "updated_at": self.updated_at.strftime("%Y/%m/%d %H:%M:%S"),
        }
