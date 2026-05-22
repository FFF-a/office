"""员工（用户）模型。"""
from datetime import datetime

from app.extensions import db


class User(db.Model):
    """员工表。"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False, comment="姓名")
    age = db.Column(db.Integer, nullable=False, comment="年龄")
    email = db.Column(db.String(120), nullable=False, unique=True, comment="邮箱")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "email": self.email,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
