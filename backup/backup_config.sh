#!/bin/bash

# 放在~目录下运行
# 设置变量
REPO_PATH="$HOME/SAR"
NGINX_CONF="/etc/nginx/sites-available/nuaasar.xyz"
SSL_PATH="/etc/letsencrypt/live/nuaasar.xyz"
SERVICE_FILE="/etc/systemd/system/nuaasar.service"

# 进入仓库目录
cd $REPO_PATH

# 创建配置文件备份目录
mkdir -p deploy/configs/{nginx,ssl,systemd}

# 复制并修改 Nginx 配置
sudo cp $NGINX_CONF deploy/configs/nginx/nuaasar.xyz
sudo cp /etc/nginx/nginx.conf deploy/configs/nginx/
sed -i 's|/home/ubuntu/|~/|g' deploy/configs/nginx/nuaasar.xyz

# 复制 SSL 配置（不包括私钥）
sudo cp $SSL_PATH/fullchain.pem deploy/configs/ssl/
sudo cp $SSL_PATH/chain.pem deploy/configs/ssl/
sudo cp /etc/letsencrypt/options-ssl-nginx.conf deploy/configs/ssl/

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