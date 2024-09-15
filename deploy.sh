#!/bin/bash

# 设置变量
REPO_PATH="$HOME/SAR"
NGINX_CONF="/etc/nginx/sites-available/nuaasar.xyz"
SSL_PATH="/etc/letsencrypt/live/nuaasar.xyz"
SERVICE_FILE="/etc/systemd/system/nuaasar.service"

# 更新系统并安装必要的软件
sudo apt update
sudo apt install -y python3 python3-pip python3-venv nginx certbot python3-certbot-nginx

# 创建并激活虚拟环境
cd $REPO_PATH/week6/backend
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 复制并修改 Nginx 配置
sudo cp $REPO_PATH/deploy/configs/nginx/nginx.conf /etc/nginx/
sudo cp $REPO_PATH/deploy/configs/nginx/nuaasar.xyz $NGINX_CONF
sudo sed -i "s|~/|$HOME/|g" $NGINX_CONF

# 注释掉 SSL 配置（因为我们还没有证书）
sudo sed -i 's/^\(\s*ssl_certificate.*\)/#\1/' $NGINX_CONF
sudo sed -i 's/^\(\s*ssl_certificate_key.*\)/#\1/' $NGINX_CONF

sudo ln -sf $NGINX_CONF /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# 复制并修改 systemd 服务文件
sudo cp $REPO_PATH/deploy/configs/systemd/nuaasar.service $SERVICE_FILE
sudo sed -i "s|~/|$HOME/|g" $SERVICE_FILE

# 重新加载 systemd，启动服务
sudo systemctl daemon-reload
sudo systemctl enable nuaasar.service
sudo systemctl start nuaasar.service

# 重启 Nginx
sudo systemctl restart nginx

echo "Initial deployment completed!"
echo "Now, let's set up SSL certificates using Certbot."

# 运行 Certbot 获取新的 SSL 证书
sudo certbot --nginx -d nuaasar.xyz -d www.nuaasar.xyz

# 再次重启 Nginx 以应用新的 SSL 配置
sudo systemctl restart nginx

echo "Deployment and SSL setup completed!"