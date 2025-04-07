from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class Episode(db.Model,SerializerMixin):
    __tablename__ = 'episodes'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, nullable=False)
    number = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Episode {self.number}>'

class Appearance(db.Model,SerializerMixin):
    __tablename__ = 'appearances'
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    episode_id = db.Column(db.Integer, db.ForeignKey('episodes.id'), nullable=False)
    guest_id = db.Column(db.Integer, db.ForeignKey('guests.id'), nullable=False)

    #  relationships with cascade defined in backref
    episode = db.relationship('Episode', backref=db.backref('appearances', lazy=True, cascade="all, delete-orphan"))
    guest = db.relationship('Guest')  

    @validates('rating')
    def validate_rating(self, key, rating):
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5.")
        return rating

    def __repr__(self):
        return f'<Appearance Rating: {self.rating} in Episode {self.episode.date}>'

class Guest(db.Model,SerializerMixin):
    __tablename__ = 'guests'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    occupation = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Guest {self.name}>'
