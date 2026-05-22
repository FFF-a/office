"""管理员模型。"""
from datetime import datetime

from app.extensions import db


class Admin(db.Model):
    """管理员表。"""

    __tablename__ = "admins"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True, comment="用户名")
    password_hash = db.Column(db.String(128), nullable=False, comment="bcrypt 密码哈希")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
