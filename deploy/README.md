# 后端服务器部署说明

## GitHub Actions 自动部署（SSH）

在仓库 **Settings → Secrets and variables → Actions** 添加：

| Secret | 示例 | 说明 |
|--------|------|------|
| `DEPLOY_HOST` | `123.45.67.89` | 服务器公网 IP |
| `DEPLOY_USER` | `root` | SSH 用户名 |
| `DEPLOY_SSH_KEY` | `-----BEGIN OPENSSH...` | 私钥全文 |
| `DEPLOY_PATH` | `/opt/office_backend` | 代码目录 |
| `DEPLOY_PORT` | `22` | 可选，默认 22 |

服务器上需提前：

1. 安装 Python 3.11+、MySQL，执行 `init_db.sql`
2. 在 `DEPLOY_PATH` 创建 `.env`（不要提交到 Git）
3. 开放防火墙 **5000** 端口

推送 `main` 分支后 workflow `Backend Deploy` 会自动执行。

## Docker 手动运行

```bash
docker build -t office-backend .
docker run -d -p 5000:5000 --env-file .env office-backend
```
