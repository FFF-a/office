"""JWT 路由守卫：保护需要管理员身份的接口。"""
from functools import wraps

from flask import g, request

from app.utils.exceptions import UnauthorizedException
from app.utils.jwt_helper import decode_token


# 无需 JWT 的白名单路径（登录接口）
PUBLIC_PATHS = {
    "/api/admin/login",
}


def jwt_required(f):
    """
    装饰器：校验 Authorization: Bearer <token>。
    校验通过后将 admin_id、username 写入 g。
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        if request.path in PUBLIC_PATHS:
            return f(*args, **kwargs)

        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            raise UnauthorizedException("请在 Header 中携带 Bearer Token")

        token = auth_header[7:].strip()
        if not token:
            raise UnauthorizedException("令牌不能为空")

        payload = decode_token(token)
        g.admin_id = payload.get("sub")
        g.username = payload.get("username")
        return f(*args, **kwargs)

    return decorated


def register_auth_guard(app):
    """为所有 /api/ 路由（除白名单）注册全局 before_request 守卫。"""

    @app.before_request
    def _check_jwt():
        # 浏览器 CORS 预检不带 Token，必须放行
        if request.method == "OPTIONS":
            return None

        path = request.path

        # 非 API 或公开路径跳过
        if not path.startswith("/api/"):
            return None
        if path in PUBLIC_PATHS:
            return None

        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            raise UnauthorizedException("请在 Header 中携带 Bearer Token")

        token = auth_header[7:].strip()
        payload = decode_token(token)
        g.admin_id = payload.get("sub")
        g.username = payload.get("username")
        return None
