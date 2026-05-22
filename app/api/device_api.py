"""设备管理 RESTful 接口（支持联表查询）。"""
from flask import request
from flask_restful import Resource

from app.service.device_service import DeviceService
from app.utils.response import success


class DeviceListResource(Resource):
    """GET /api/devices  POST /api/devices"""

    def get(self):
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)
        category_id = request.args.get("category_id", type=int)
        with_category = request.args.get("with_category", "1") != "0"

        data = DeviceService.list_devices(
            page=page,
            per_page=per_page,
            category_id=category_id,
            with_category=with_category,
        )
        return success(data=data, message="查询成功")

    def post(self):
        data = request.get_json(silent=True) or {}
        device = DeviceService.create_device(data)
        return success(data=device.to_dict(include_category=True), message="创建成功")


class DeviceDetailResource(Resource):
    """GET/PUT/DELETE /api/devices/<id>"""

    def get(self, device_id: int):
        device = DeviceService.get_device(device_id, with_category=True)
        return success(
            data=device.to_dict(include_category=True),
            message="查询成功",
        )

    def put(self, device_id: int):
        data = request.get_json(silent=True) or {}
        device = DeviceService.update_device(device_id, data)
        return success(
            data=device.to_dict(include_category=True),
            message="更新成功",
        )

    def delete(self, device_id: int):
        DeviceService.delete_device(device_id)
        return success(data=None, message="删除成功")
