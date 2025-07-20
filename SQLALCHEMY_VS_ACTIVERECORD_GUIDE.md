# SQLAlchemy vs ActiveRecord: Complete Comparison Guide

A comprehensive guide comparing Flask SQLAlchemy with Rails ActiveRecord, including query patterns, relationships, and testing strategies.

## 📖 Table of Contents

- [Quick Query Reference](#quick-query-reference)
- [Relationship Types](#relationship-types)
- [Complete Examples](#complete-examples)
- [Testing with Pytest and FactoryBoy](#testing-with-pytest-and-factoryboy)
- [Best Practices](#best-practices)

## 🔍 Quick Query Reference

### Basic Queries

| Operation | ActiveRecord (Rails) | Modern SQLAlchemy 2.x | Legacy SQLAlchemy |
|-----------|---------------------|----------------------|-------------------|
| **Get all records** | `User.all` | `db.session.scalars(select(User)).all()` | `User.query.all()` |
| **Get first record** | `User.first` | `db.session.scalars(select(User).limit(1)).first()` | `User.query.first()` |
| **Get last record** | `User.last` | `db.session.scalars(select(User).order_by(User.id.desc()).limit(1)).first()` | `User.query.order_by(User.id.desc()).first()` |
| **Find by ID** | `User.find(1)` | `db.session.get(User, 1)` | `User.query.get(1)` |
| **Find by attribute** | `User.find_by(email: "a@b.com")` | `db.session.scalars(select(User).where(User.email == "a@b.com")).first()` | `User.query.filter_by(email="a@b.com").first()` |

### Filtering and Conditions

| Operation | ActiveRecord (Rails) | Modern SQLAlchemy 2.x | Legacy SQLAlchemy |
|-----------|---------------------|----------------------|-------------------|
| **Simple filter** | `User.where(active: true)` | `db.session.scalars(select(User).where(User.active.is_(True))).all()` | `User.query.filter_by(active=True).all()` |
| **Multiple conditions** | `User.where(active: true, role: "admin")` | `db.session.scalars(select(User).where(User.active.is_(True), User.role == "admin")).all()` | `User.query.filter_by(active=True, role="admin").all()` |
| **OR conditions** | `User.where("name = ? OR name = ?", "Alice", "Bob")` | `db.session.scalars(select(User).where(or_(User.name == "Alice", User.name == "Bob"))).all()` | `User.query.filter(or_(User.name == "Alice", User.name == "Bob")).all()` |

### Ordering and Limiting

| Operation | ActiveRecord (Rails) | Modern SQLAlchemy 2.x | Legacy SQLAlchemy |
|-----------|---------------------|----------------------|-------------------|
| **Order by** | `User.order(:created_at)` | `db.session.scalars(select(User).order_by(User.created_at)).all()` | `User.query.order_by(User.created_at).all()` |
| **Limit and offset** | `User.limit(5).offset(10)` | `db.session.scalars(select(User).limit(5).offset(10)).all()` | `User.query.limit(5).offset(10).all()` |
| **Take specific count** | `User.take(3)` | `db.session.scalars(select(User).limit(3)).all()` | `User.query.limit(3).all()` |

### Aggregations

| Operation | ActiveRecord (Rails) | Modern SQLAlchemy 2.x | Legacy SQLAlchemy |
|-----------|---------------------|----------------------|-------------------|
| **Count** | `User.count` | `db.session.scalar(select(func.count(User.id)))` | `User.query.count()` |
| **Sum** | `User.sum(:age)` | `db.session.scalar(select(func.sum(User.age)))` | `db.session.query(func.sum(User.age)).scalar()` |
| **Average** | `User.average(:age)` | `db.session.scalar(select(func.avg(User.age)))` | `db.session.query(func.avg(User.age)).scalar()` |
| **Min/Max** | `User.minimum(:age)` / `User.maximum(:age)` | `db.session.scalar(select(func.min(User.age)))` / `db.session.scalar(select(func.max(User.age)))` | `db.session.query(func.min(User.age)).scalar()` |

## 🔗 Relationship Types

### Overview

| Relationship Type | SQLAlchemy | ActiveRecord | Description |
|------------------|------------|--------------|-------------|
| **One-to-One** | `db.relationship(..., uselist=False)` | `has_one` + `belongs_to` | Single related record |
| **One-to-Many** | `db.relationship(...)` | `has_many` + `belongs_to` | Parent has multiple children |
| **Many-to-One** | `db.ForeignKey(...)` + `relationship(...)` | `belongs_to` | Child belongs to parent |
| **Many-to-Many** | `db.relationship(..., secondary=...)` | `has_and_belongs_to_many` | Many records relate to many |
| **Many-to-Many with data** | Association object + relationships | `has_many :through` | Join table with additional fields |

## 📋 Complete Examples

### Setup and Imports

```python
# app/models/__init__.py
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select, func, or_, and_
from sqlalchemy.orm import selectinload, joinedload

db = SQLAlchemy()
```

### One-to-One Relationship

```python
# app/models/user.py
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    # One-to-One relationship
    profile = db.relationship("Profile", back_populates="user", uselist=False, cascade="all, delete-orphan")

# app/models/profile.py
class Profile(db.Model):
    __tablename__ = 'profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    bio = db.Column(db.Text)
    avatar_url = db.Column(db.String(255))
    
    # Back reference to user
    user = db.relationship("User", back_populates="profile")
```

**Rails Equivalent:**
```ruby
# app/models/user.rb
class User < ApplicationRecord
  has_one :profile, dependent: :destroy
end

# app/models/profile.rb
class Profile < ApplicationRecord
  belongs_to :user
end
```

### One-to-Many Relationship

```python
# app/models/author.py
class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    
    # One-to-Many relationship
    books = db.relationship("Book", back_populates="author", cascade="all, delete-orphan")

# app/models/book.py
class Book(db.Model):
    __tablename__ = 'books'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    isbn = db.Column(db.String(13), unique=True)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable=False)
    
    # Many-to-One relationship
    author = db.relationship("Author", back_populates="books")
```

**Rails Equivalent:**
```ruby
# app/models/author.rb
class Author < ApplicationRecord
  has_many :books, dependent: :destroy
end

# app/models/book.rb
class Book < ApplicationRecord
  belongs_to :author
end
```

### Many-to-Many Relationship

```python
# app/models/associations.py
# Join table for many-to-many relationship
student_courses = db.Table(
    'student_courses',
    db.Column('student_id', db.Integer, db.ForeignKey('students.id'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('courses.id'), primary_key=True),
    db.Column('enrolled_at', db.DateTime, default=db.func.current_timestamp())
)

# app/models/student.py
class Student(db.Model):
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    # Many-to-Many relationship
    courses = db.relationship(
        "Course", 
        secondary=student_courses, 
        back_populates="students",
        lazy='dynamic'
    )

# app/models/course.py
class Course(db.Model):
    __tablename__ = 'courses'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(10), unique=True, nullable=False)
    
    # Many-to-Many relationship
    students = db.relationship(
        "Student", 
        secondary=student_courses, 
        back_populates="courses",
        lazy='dynamic'
    )
```

**Rails Equivalent:**
```ruby
# app/models/student.rb
class Student < ApplicationRecord
  has_and_belongs_to_many :courses
end

# app/models/course.rb
class Course < ApplicationRecord
  has_and_belongs_to_many :students
end
```

### Many-to-Many with Additional Data (Association Object)

```python
# app/models/enrollment.py
class Enrollment(db.Model):
    __tablename__ = 'enrollments'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    
    # Additional fields
    grade = db.Column(db.String(2))
    enrolled_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    completed_at = db.Column(db.DateTime)
    
    # Relationships
    student = db.relationship("Student", back_populates="enrollments")
    course = db.relationship("Course", back_populates="enrollments")
    
    # Composite unique constraint
    __table_args__ = (db.UniqueConstraint('student_id', 'course_id'),)

# Update Student model
class Student(db.Model):
    # ... existing fields ...
    
    enrollments = db.relationship("Enrollment", back_populates="student", cascade="all, delete-orphan")
    
    # Convenience property to access courses through enrollments
    @property
    def enrolled_courses(self):
        return [enrollment.course for enrollment in self.enrollments]

# Update Course model  
class Course(db.Model):
    # ... existing fields ...
    
    enrollments = db.relationship("Enrollment", back_populates="course", cascade="all, delete-orphan")
    
    # Convenience property to access students through enrollments
    @property
    def enrolled_students(self):
        return [enrollment.student for enrollment in self.enrollments]
```

**Rails Equivalent:**
```ruby
# app/models/student.rb
class Student < ApplicationRecord
  has_many :enrollments, dependent: :destroy
  has_many :courses, through: :enrollments
end

# app/models/course.rb
class Course < ApplicationRecord
  has_many :enrollments, dependent: :destroy
  has_many :students, through: :enrollments
end

# app/models/enrollment.rb
class Enrollment < ApplicationRecord
  belongs_to :student
  belongs_to :course
  
  validates :student_id, uniqueness: { scope: :course_id }
end
```

## 🧪 Testing with Pytest and FactoryBoy

### Setup Files

#### conftest.py
```python
# tests/conftest.py
import pytest
from app import create_app
from app.models import db
from tests.factories import *

@pytest.fixture(scope='session')
def app():
    """Create application for testing."""
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture(scope='function')
def client(app):
    """Create test client."""
    return app.test_client()

@pytest.fixture(scope='function')
def db_session(app):
    """Create database session for testing."""
    with app.app_context():
        connection = db.engine.connect()
        transaction = connection.begin()
        
        # Configure session to use this connection
        options = dict(bind=connection, binds={})
        session = db.create_scoped_session(options=options)
        
        # Make this the default session
        db.session = session
        
        # Set up factories to use this session
        from tests.factories import BaseFactory
        BaseFactory._meta.sqlalchemy_session = session
        
        yield session
        
        # Cleanup
        transaction.rollback()
        connection.close()
        session.remove()
```

#### factories.py
```python
# tests/factories.py
import factory
from factory.alchemy import SQLAlchemyModelFactory
from factory import SubFactory, LazyAttribute, Sequence
from app.models import User, Profile, Author, Book, Student, Course, Enrollment

class BaseFactory(SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session_persistence = "commit"

# One-to-One Factories
class UserFactory(BaseFactory):
    class Meta:
        model = User
    
    name = factory.Faker('name')
    email = factory.Sequence(lambda n: f'user{n}@example.com')

class ProfileFactory(BaseFactory):
    class Meta:
        model = Profile
    
    user = SubFactory(UserFactory)
    bio = factory.Faker('text', max_nb_chars=200)
    avatar_url = factory.Faker('image_url')

# One-to-Many Factories
class AuthorFactory(BaseFactory):
    class Meta:
        model = Author
    
    name = factory.Faker('name')

class BookFactory(BaseFactory):
    class Meta:
        model = Book
    
    title = factory.Faker('sentence', nb_words=4)
    isbn = factory.Sequence(lambda n: f'978{n:010d}')
    author = SubFactory(AuthorFactory)

# Many-to-Many Factories
class StudentFactory(BaseFactory):
    class Meta:
        model = Student
    
    name = factory.Faker('name')
    email = factory.Sequence(lambda n: f'student{n}@university.edu')

class CourseFactory(BaseFactory):
    class Meta:
        model = Course
    
    name = factory.Faker('word')
    code = factory.Sequence(lambda n: f'CS{n:03d}')

class EnrollmentFactory(BaseFactory):
    class Meta:
        model = Enrollment
    
    student = SubFactory(StudentFactory)
    course = SubFactory(CourseFactory)
    grade = factory.Faker('random_element', elements=['A', 'B', 'C', 'D', 'F'])
```

### Test Files

#### test_relationships.py
```python
# tests/test_relationships.py
import pytest
from tests.factories import *

class TestOneToOneRelationship:
    """Test One-to-One relationships (User ↔ Profile)"""
    
    def test_user_profile_creation(self, db_session):
        """Test creating a user with a profile."""
        profile = ProfileFactory()
        
        assert profile.user is not None
        assert profile.user.profile == profile
        assert profile.user.name is not None
        assert profile.bio is not None
    
    def test_user_without_profile(self, db_session):
        """Test user can exist without a profile."""
        user = UserFactory()
        
        assert user.profile is None
    
    def test_profile_deletion_cascades(self, db_session):
        """Test that deleting user deletes associated profile."""
        profile = ProfileFactory()
        user = profile.user
        user_id = user.id
        
        db_session.delete(user)
        db_session.commit()
        
        # Profile should be deleted due to cascade
        assert db_session.get(Profile, profile.id) is None

class TestOneToManyRelationship:
    """Test One-to-Many relationships (Author → Books)"""
    
    def test_author_with_books(self, db_session):
        """Test author can have multiple books."""
        author = AuthorFactory()
        book1 = BookFactory(author=author)
        book2 = BookFactory(author=author)
        
        assert len(author.books) == 2
        assert book1 in author.books
        assert book2 in author.books
        assert book1.author == author
        assert book2.author == author
    
    def test_author_without_books(self, db_session):
        """Test author can exist without books."""
        author = AuthorFactory()
        
        assert len(author.books) == 0
    
    def test_book_deletion_doesnt_affect_author(self, db_session):
        """Test deleting book doesn't delete author."""
        book = BookFactory()
        author = book.author
        author_id = author.id
        
        db_session.delete(book)
        db_session.commit()
        
        # Author should still exist
        assert db_session.get(Author, author_id) is not None
    
    def test_author_deletion_cascades_to_books(self, db_session):
        """Test deleting author deletes all their books."""
        author = AuthorFactory()
        book1 = BookFactory(author=author)
        book2 = BookFactory(author=author)
        book_ids = [book1.id, book2.id]
        
        db_session.delete(author)
        db_session.commit()
        
        # Books should be deleted due to cascade
        for book_id in book_ids:
            assert db_session.get(Book, book_id) is None

class TestManyToManyRelationship:
    """Test Many-to-Many relationships (Student ↔ Course)"""
    
    def test_student_course_enrollment(self, db_session):
        """Test student can enroll in multiple courses."""
        student = StudentFactory()
        course1 = CourseFactory()
        course2 = CourseFactory()
        
        student.courses.append(course1)
        student.courses.append(course2)
        db_session.commit()
        
        assert course1 in student.courses.all()
        assert course2 in student.courses.all()
        assert student in course1.students.all()
        assert student in course2.students.all()
    
    def test_course_multiple_students(self, db_session):
        """Test course can have multiple students."""
        course = CourseFactory()
        student1 = StudentFactory()
        student2 = StudentFactory()
        
        course.students.append(student1)
        course.students.append(student2)
        db_session.commit()
        
        assert student1 in course.students.all()
        assert student2 in course.students.all()
        assert course in student1.courses.all()
        assert course in student2.courses.all()

class TestAssociationObjectRelationship:
    """Test Many-to-Many with additional data (Enrollment)"""
    
    def test_enrollment_creation(self, db_session):
        """Test creating enrollment with additional data."""
        enrollment = EnrollmentFactory()
        
        assert enrollment.student is not None
        assert enrollment.course is not None
        assert enrollment.grade is not None
        assert enrollment in enrollment.student.enrollments
        assert enrollment in enrollment.course.enrollments
    
    def test_student_enrolled_courses_property(self, db_session):
        """Test convenience property for accessing courses."""
        student = StudentFactory()
        course1 = CourseFactory()
        course2 = CourseFactory()
        
        enrollment1 = EnrollmentFactory(student=student, course=course1, grade='A')
        enrollment2 = EnrollmentFactory(student=student, course=course2, grade='B')
        
        enrolled_courses = student.enrolled_courses
        assert len(enrolled_courses) == 2
        assert course1 in enrolled_courses
        assert course2 in enrolled_courses
    
    def test_course_enrolled_students_property(self, db_session):
        """Test convenience property for accessing students."""
        course = CourseFactory()
        student1 = StudentFactory()
        student2 = StudentFactory()
        
        enrollment1 = EnrollmentFactory(student=student1, course=course, grade='A')
        enrollment2 = EnrollmentFactory(student=student2, course=course, grade='C')
        
        enrolled_students = course.enrolled_students
        assert len(enrolled_students) == 2
        assert student1 in enrolled_students
        assert student2 in enrolled_students
    
    def test_unique_constraint(self, db_session):
        """Test that student can't enroll in same course twice."""
        student = StudentFactory()
        course = CourseFactory()
        
        # First enrollment should work
        enrollment1 = EnrollmentFactory(student=student, course=course)
        
        # Second enrollment should fail due to unique constraint
        with pytest.raises(Exception):  # IntegrityError in real database
            enrollment2 = EnrollmentFactory(student=student, course=course)
            db_session.commit()
```

#### test_queries.py
```python
# tests/test_queries.py
import pytest
from sqlalchemy import select, func, or_, and_
from tests.factories import *

class TestBasicQueries:
    """Test basic query operations."""
    
    def test_get_all_users(self, db_session):
        """Test getting all users."""
        users = [UserFactory() for _ in range(3)]
        
        # Modern SQLAlchemy
        all_users = db_session.scalars(select(User)).all()
        assert len(all_users) == 3
    
    def test_get_first_user(self, db_session):
        """Test getting first user."""
        users = [UserFactory() for _ in range(3)]
        
        first_user = db_session.scalars(select(User).limit(1)).first()
        assert first_user is not None
        assert first_user.id == users[0].id
    
    def test_find_by_id(self, db_session):
        """Test finding user by ID."""
        user = UserFactory()
        
        found_user = db_session.get(User, user.id)
        assert found_user == user
    
    def test_filter_by_email(self, db_session):
        """Test filtering by email."""
        user = UserFactory(email="test@example.com")
        UserFactory(email="other@example.com")
        
        found_user = db_session.scalars(
            select(User).where(User.email == "test@example.com")
        ).first()
        
        assert found_user == user

class TestComplexQueries:
    """Test complex query operations."""
    
    def test_join_query(self, db_session):
        """Test joining tables."""
        author = AuthorFactory(name="Test Author")
        book1 = BookFactory(author=author, title="Book 1")
        book2 = BookFactory(author=author, title="Book 2")
        
        # Get authors with their books
        authors_with_books = db_session.scalars(
            select(Author)
            .join(Book)
            .where(Book.title.like("Book%"))
        ).all()
        
        assert len(authors_with_books) == 1
        assert authors_with_books[0] == author
    
    def test_eager_loading(self, db_session):
        """Test eager loading relationships."""
        from sqlalchemy.orm import selectinload
        
        author = AuthorFactory()
        books = [BookFactory(author=author) for _ in range(3)]
        
        # Eager load books with author
        authors = db_session.scalars(
            select(Author).options(selectinload(Author.books))
        ).all()
        
        assert len(authors[0].books) == 3
    
    def test_aggregation_queries(self, db_session):
        """Test aggregation functions."""
        author1 = AuthorFactory()
        author2 = AuthorFactory()
        
        # Author1 has 3 books, Author2 has 2 books
        [BookFactory(author=author1) for _ in range(3)]
        [BookFactory(author=author2) for _ in range(2)]
        
        # Count books per author
        book_counts = db_session.execute(
            select(Author.id, func.count(Book.id).label('book_count'))
            .join(Book)
            .group_by(Author.id)
        ).all()
        
        book_counts_dict = {author_id: count for author_id, count in book_counts}
        assert book_counts_dict[author1.id] == 3
        assert book_counts_dict[author2.id] == 2
```

## 🎯 Best Practices

### SQLAlchemy Best Practices

1. **Use Modern SQLAlchemy 2.x syntax** with `select()` statements
2. **Always use `db.session.commit()`** after database modifications
3. **Use eager loading** to avoid N+1 queries: `selectinload()`, `joinedload()`
4. **Define relationships clearly** with `back_populates` for bidirectional relationships
5. **Use cascades appropriately**: `cascade="all, delete-orphan"` for dependent records
6. **Add proper constraints**: foreign keys, unique constraints, indexes
7. **Use factory patterns** for testing to create consistent test data

### ActiveRecord Best Practices

1. **Use scopes** for reusable query logic
2. **Leverage associations** instead of manual joins
3. **Use `includes`** to prevent N+1 queries
4. **Add proper validations** and callbacks
5. **Use `dependent: :destroy`** for cascading deletes
6. **Create factories** with FactoryBot for testing

### Common Patterns

#### Repository Pattern (SQLAlchemy)
```python
# app/repositories/user_repository.py
class UserRepository:
    def __init__(self, db_session):
        self.db_session = db_session
    
    def find_by_email(self, email):
        return self.db_session.scalars(
            select(User).where(User.email == email)
        ).first()
    
    def find_active_users(self):
        return self.db_session.scalars(
            select(User).where(User.active.is_(True))
        ).all()
    
    def create(self, **kwargs):
        user = User(**kwargs)
        self.db_session.add(user)
        self.db_session.commit()
        return user
```

#### Scopes Pattern (ActiveRecord equivalent in SQLAlchemy)
```python
# app/models/user.py
class User(db.Model):
    # ... model definition ...
    
    @classmethod
    def active(cls):
        return select(cls).where(cls.active.is_(True))
    
    @classmethod
    def with_profile(cls):
        return select(cls).options(selectinload(cls.profile))
    
    @classmethod
    def by_role(cls, role):
        return select(cls).where(cls.role == role)

# Usage:
active_users = db.session.scalars(User.active()).all()
admin_users = db.session.scalars(User.by_role('admin')).all()
```

### Advanced Query Examples

#### Complex Filtering
```python
# SQLAlchemy - Complex conditions
users = db.session.scalars(
    select(User)
    .where(
        and_(
            User.active.is_(True),
            or_(
                User.role == 'admin',
                User.role == 'manager'
            ),
            User.created_at > datetime(2023, 1, 1)
        )
    )
    .order_by(User.created_at.desc())
    .limit(10)
).all()
```

```ruby
# ActiveRecord equivalent
users = User
  .where(active: true)
  .where(role: ['admin', 'manager'])
  .where('created_at > ?', Date.new(2023, 1, 1))
  .order(created_at: :desc)
  .limit(10)
```

#### Subqueries
```python
# SQLAlchemy - Subquery
subquery = select(Book.author_id).where(Book.published_year > 2020)
recent_authors = db.session.scalars(
    select(Author).where(Author.id.in_(subquery))
).all()
```

```ruby
# ActiveRecord equivalent
recent_authors = Author
  .joins(:books)
  .where(books: { published_year: 2021.. })
  .distinct
```

#### Window Functions
```python
# SQLAlchemy - Window functions
from sqlalchemy import func

query = db.session.execute(
    select(
        Book.title,
        Book.author_id,
        func.row_number().over(
            partition_by=Book.author_id,
            order_by=Book.published_year.desc()
        ).label('book_rank')
    )
).all()
```

```ruby
# ActiveRecord equivalent (Rails 7+)
books = Book
  .select(
    :title,
    :author_id,
    "ROW_NUMBER() OVER (PARTITION BY author_id ORDER BY published_year DESC) AS book_rank"
  )
```

## 📊 Performance Considerations

### N+1 Query Prevention

**SQLAlchemy:**
```python
# Bad - N+1 queries
authors = db.session.scalars(select(Author)).all()
for author in authors:
    print(f"{author.name} has {len(author.books)} books")  # Triggers query per author

# Good - Eager loading
authors = db.session.scalars(
    select(Author).options(selectinload(Author.books))
).all()
for author in authors:
    print(f"{author.name} has {len(author.books)} books")  # No additional queries
```

**ActiveRecord:**
```ruby
# Bad - N+1 queries
authors = Author.all
authors.each { |author| puts "#{author.name} has #{author.books.count} books" }

# Good - Eager loading
authors = Author.includes(:books)
authors.each { |author| puts "#{author.name} has #{author.books.size} books" }
```

### Batch Operations

**SQLAlchemy:**
```python
# Efficient bulk insert
users_data = [
    {'name': 'User 1', 'email': 'user1@example.com'},
    {'name': 'User 2', 'email': 'user2@example.com'},
    # ... more data
]
db.session.bulk_insert_mappings(User, users_data)
db.session.commit()
```

**ActiveRecord:**
```ruby
# Efficient bulk insert
users_data = [
  { name: 'User 1', email: 'user1@example.com' },
  { name: 'User 2', email: 'user2@example.com' },
  # ... more data
]
User.insert_all(users_data)
```

This comprehensive guide provides everything you need to understand and work with both SQLAlchemy and ActiveRecord effectively, including modern best practices and performance optimizations. 