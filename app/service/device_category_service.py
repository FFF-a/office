"""设备分类业务逻辑。"""
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models.device import Device
from app.models.device_category import DeviceCategory
from app.utils.exceptions import BadRequestException, ConflictException, NotFoundException


class DeviceCategoryService:
    """设备分类 CRUD 服务。"""

    @staticmethod
    def list_categories() -> list:
        categories = DeviceCategory.query.order_by(DeviceCategory.id).all()
        return [c.to_dict(include_device_count=True) for c in categories]

    @staticmethod
    def get_category(category_id: int) -> DeviceCategory:
        category = DeviceCategory.query.get(category_id)
        if not category:
            raise NotFoundException("设备分类不存在")
        return category

    @staticmethod
    def create_category(data: dict) -> DeviceCategory:
        name = (data.get("name") or "").strip()
        if not name:
            raise BadRequestException("分类名称不能为空")
        if len(name) > 50:
            raise BadRequestException("分类名称不能超过 50 个字符")

        category = DeviceCategory(
            name=name,
            description=data.get("description"),
        )
        db.session.add(category)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise ConflictException("分类名称已存在")
        return category

    @staticmethod
    def update_category(category_id: int, data: dict) -> DeviceCategory:
        category = DeviceCategoryService.get_category(category_id)

        if "name" in data and data["name"] is not None:
            name = str(data["name"]).strip()
            if not name:
                raise BadRequestException("分类名称不能为空")
            category.name = name
        if "description" in data:
            category.description = data.get("description")

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise ConflictException("分类名称已存在")
        return category

    @staticmethod
    def delete_category(category_id: int) -> None:
        """分类下存在设备时禁止删除。"""
        category = DeviceCategoryService.get_category(category_id)
        device_count = Device.query.filter_by(category_id=category_id).count()
        if device_count > 0:
            raise ConflictException(
                f"该分类下仍有 {device_count} 台设备，无法删除"
            )
        db.session.delete(category)
        db.session.commit()
