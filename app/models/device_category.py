"""设备分类模型（一对多关联设备）。"""
from datetime import datetime

from app.extensions import db


class DeviceCategory(db.Model):
    """设备分类表。"""

    __tablename__ = "device_categories"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True, comment="分类名称")
    description = db.Column(db.String(255), nullable=True, comment="分类描述")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # 一对多：分类 -> 设备
    devices = db.relationship(
        "Device",
        back_populates="category",
        lazy="dynamic",
    )

    def to_dict(self, include_device_count: bool = False) -> dict:
        data = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
        if include_device_count:
            data["device_count"] = self.devices.count()
        return data
