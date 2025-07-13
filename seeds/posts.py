from flask_seeder import Seeder
from app.models.post import Post
from app.models.user import User

class PostSeeder(Seeder):
    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 5

    def run(self):
        # Get existing users to be authors
        admin = User.query.filter_by(email='admin@test.com').first()
        manager = User.query.filter_by(email='manager@test.com').first()
        agent = User.query.filter_by(email='agent@test.com').first()

        # Create sample posts
        post1 = Post(
            title="Welcome to the Platform",
            content="This is our first post welcoming everyone to our new platform. We're excited to share updates and insights with our community.",
            author=admin
        )
        self.db.session.add(post1)

        post2 = Post(
            title="Getting Started Guide",
            content="Here's a comprehensive guide to help you get started with all the features available on our platform. Follow these steps to make the most of your experience.",
            author=manager
        )
        self.db.session.add(post2)

        post3 = Post(
            title="Tips for New Users",
            content="As someone who has been using this platform for a while, here are my top tips for new users to quickly become productive and efficient.",
            author=agent
        )
        self.db.session.add(post3)

        post4 = Post(
            title="Platform Updates",
            content="We've made several improvements to the platform this month. Here's a summary of all the new features and bug fixes.",
            author=admin
        )
        self.db.session.add(post4)

        post5 = Post(
            title="Community Guidelines",
            content="To maintain a positive and productive environment for everyone, please review our community guidelines and help us create a welcoming space.",
            author=manager
        )
        self.db.session.add(post5) 