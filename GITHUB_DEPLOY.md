# 后端 GitHub 自动化部署

## 阿里云 ECS（推荐）

完整步骤见：**[deploy/ALIYUN_ECS.md](deploy/ALIYUN_ECS.md)**

简要流程：

1. 阿里云买 ECS（Ubuntu）+ 安全组放行 **22、5000**
2. SSH 登录，运行 `deploy/aliyun-ecs-setup.sh` 初始化
3. GitHub 仓库 `FFF-a/office` 配置 Secrets：`DEPLOY_HOST`、`DEPLOY_USER`、`DEPLOY_SSH_KEY`、`DEPLOY_PATH`
4. `git push` → Actions 自动 `git pull` + 重启服务

## Workflows

| 文件 | 作用 |
|------|------|
| `backend-ci.yml` | 每次 push 检查 Flask 能否加载 |
| `backend-deploy.yml` | push 后部署到 ECS（需 Secrets） |

## API 地址

部署成功后：

```
http://<ECS公网IP>:5000
```

健康检查：`/health`  
登录：`POST /api/admin/login`
