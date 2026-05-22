"""设备模型（多对一关联分类）。"""
from datetime import datetime

from app.extensions import db


class Device(db.Model):
    """设备表。"""

    __tablename__ = "devices"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, comment="设备名称")
    model = db.Column(db.String(100), nullable=True, comment="设备型号")
    serial_number = db.Column(db.String(100), nullable=True, unique=True, comment="序列号")
    status = db.Column(
        db.String(20), nullable=False, default="available", comment="状态"
    )
    category_id = db.Column(
        db.Integer,
        db.ForeignKey("device_categories.id", ondelete="RESTRICT"),
        nullable=False,
        comment="所属分类 ID",
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    category = db.relationship("DeviceCategory", back_populates="devices")

    def to_dict(self, include_category: bool = False) -> dict:
        data = {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "serial_number": self.serial_number,
            "status": self.status,
            "category_id": self.category_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
        if include_category and self.category:
            data["category"] = self.category.to_dict()
        return data
