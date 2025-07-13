from app.factory import db
from datetime import datetime

class PostLike(db.Model):
    __tablename__ = 'post_likes'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='post_likes')
    post = db.relationship('Post', backref='post_likes')
    
    def __repr__(self):
        return f'<PostLike user_id={self.user_id} post_id={self.post_id}>'

    @property
    def serialize(self):
        return {
            'user_id': self.user_id,
            'post_id': self.post_id,
            'user_name': self.user.name if self.user else None,
            'post_title': self.post.title if self.post else None,
            'created_at': self.created_at.strftime("%Y/%m/%d %H:%M:%S")
        } 