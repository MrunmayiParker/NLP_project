from app import db
from datetime import datetime, timezone
from sqlalchemy.schema import UniqueConstraint

class Paper(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    filepath = db.Column(db.String(500), nullable=False)
    upload_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    hash = db.Column(db.String(64), nullable=False)

    __table_args__ = (
        UniqueConstraint('hash', name='uq_paper_hash'),
    )
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship("User", backref=db.backref("papers", lazy=True))