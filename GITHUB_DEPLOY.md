# 后端 GitHub 自动化说明

仓库：https://github.com/FFF-a/office

## 已配置的 Workflow

| 文件 | 触发 | 作用 |
|------|------|------|
| `backend-ci.yml` | 每次 push / PR | 安装依赖、检查 Flask 能否启动 |
| `backend-deploy.yml` | push 到 main + 手动 | SSH 部署到云服务器（需配置 Secrets） |

## 你需要做的（一次性）

### 1. 把本目录代码推到 GitHub

```powershell
cd office_backend
git add .
git commit -m "ci: add GitHub Actions for backend"
git push origin main
```

若默认分支是 `master`，把上面 `main` 改成 `master`。

### 2. 若要自动部署到服务器

按 `deploy/README.md` 在 GitHub 添加 `DEPLOY_HOST` 等 Secrets。

未配置 `DEPLOY_HOST` 时，**Deploy 工作流会自动跳过**，不影响 CI。

### 3. 在服务器准备 `.env`

与本地相同，但不要提交到 Git。
