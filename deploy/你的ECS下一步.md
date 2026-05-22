# 你的 ECS 信息（按截图）

| 项目 | 值 |
|------|-----|
| 公网 IP | **118.31.109.161** |
| 系统 | Alibaba Cloud Linux 3 |
| 私网 IP | 172.22.125.56 |
| 已放行端口 | 22, 80, 3001, **8000** |

## 重要：API 端口

Flask 默认 **5000**，你安全组**还没开 5000**。

**二选一：**

1. **推荐**：安全组 → 入方向 → 添加 **TCP 5000** / 0.0.0.0/0  
2. 或用已开放的 **8000**：初始化时执行  
   `API_PORT=8000 bash aliyun-ecs-setup-alinux.sh`

---

## 第 1 步：SSH 登录 ECS

```powershell
ssh -i 你的密钥.pem root@118.31.109.161
```

（用户名也可能是 `ecs-user`，以控制台为准）

---

## 第 2 步：首次初始化（在 ECS 上执行）

把本地的 `deploy/aliyun-ecs-setup-alinux.sh` 上传到服务器，或 push 代码后：

```bash
cd /opt
git clone https://github.com/FFF-a/office.git office_backend
cd office_backend
bash deploy/aliyun-ecs-setup-alinux.sh
```

编辑数据库密码：

```bash
vi /opt/office_backend/.env
# 改 DB_PASSWORD=你的MySQL密码
systemctl restart office-backend
```

浏览器测试：

```
http://118.31.109.161:5000/health
```

（若用 8000 端口则改成 :8000）

---

## 第 3 步：GitHub Secrets

仓库 https://github.com/FFF-a/office → Settings → Secrets：

| Secret | 值 |
|--------|-----|
| DEPLOY_HOST | `118.31.109.161` |
| DEPLOY_USER | `root` |
| DEPLOY_SSH_KEY | 你的 .pem 私钥全文 |
| DEPLOY_PATH | `/opt/office_backend` |

---

## 第 4 步：本机 push 触发自动部署

```powershell
cd office_backend
git push origin main
```

Actions 里看 **Backend Deploy to Aliyun ECS**。

---

## 第 5 步：前端 APK 改公网地址

```
EXPO_PUBLIC_API_URL=http://118.31.109.161:5000
```

（端口与 ECS 上一致）

重新 eas build 或 push office-mobile 仓库。
