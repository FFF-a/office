#!/bin/bash
# 阿里云 ECS 首次初始化（Ubuntu 22.04/24.04）
# 用法：以 root 登录 ECS 后执行
#   curl -fsSL https://raw.githubusercontent.com/FFF-a/office/main/deploy/aliyun-ecs-setup.sh | bash
# 或上传本文件后：bash aliyun-ecs-setup.sh

set -e

DEPLOY_PATH="${DEPLOY_PATH:-/opt/office_backend}"
REPO_URL="${REPO_URL:-https://github.com/FFF-a/office.git}"
BRANCH="${BRANCH:-main}"

echo "==> 安装系统依赖..."
export DEBIAN_FRONTEND=noninteractive
apt-get update -y
apt-get install -y python3 python3-venv python3-pip git mysql-server curl

echo "==> 启动 MySQL..."
systemctl enable mysql
systemctl start mysql

echo "==> 克隆代码到 ${DEPLOY_PATH}..."
mkdir -p "$(dirname "$DEPLOY_PATH")"
if [ ! -d "$DEPLOY_PATH/.git" ]; then
  git clone -b "$BRANCH" "$REPO_URL" "$DEPLOY_PATH"
else
  echo "目录已存在，跳过 clone"
fi

cd "$DEPLOY_PATH"

if [ ! -f .env ]; then
  echo "==> 创建 .env（请稍后修改密码与密钥）..."
  cp deploy/env.production.example .env
  sed -i 's/请改成随机长字符串/office_prod_secret_'$(date +%s)'/g' .env
  echo "!!! 请编辑 ${DEPLOY_PATH}/.env 设置 DB_PASSWORD 等 !!!"
fi

echo "==> Python 虚拟环境与依赖..."
python3 -m venv venv
./venv/bin/pip install -r requirements.txt -q

echo "==> 初始化数据库（若尚未执行）..."
if command -v mysql &>/dev/null; then
  mysql -u root < init_db.sql 2>/dev/null || sudo mysql < init_db.sql || true
fi
./venv/bin/python scripts/init_admin.py || true

echo "==> 安装 systemd 服务..."
cp deploy/office-backend.service /etc/systemd/system/office-backend.service
systemctl daemon-reload
systemctl enable office-backend
systemctl restart office-backend

echo "==> 本机健康检查..."
sleep 2
curl -sf http://127.0.0.1:5000/health && echo "" || echo "健康检查失败，请查看 journalctl -u office-backend"

echo ""
echo "============================================"
echo " ECS 初始化完成"
echo " 代码目录: ${DEPLOY_PATH}"
echo " 下一步:"
echo "  1. 阿里云安全组放行 TCP 22、5000"
echo "  2. 编辑 .env 中的 DB_PASSWORD"
echo "  3. 在 GitHub 配置 Actions Secrets 见 deploy/ALIYUN_ECS.md"
echo "============================================"
