"""设备分类 RESTful 接口。"""
from flask import request
from flask_restful import Resource

from app.service.device_category_service import DeviceCategoryService
from app.utils.response import success


class DeviceCategoryListResource(Resource):
    """GET /api/device-categories  POST /api/device-categories"""

    def get(self):
        items = DeviceCategoryService.list_categories()
        return success(data=items, message="查询成功")

    def post(self):
        data = request.get_json(silent=True) or {}
        category = DeviceCategoryService.create_category(data)
        return success(data=category.to_dict(), message="创建成功")


class DeviceCategoryDetailResource(Resource):
    """GET/PUT/DELETE /api/device-categories/<id>"""

    def get(self, category_id: int):
        category = DeviceCategoryService.get_category(category_id)
        return success(
            data=category.to_dict(include_device_count=True),
            message="查询成功",
        )

    def put(self, category_id: int):
        data = request.get_json(silent=True) or {}
        category = DeviceCategoryService.update_category(category_id, data)
        return success(data=category.to_dict(), message="更新成功")

    def delete(self, category_id: int):
        DeviceCategoryService.delete_category(category_id)
        return success(data=None, message="删除成功")
