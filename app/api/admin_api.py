"""管理员登录接口。"""
from flask import request
from flask_restful import Resource

from app.service.admin_service import AdminService
from app.utils.response import success


class AdminLoginResource(Resource):
    """POST /api/admin/login — 无需 JWT。"""

    def post(self):
        data = request.get_json(silent=True) or {}
        result = AdminService.login(data)
        return success(data=result, message="登录成功")
