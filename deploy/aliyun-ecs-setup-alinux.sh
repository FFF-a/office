#!/bin/bash
# 阿里云 ECS 首次初始化（Alibaba Cloud Linux 3）
# 以 root 登录后：bash aliyun-ecs-setup-alinux.sh

set -e

DEPLOY_PATH="${DEPLOY_PATH:-/opt/office_backend}"
REPO_URL="${REPO_URL:-https://github.com/FFF-a/office.git}"
BRANCH="${BRANCH:-main}"
# 安全组已放行 8000 时可改为 8000；推荐再添加 5000 规则
API_PORT="${API_PORT:-5000}"

echo "==> 安装系统依赖 (dnf)..."
dnf install -y python3 python3-pip python3-devel git gcc openssl-devel \
  mariadb-server mariadb curl

echo "==> 启动 MariaDB/MySQL..."
systemctl enable mariadb
systemctl start mariadb

echo "==> 克隆代码到 ${DEPLOY_PATH}..."
mkdir -p "$(dirname "$DEPLOY_PATH")"
if [ ! -d "$DEPLOY_PATH/.git" ]; then
  git clone -b "$BRANCH" "$REPO_URL" "$DEPLOY_PATH"
fi

cd "$DEPLOY_PATH"

if [ ! -f .env ]; then
  cp deploy/env.production.example .env
  sed -i "s/FLASK_PORT=5000/FLASK_PORT=${API_PORT}/" .env
  sed -i 's/请改成随机长字符串/office_prod_'$(date +%s)'/g' .env
  echo "!!! 请执行: vi ${DEPLOY_PATH}/.env  修改 DB_PASSWORD !!!"
fi

echo "==> Python 虚拟环境..."
python3 -m venv venv
./venv/bin/pip install -r requirements.txt -q

echo "==> 初始化数据库..."
mysql -u root < init_db.sql 2>/dev/null || true
./venv/bin/python scripts/init_admin.py || true

echo "==> systemd 服务..."
cp deploy/office-backend.service /etc/systemd/system/office-backend.service
systemctl daemon-reload
systemctl enable office-backend
systemctl restart office-backend

sleep 2
curl -sf "http://127.0.0.1:${API_PORT}/health" && echo "" || journalctl -u office-backend -n 30 --no-pager

echo ""
echo "============================================"
echo " 公网访问: http://118.31.109.161:${API_PORT}/health"
echo " 安全组需放行 TCP ${API_PORT}（你已有 8000，也可用 API_PORT=8000 bash 本脚本）"
echo " GitHub Secrets: DEPLOY_HOST=118.31.109.161"
echo "============================================"
