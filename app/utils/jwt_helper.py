"""JWT 令牌生成与解析。"""
from datetime import datetime, timezone

import jwt
from flask import current_app

from app.utils.exceptions import UnauthorizedException


def create_token(admin_id: int, username: str) -> str:
    """签发 JWT，默认 2 小时过期。"""
    now = datetime.now(timezone.utc)
    expire_delta = current_app.config["JWT_EXPIRE_DELTA"]
    payload = {
        "sub": admin_id,
        "username": username,
        "iat": now,
        "exp": now + expire_delta,
    }
    return jwt.encode(
        payload,
        current_app.config["JWT_SECRET"],
        algorithm="HS256",
    )


def decode_token(token: str) -> dict:
    """解析并校验 JWT。"""
    try:
        return jwt.decode(
            token,
            current_app.config["JWT_SECRET"],
            algorithms=["HS256"],
        )
    except jwt.ExpiredSignatureError:
        raise UnauthorizedException("令牌已过期，请重新登录")
    except jwt.InvalidTokenError:
        raise UnauthorizedException("无效的令牌")
