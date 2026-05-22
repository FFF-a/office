"""Flask 应用工厂。"""
from flask import Flask, jsonify
from flask_cors import CORS
from flask_restful import Api

from app.api.admin_api import AdminLoginResource
from app.api.device_api import DeviceDetailResource, DeviceListResource
from app.api.device_category_api import (
    DeviceCategoryDetailResource,
    DeviceCategoryListResource,
)
from app.api.user_api import UserDetailResource, UserListResource
from app.config import Config
from app.error_handlers import register_error_handlers
from app.extensions import db
from app.middleware.auth_middleware import register_auth_guard
from app.middleware.logging_middleware import register_logging_middleware


def create_app(config_class=Config) -> Flask:
    """创建并配置 Flask 应用。"""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 开发环境跨域：允许浏览器 / Expo Web 携带 Authorization 访问 API
    CORS(
        app,
        resources={r"/api/*": {"origins": "*"}},
        supports_credentials=False,
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    )

    db.init_app(app)

    register_error_handlers(app)
    register_logging_middleware(app)
    register_auth_guard(app)

    api = Api(app, prefix="/api")

    # 管理员登录（公开）
    api.add_resource(AdminLoginResource, "/admin/login")

    # 员工管理
    api.add_resource(UserListResource, "/users")
    api.add_resource(UserDetailResource, "/users/<int:user_id>")

    # 设备分类
    api.add_resource(DeviceCategoryListResource, "/device-categories")
    api.add_resource(
        DeviceCategoryDetailResource, "/device-categories/<int:category_id>"
    )

    # 设备管理
    api.add_resource(DeviceListResource, "/devices")
    api.add_resource(DeviceDetailResource, "/devices/<int:device_id>")

    @app.route("/health")
    def health():
        return jsonify({"code": 200, "message": "ok", "data": {"status": "up"}})

    return app
