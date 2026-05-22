"""密码 bcrypt 加密与校验。"""
import bcrypt


def hash_password(plain: str) -> str:
    """使用 bcrypt 加密密码。"""
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def check_password(plain: str, hashed: str) -> bool:
    """校验明文密码与哈希是否匹配。"""
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
