"""设备管理业务逻辑（含联表查询）。"""
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

from app.extensions import db
from app.models.device import Device
from app.models.device_category import DeviceCategory
from app.utils.exceptions import BadRequestException, ConflictException, NotFoundException


class DeviceService:
    """设备 CRUD 服务。"""

    @staticmethod
    def list_devices(
        page: int = 1,
        per_page: int = 10,
        category_id: int = None,
        with_category: bool = True,
    ) -> dict:
        """设备列表，支持按分类筛选与联表查询。"""
        page = max(1, page)
        per_page = min(max(1, per_page), 100)

        query = Device.query
        if with_category:
            query = query.options(joinedload(Device.category))
        if category_id is not None:
            query = query.filter(Device.category_id == category_id)

        query = query.order_by(Device.id.desc())
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        return {
            "items": [
                d.to_dict(include_category=with_category) for d in pagination.items
            ],
            "total": pagination.total,
            "page": page,
            "per_page": per_page,
            "pages": pagination.pages,
        }

    @staticmethod
    def get_device(device_id: int, with_category: bool = True) -> Device:
        """单条查询，联表加载分类信息。"""
        query = Device.query
        if with_category:
            query = query.options(joinedload(Device.category))
        device = query.filter(Device.id == device_id).first()
        if not device:
            raise NotFoundException("设备不存在")
        return device

    @staticmethod
    def _validate_category(category_id) -> int:
        if category_id is None:
            raise BadRequestException("设备分类不能为空")
        category = DeviceCategory.query.get(category_id)
        if not category:
            raise NotFoundException("设备分类不存在")
        return category_id

    @staticmethod
    def create_device(data: dict) -> Device:
        name = (data.get("name") or "").strip()
        if not name:
            raise BadRequestException("设备名称不能为空")

        category_id = DeviceService._validate_category(data.get("category_id"))
        status = (data.get("status") or "available").strip()

        device = Device(
            name=name,
            model=data.get("model"),
            serial_number=data.get("serial_number"),
            status=status,
            category_id=category_id,
        )
        db.session.add(device)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise ConflictException("设备序列号已存在")
        return DeviceService.get_device(device.id)

    @staticmethod
    def update_device(device_id: int, data: dict) -> Device:
        device = Device.query.get(device_id)
        if not device:
            raise NotFoundException("设备不存在")

        if "name" in data and data["name"] is not None:
            name = str(data["name"]).strip()
            if not name:
                raise BadRequestException("设备名称不能为空")
            device.name = name
        if "model" in data:
            device.model = data.get("model")
        if "serial_number" in data:
            device.serial_number = data.get("serial_number")
        if "status" in data and data["status"] is not None:
            device.status = str(data["status"]).strip()
        if "category_id" in data and data["category_id"] is not None:
            device.category_id = DeviceService._validate_category(data["category_id"])

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise ConflictException("设备序列号已存在")
        return DeviceService.get_device(device.id)

    @staticmethod
    def delete_device(device_id: int) -> None:
        device = Device.query.get(device_id)
        if not device:
            raise NotFoundException("设备不存在")
        db.session.delete(device)
        db.session.commit()
