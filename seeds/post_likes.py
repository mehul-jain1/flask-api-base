from flask_seeder import Seeder
from app.models.post import Post
from app.models.user import User
from app.models.post_like import PostLike

class PostLikeSeeder(Seeder):
    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 6

    def run(self):
        # Get existing users
        admin = User.query.filter_by(email='admin@test.com').first()
        manager = User.query.filter_by(email='manager@test.com').first()
        agent = User.query.filter_by(email='agent@test.com').first()

        # Get existing posts
        welcome_post = Post.query.filter_by(title="Welcome to the Platform").first()
        guide_post = Post.query.filter_by(title="Getting Started Guide").first()
        tips_post = Post.query.filter_by(title="Tips for New Users").first()
        updates_post = Post.query.filter_by(title="Platform Updates").first()
        guidelines_post = Post.query.filter_by(title="Community Guidelines").first()

        # Create some likes using the PostLike class methods
        if admin and guide_post:
            PostLike.create_like(admin, guide_post)
        
        if admin and tips_post:
            PostLike.create_like(admin, tips_post)

        if manager and welcome_post:
            PostLike.create_like(manager, welcome_post)
        
        if manager and tips_post:
            PostLike.create_like(manager, tips_post)
        
        if manager and updates_post:
            PostLike.create_like(manager, updates_post)

        if agent and welcome_post:
            PostLike.create_like(agent, welcome_post)
        
        if agent and guide_post:
            PostLike.create_like(agent, guide_post)
        
        if agent and updates_post:
            PostLike.create_like(agent, updates_post)
        
        if agent and guidelines_post:
            PostLike.create_like(agent, guidelines_post) 