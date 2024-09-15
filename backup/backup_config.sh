#!/bin/bash

# 设置变量
REPO_PATH="$HOME/SAR"
NGINX_CONF="/etc/nginx/sites-available/nuaasar.xyz"
SERVICE_FILE="/etc/systemd/system/nuaasar.service"

# 进入仓库目录
cd $REPO_PATH

# 创建配置文件备份目录
mkdir -p deploy/configs/{nginx,systemd}

# 复制并修改 Nginx 配置
sudo cp $NGINX_CONF deploy/configs/nginx/nuaasar.xyz
sudo cp /etc/nginx/nginx.conf deploy/configs/nginx/
sed -i 's|/home/ubuntu/|~/|g' deploy/configs/nginx/nuaasar.xyz

# 从 Nginx 配置中移除 SSL 相关配置
sed -i '/ssl_certificate/d' deploy/configs/nginx/nuaasar.xyz
sed -i '/ssl_certificate_key/d' deploy/configs/nginx/nuaasar.xyz

# 复制并修改 systemd 服务文件
sudo cp $SERVICE_FILE deploy/configs/systemd/nuaasar.service
sed -i 's|/home/ubuntu/|~/|g' deploy/configs/systemd/nuaasar.service

# 更新 requirements.txt
cd week6/backend
source venv/bin/activate
pip freeze > requirements.txt
deactivate

# 提交更改到 Git
cd $REPO_PATH
git add .
git commit -m "Update deployment configs and requirements"
git push

echo "Configuration files have been backed up, modified, and pushed to the repository."
echo "To deploy on a new server, clone the repository and run the deploy.sh script."