"""员工管理 RESTful 接口。"""
from flask import request
from flask_restful import Resource

from app.service.user_service import UserService
from app.utils.response import success


class UserListResource(Resource):
    """GET /api/users  POST /api/users"""

    def get(self):
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)
        data = UserService.list_users(page=page, per_page=per_page)
        return success(data=data, message="查询成功")

    def post(self):
        data = request.get_json(silent=True) or {}
        user = UserService.create_user(data)
        return success(data=user.to_dict(), message="创建成功", code=200)


class UserDetailResource(Resource):
    """GET/PUT/DELETE /api/users/<id>"""

    def get(self, user_id: int):
        user = UserService.get_user(user_id)
        return success(data=user.to_dict(), message="查询成功")

    def put(self, user_id: int):
        data = request.get_json(silent=True) or {}
        user = UserService.update_user(user_id, data)
        return success(data=user.to_dict(), message="更新成功")

    def delete(self, user_id: int):
        UserService.delete_user(user_id)
        return success(data=None, message="删除成功")
