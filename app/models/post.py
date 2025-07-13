from app.factory import db
from datetime import datetime

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    author = db.relationship('User', backref='posts')
    likes = db.relationship('PostLike', backref='posts')
    
    def __repr__(self):
        return '<Post {}>'.format(self.title)

    def get_likes(self):
        """Get all likes for this post"""
        from app.models.post_like import PostLike
        return PostLike.get_likes_for_post(self.id)

    def get_likes_count(self):
        """Get count of likes for this post"""
        from app.models.post_like import PostLike
        return PostLike.get_likes_count_for_post(self.id)

    def is_liked_by(self, user):
        """Check if this post is liked by a specific user"""
        from app.models.post_like import PostLike
        return PostLike.exists(user.id, self.id)

    def get_users_who_liked(self):
        """Get all users who liked this post"""
        from app.models.post_like import PostLike
        likes = PostLike.get_likes_for_post(self.id)
        return [like.user for like in likes if like.user]

    @property
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'author_id': self.author_id,
            'author_name': self.author.name if self.author else None,
            'likes_count': self.get_likes_count(),
            'created_at': self.created_at.strftime("%Y/%m/%d %H:%M:%S"),
            'updated_at': self.updated_at.strftime("%Y/%m/%d %H:%M:%S")
        } 