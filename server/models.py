from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
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
    def nam(self,key,name):
        if not name.strip():
            raise ValueError('Name is required')
        existing_a=Author.query.filter(Author.name == name).first()
        if existing_a:
            raise ValueError('Two authors cannnot have the same name')
        return name
    
    
    #@staticmethod
    #def create_author(name,phone_number=None):
    #    try:
    #        author=Author(name=name,phone_number=phone_number)
    #        db.session.add(author)
    #        db.session.commit()
    #        return author
    #    except IntegrityError:
    #        db.session.rollback()
    #        raise ValueError(f'author with name {name} already registered ')


   
    @validates('phone_number')
    def number(self,key,value):
        if len(value) != 10:
            raise ValueError('phone number must have exactly 10 digits')
        if not value.isdigit():
            raise ValueError('must be int')
        return value
    
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
    def titl(self,key,title):
        clickbait=["Won't Believe",'Secret','Top','Guess']
        if not title:
            raise ValueError('must have a title') 
        if not any(bait in title for bait in clickbait):
            raise ValueError('Must contain a clickbait')
        
    @validates('content')
    def cont(self,key,content):
        if len(content) < 250:
            raise ValueError('Must be at least 250 chatacters')
        return content
    
    @validates('summary')
    def summ(self,key,summary):
        if len(summary) > 250:
            raise ValueError('summary must be longer than 250 chars')
        
    @validates('category')
    def catgory(self,key,category):
        valid_category=['Fiction','Non-Fiction']
        if category not in valid_category:
            raise ValueError('category must be either Fiction or Non-Fiction')

   

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
