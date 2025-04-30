# change
from app import db 
from datetime import datetime, timezone
import uuid

class Conversation(db.Model):
    qid = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    # conversation_id = db.Column(db.Integer, nullable = False) 

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    paper_id = db.Column(db.Integer, db.ForeignKey("paper.id"), nullable=False)
    session_id = db.Column(db.String(100), db.ForeignKey("conversation_session.session_id"), nullable=False)  # <-- New
    