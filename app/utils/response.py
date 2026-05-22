"""统一接口响应格式：{code, message, data}。"""
from flask import jsonify


def success(data=None, message: str = "操作成功", code: int = 200):
    """成功响应（供 Flask-RESTful Resource 返回，由框架序列化为 JSON）。"""
    return {"code": code, "message": message, "data": data}, 200


def fail(message: str, code: int, data=None):
    """失败响应（HTTP 状态码与业务 code 保持一致）。"""
    return jsonify({"code": code, "message": message, "data": data}), code
