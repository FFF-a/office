"""员工（用户）业务逻辑。"""
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models.user import User
from app.utils.exceptions import BadRequestException, ConflictException, NotFoundException
from app.utils.validators import validate_age, validate_email_format, validate_name


class UserService:
    """员工 CRUD 服务。"""

    @staticmethod
    def list_users(page: int = 1, per_page: int = 10) -> dict:
        """分页列表。"""
        page = max(1, page)
        per_page = min(max(1, per_page), 100)
        pagination = User.query.order_by(User.id.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        return {
            "items": [u.to_dict() for u in pagination.items],
            "total": pagination.total,
            "page": page,
            "per_page": per_page,
            "pages": pagination.pages,
        }

    @staticmethod
    def get_user(user_id: int) -> User:
        user = User.query.get(user_id)
        if not user:
            raise NotFoundException("员工不存在")
        return user

    @staticmethod
    def create_user(data: dict) -> User:
        name = validate_name(data.get("name"))
        age = validate_age(data.get("age"))
        email = validate_email_format(data.get("email"))

        user = User(name=name, age=age, email=email)
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise ConflictException("邮箱已存在")
        return user

    @staticmethod
    def update_user(user_id: int, data: dict) -> User:
        user = UserService.get_user(user_id)

        if "name" in data and data["name"] is not None:
            user.name = validate_name(data["name"])
        if "age" in data and data["age"] is not None:
            user.age = validate_age(data["age"])
        if "email" in data and data["email"] is not None:
            user.email = validate_email_format(data["email"])

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise ConflictException("邮箱已存在")
        return user

    @staticmethod
    def delete_user(user_id: int) -> None:
        user = UserService.get_user(user_id)
        db.session.delete(user)
        db.session.commit()
