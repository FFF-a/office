# Office Backend — 人工专高复赛考题

Python Flask + Flask-RESTful + Flask-SQLAlchemy + MySQL 8.0 后端。

## 项目结构

```
office_backend/
├── app/
│   ├── __init__.py          # 应用工厂、路由注册
│   ├── config.py            # 环境变量配置
│   ├── extensions.py      # SQLAlchemy 实例
│   ├── error_handlers.py    # 全局异常处理
│   ├── models/              # ORM 模型层
│   ├── service/             # 业务逻辑层
│   ├── api/                 # RESTful 接口层
│   ├── middleware/          # 日志 + JWT 守卫
│   └── utils/               # 响应、校验、JWT、密码
├── scripts/
│   └── init_admin.py        # 初始化管理员
├── logs/                    # API 日志（自动创建）
├── init_db.sql              # MySQL 建表脚本
├── requirements.txt
├── .env.example
└── run.py
```

## 快速启动

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
copy .env.example .env
# 编辑 .env，填写 MySQL 与 JWT_SECRET
```

### 3. 初始化数据库

```bash
mysql -u root -p < init_db.sql
python scripts/init_admin.py
```

默认管理员：`admin` / `admin123`

### 4. 启动服务

```bash
python run.py
```

健康检查：`GET http://127.0.0.1:5000/health`

## API 说明

除 `POST /api/admin/login` 外，所有 `/api/*` 接口需在 Header 携带：

```
Authorization: Bearer <token>
```

### 管理员登录

`POST /api/admin/login`

```json
{"username": "admin", "password": "admin123"}
```

### 员工 CRUD

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/users | 分页列表 ?page=1&per_page=10 |
| POST | /api/users | 创建 |
| GET | /api/users/:id | 详情 |
| PUT | /api/users/:id | 更新 |
| DELETE | /api/users/:id | 删除 |

创建/更新校验：姓名 1-20 字符、年龄 18-60、邮箱格式。

### 设备分类

| 方法 | 路径 |
|------|------|
| GET/POST | /api/device-categories |
| GET/PUT/DELETE | /api/device-categories/:id |

分类下仍有设备时 `DELETE` 返回 409。

### 设备管理（联表）

| 方法 | 路径 |
|------|------|
| GET/POST | /api/devices |
| GET/PUT/DELETE | /api/devices/:id |

`GET /api/devices?category_id=1&with_category=1` 联表返回分类信息。

## 统一响应格式

```json
{"code": 200, "message": "操作成功", "data": {}}
```

业务错误码：400 / 401 / 404 / 409 / 500

## 日志

所有 `/api/` 请求自动记录：时间、方法、URL、IP、状态码、耗时（ms），输出至控制台与 `logs/api.log`。
