from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name')
    def validate_name(self, key, input):
        matching_name = Author.query.filter_by(name = input).first()
        if len(input) == 0 or matching_name:
            raise ValueError('Invalid name')
        return input
    
    @validates('phone_number')
    def validate_phone_number(self, key, input):
        accept = '123456789'
        status = True
        for character in input:
            if character not in accept:
                status = False
        if not len(input) == 10 or status == False:
            raise ValueError('Invalid phone number')
        return input

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators
    @validates('title')
    def validate_title(self, key, input):
        accepted = ['Won\'t Believe', 'Secret', 'Top', 'Guess']
        includes = False
        for item in accepted:
            if item in input:
                includes = True
        if includes == False:
            raise ValueError('Does not include key words')
        return input
    
    @validates('content')
    def validate_content(self, key, input):
        if len(input) < 250:
            raise ValueError('Too short')
        return input

    @validates('summary')
    def validate_summary(self, key, input):
        if len(input) > 250:
            raise ValueError('Too long')
        return input
    
    @validates('category')
    def validate_category(self, key, input):
        if input != 'Fiction' and input != 'Non-Fiction':
            raise ValueError('Must be fiction or non-fiction')
        return input

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
