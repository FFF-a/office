"""管理员登录业务逻辑。"""
from flask import current_app

from app.extensions import db
from app.models.admin import Admin
from app.utils.exceptions import BadRequestException, UnauthorizedException
from app.utils.jwt_helper import create_token
from app.utils.password import check_password, hash_password
from app.utils.validators import require_fields


class AdminService:
    """管理员认证服务。"""

    @staticmethod
    def login(data: dict) -> dict:
        """管理员登录，返回 JWT。"""
        require_fields(data, ["username", "password"])
        username = str(data["username"]).strip()
        password = data["password"]

        if not username or not password:
            raise BadRequestException("用户名和密码不能为空")

        admin = Admin.query.filter_by(username=username).first()
        if not admin or not check_password(password, admin.password_hash):
            raise UnauthorizedException("用户名或密码错误")

        token = create_token(admin.id, admin.username)
        return {
            "token": token,
            "expire_seconds": int(current_app.config["JWT_EXPIRE_SECONDS"]),
            "admin": admin.to_dict(),
        }

    @staticmethod
    def create_admin(username: str, password: str) -> Admin:
        """创建管理员（初始化脚本使用）。"""
        admin = Admin(username=username, password_hash=hash_password(password))
        db.session.add(admin)
        db.session.commit()
        return admin
