from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Author name must be provided")
        
        existing_author = Author.query.filter_by(name=name).first()
        if existing_author and existing_author.id != self.id:
            raise ValueError("An author with this name already exists.")
        
        return name
    
    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if not phone_number:
            raise ValueError("Phone number must be provided")
        if not phone_number.isdigit() or len(phone_number) != 10:
            raise ValueError("Phone number must be exactly ten digits")
        return phone_number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String(250))
    category = db.Column(db.String)
    summary = db.Column(db.String(250))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates('category')
    def validate_category(self, key, category):
        if category not in ['Fiction' , 'Non-Fiction']:
            raise ValueError("category must either be Fiction or Non-Fiction")
        return category
    
    @validates('title')
    def validate_title(self, key, title):
        clickbait_keywords = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(keyword in title for keyword in clickbait_keywords):
            raise ValueError("Post title must be sufficiently clickbait-y and contain one of the following: 'Won't Believe', 'Secret', 'Top', 'Guess'")
        return title

    @validates('content')
    def validate_content(self, key, content):
        if len(content) < 250:
            raise ValueError("Post content must be at least 250 characters long")
        return content
    
    @validates('summary')
    def validate_summary(self, key, summary):
        if len(summary) > 250:
            raise ValueError("Post summary cannot exceed 250 characters")
        return summary

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
