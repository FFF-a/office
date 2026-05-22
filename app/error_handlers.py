"""全局异常处理器。"""
from flask import Flask
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from werkzeug.exceptions import HTTPException

from app.utils.exceptions import BusinessException
from app.utils.response import fail


def register_error_handlers(app: Flask) -> None:
    """注册统一异常响应。"""

    @app.errorhandler(BusinessException)
    def handle_business(exc: BusinessException):
        return fail(message=exc.message, code=exc.code)

    @app.errorhandler(400)
    def handle_400(exc):
        message = getattr(exc, "description", "请求参数错误")
        return fail(message=message, code=400)

    @app.errorhandler(401)
    def handle_401(exc):
        message = getattr(exc, "description", "未授权")
        return fail(message=message, code=401)

    @app.errorhandler(404)
    def handle_404(exc):
        return fail(message="接口或资源不存在", code=404)

    @app.errorhandler(409)
    def handle_409(exc):
        message = getattr(exc, "description", "资源冲突")
        return fail(message=message, code=409)

    @app.errorhandler(IntegrityError)
    def handle_integrity(exc: IntegrityError):
        return fail(message="数据库约束冲突", code=409)

    @app.errorhandler(SQLAlchemyError)
    def handle_db(exc: SQLAlchemyError):
        app.logger.exception("数据库异常: %s", exc)
        return fail(message="数据库操作失败", code=500)

    @app.errorhandler(HTTPException)
    def handle_http(exc: HTTPException):
        return fail(message=exc.description, code=exc.code)

    @app.errorhandler(Exception)
    def handle_unknown(exc: Exception):
        app.logger.exception("未捕获异常: %s", exc)
        return fail(message="服务器内部错误", code=500)
