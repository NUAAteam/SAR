#!/bin/bash

# 设置变量
REPO_PATH="$HOME/SAR"
BACKEND_PATH="$REPO_PATH/week6/backend"
FRONTEND_PATH="$REPO_PATH/week6/frontend"
SSL_DIR="$REPO_PATH/ssl"

# 创建 SSL 目录（如果不存在）
mkdir -p $SSL_DIR

# 确保文件权限正确
chmod -R 755 $FRONTEND_PATH
chmod -R 755 $BACKEND_PATH

# 如果没有 SSL 证书，创建自签名证书（仅用于开发/测试）
if [ ! -f "$SSL_DIR/server.crt" ]; then
  echo "生成自签名 SSL 证书..."
  openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout "$SSL_DIR/server.key" \
    -out "$SSL_DIR/server.crt" \
    -subj "/CN=localhost"
fi

# 使用 Docker Compose 构建并启动应用
cd $REPO_PATH
docker-compose up --build -d

echo "应用已启动！"
echo "- 前端: http://localhost 或 https://localhost"
echo "- 后端: http://localhost:5000"
