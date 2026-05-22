"""数据校验工具。"""
import re

from email_validator import EmailNotValidError, validate_email

from app.utils.exceptions import BadRequestException

NAME_PATTERN = re.compile(r"^[^\s].{0,19}$")  # 1-20 字符，首尾不能是空白


def validate_name(name) -> str:
    """姓名：1-20 字符，非空（去除首尾空白后校验）。"""
    if name is None:
        raise BadRequestException("姓名不能为空")
    name = str(name).strip()
    if not name or len(name) > 20:
        raise BadRequestException("姓名必须为 1-20 个字符且不能为空")
    if not NAME_PATTERN.match(name):
        raise BadRequestException("姓名格式不正确")
    return name


def validate_age(age) -> int:
    """年龄：18-60 整数。"""
    if age is None:
        raise BadRequestException("年龄不能为空")
    try:
        age = int(age)
    except (TypeError, ValueError):
        raise BadRequestException("年龄必须为整数")
    if age < 18 or age > 60:
        raise BadRequestException("年龄必须在 18-60 之间")
    return age


def validate_email_format(email) -> str:
    """邮箱格式校验。"""
    if email is None or not str(email).strip():
        raise BadRequestException("邮箱不能为空")
    email = str(email).strip()
    try:
        valid = validate_email(email, check_deliverability=False)
        return valid.normalized
    except EmailNotValidError:
        raise BadRequestException(
            "邮箱格式不正确，请填写有效邮箱，如 zhangsan@company.com"
        )


def require_fields(data: dict, fields: list) -> None:
    """检查必填字段是否存在。"""
    if not data:
        raise BadRequestException("请求体不能为空")
    missing = [f for f in fields if f not in data or data[f] in (None, "")]
    if missing:
        raise BadRequestException(f"缺少必填字段: {', '.join(missing)}")
