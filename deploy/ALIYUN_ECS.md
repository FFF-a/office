# GitHub Actions + 阿里云 ECS 自动部署指南

## 架构

```
开发者 git push (main)
        ↓
GitHub Actions (Backend Deploy)
        ↓ SSH
阿里云 ECS (/opt/office_backend)
        ↓
Flask :5000  +  MySQL (本机)
        ↓
手机 APK / 浏览器 访问 http://ECS公网IP:5000
```

---

## 一、购买与配置 ECS（阿里云控制台）

### 1. 创建 ECS

- **地域**：选离用户近的（如华东）
- **镜像**：Ubuntu 22.04 64 位
- **规格**：2 核 2G 起（比赛够用）
- **公网 IP**：分配弹性公网 IP
- **登录**：推荐 **密钥对**（下载 `.pem`）

### 2. 安全组（必做）

入方向放行：

| 端口 | 协议 | 授权对象 | 说明 |
|------|------|----------|------|
| 22 | TCP | 0.0.0.0/0 或你的 IP | SSH |
| 5000 | TCP | 0.0.0.0/0 | Flask API |

> 生产环境建议 5000 仅内网，前面加 Nginx 443；比赛演示可直接开 5000。

### 3. 首次登录 ECS

Windows PowerShell（密钥示例）：

```powershell
ssh -i C:\path\to\your.pem root@你的ECS公网IP
```

---

## 二、ECS 上一键初始化（仅第一次）

登录 ECS 后执行：

```bash
export DEPLOY_PATH=/opt/office_backend
curl -fsSL https://raw.githubusercontent.com/FFF-a/office/main/deploy/aliyun-ecs-setup.sh -o setup.sh
bash setup.sh
```

或手动上传 `deploy/aliyun-ecs-setup.sh` 后执行。

然后**务必**编辑：

```bash
nano /opt/office_backend/.env
# 修改 DB_PASSWORD、SECRET_KEY、JWT_SECRET
systemctl restart office-backend
```

验证：

```bash
curl http://127.0.0.1:5000/health
```

浏览器访问：`http://ECS公网IP:5000/health`

---

## 三、GitHub 配置 Secrets

仓库：https://github.com/FFF-a/office  
**Settings → Secrets and variables → Actions → New repository secret**

| Secret 名称 | 填什么 |
|-------------|--------|
| `DEPLOY_HOST` | ECS **公网 IP** |
| `DEPLOY_USER` | `root`（或你的 SSH 用户） |
| `DEPLOY_SSH_KEY` | `.pem` 私钥**全文**（`-----BEGIN...` 到 `-----END...`） |
| `DEPLOY_PATH` | `/opt/office_backend` |
| `DEPLOY_PORT` | `22`（可选） |

### 私钥怎么填进 GitHub

1. 记事本打开下载的 `.pem`，全选复制  
2. 粘贴到 `DEPLOY_SSH_KEY` Secret 里保存  

---

## 四、自动部署如何触发

- 向 `main` 分支 **push** 代码 → 自动运行 **Backend Deploy**  
- 或 GitHub **Actions** → **Backend Deploy** → **Run workflow**

Workflow 会在 ECS 上执行：

1. `git pull` 拉最新代码  
2. `pip install` 更新依赖  
3. `systemctl restart office-backend`  

查看日志：GitHub Actions 页面 / ECS 上 `journalctl -u office-backend -f`

---

## 五、前端 APK 指向 ECS

手机不能访问 `172.20.10.10` 局域网地址时，需改 API 为 ECS 公网：

**office_mobile/.env` 或 EAS Secrets：**

```
EXPO_PUBLIC_API_URL=http://你的ECS公网IP:5000
```

然后重新 `eas build` 或在 **office-mobile** 仓库配置 GitHub Secret `EXPO_PUBLIC_API_URL` 后 push 触发自动打包。

---

## 六、常见问题

| 现象 | 处理 |
|------|------|
| Actions SSH 连不上 | 检查安全组 22、密钥是否完整、DEPLOY_HOST 是否正确 |
| health 不通 | `systemctl status office-backend`；MySQL 是否启动；`.env` 数据库密码 |
| 外网访问不了 5000 | 安全组是否放行 5000；`FLASK_HOST=0.0.0.0` |
| git pull 失败 | ECS 能否访问 GitHub；仓库是否公开 |

---

## 七、可选：仅 CI 不部署

不配置 `DEPLOY_HOST` 时，只运行 **Backend CI**，不会 SSH 部署。
