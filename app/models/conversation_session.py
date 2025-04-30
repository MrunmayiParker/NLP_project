from app import db #change
from datetime import datetime, timezone
import uuid

class ConversationSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), nullable=False, default=lambda: str(uuid.uuid4()), unique=True)
    session_name = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Optional: relationship back to conversations
    conversations = db.relationship('Conversation', backref='session', lazy=True)
