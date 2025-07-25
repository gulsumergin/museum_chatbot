from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()

class Message(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    age = db.Column(db.Integer)  # <-- yaş alanını ekledik
    artwork = db.Column(db.String(120))
    sender = db.Column(db.String(10))  # 'user' or 'bot'
    text = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Message {self.username} - {self.sender}>'
