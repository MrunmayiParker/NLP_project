from app import db
from datetime import datetime, timezone

class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    userid = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    paperid = db.Column(db.Integer, db.ForeignKey("paper.id"), nullable=False)