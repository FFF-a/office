"""初始化默认管理员账号（首次部署运行一次）。"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv

load_dotenv()

from app import create_app
from app.models.admin import Admin
from app.service.admin_service import AdminService

DEFAULT_USERNAME = "admin"
DEFAULT_PASSWORD = "admin123"


def main():
    app = create_app()
    with app.app_context():
        existing = Admin.query.filter_by(username=DEFAULT_USERNAME).first()
        if existing:
            print(f"管理员 [{DEFAULT_USERNAME}] 已存在，跳过初始化")
            return
        AdminService.create_admin(DEFAULT_USERNAME, DEFAULT_PASSWORD)
        print(f"管理员创建成功: username={DEFAULT_USERNAME}, password={DEFAULT_PASSWORD}")
        print("请登录后立即修改密码！")


if __name__ == "__main__":
    main()
