from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

# Create the database object (we'll connect it to Flask later)
db = SQLAlchemy()

class User(db.Model):
    # __tablename__ tells SQLAlchemy what to name the table
    __tablename__ = 'users'

    # Define columns
    id = db.Column(db.Integer, primary_key=True) # ID auto increments
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # convert a User to JSON
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at
        }

# - `id`: Primary key!, auto-increments (1, 2, 3...)
# - `username`: String up to 80 chars, must be unique, can't be null
# - `email`: String up to 120 chars, must be unique, can't be null
# - `created_at`: Timestamp, automatically set when user is created
# - `to_dict()`: Helper method to convert User object to a dictionary (for JSON responses)