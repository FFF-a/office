"""业务异常定义，供全局异常处理器捕获。"""


class BusinessException(Exception):
    """业务异常基类。"""

    def __init__(self, message: str, code: int = 400):
        self.message = message
        self.code = code
        super().__init__(message)


class BadRequestException(BusinessException):
    """参数校验失败 / 非法请求。"""

    def __init__(self, message: str = "请求参数错误"):
        super().__init__(message, code=400)


class UnauthorizedException(BusinessException):
    """未登录或令牌无效。"""

    def __init__(self, message: str = "未授权，请先登录"):
        super().__init__(message, code=401)


class NotFoundException(BusinessException):
    """资源不存在。"""

    def __init__(self, message: str = "资源不存在"):
        super().__init__(message, code=404)


class ConflictException(BusinessException):
    """资源冲突（如唯一键重复、分类下仍有设备）。"""

    def __init__(self, message: str = "资源冲突"):
        super().__init__(message, code=409)
