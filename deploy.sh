#!/bin/bash

# 设置变量
REPO_PATH="$HOME/SAR"
NGINX_CONF="/etc/nginx/sites-available/nuaasar.xyz"
SSL_PATH="/etc/letsencrypt/live/nuaasar.xyz"
SERVICE_FILE="/etc/systemd/system/nuaasar.service"
DOMAIN="nuaasar.xyz"
BACKEND_PATH="$REPO_PATH/week6/backend"
FRONTEND_PATH="$REPO_PATH/week6/frontend"

# 更新系统并安装必要的软件
sudo apt update
sudo apt install -y python3 python3-pip python3-venv nginx certbot python3-certbot-nginx

# 创建并激活虚拟环境
cd $BACKEND_PATH
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 复制并修改 Nginx 配置
sudo cp $REPO_PATH/deploy/configs/nginx/nginx.conf /etc/nginx/
sudo cp $REPO_PATH/deploy/configs/nginx/$DOMAIN $NGINX_CONF
sudo sed -i "s|~/|$HOME/|g" $NGINX_CONF

# 设置前端文件权限
sudo chmod -R 755 $FRONTEND_PATH
sudo chgrp -R www-data $FRONTEND_PATH

# 设置后端文件权限
sudo chmod -R 755 $BACKEND_PATH
sudo chgrp -R www-data $BACKEND_PATH

# 确保路径可访问
sudo chmod 755 $HOME
sudo chmod 755 $REPO_PATH
sudo chmod 755 $REPO_PATH/week6

# 复制并修改 systemd 服务文件
sudo cp $REPO_PATH/deploy/configs/systemd/nuaasar.service $SERVICE_FILE
sudo sed -i "s|~/|$HOME/|g" $SERVICE_FILE

# 修改服务文件以使用 root 用户运行（注意：这可能带来安全风险）
sudo sed -i 's/User=.*/User=root/' $SERVICE_FILE
sudo sed -i 's/Group=.*/Group=root/' $SERVICE_FILE

# 重新加载 systemd，启动服务
sudo systemctl daemon-reload
sudo systemctl enable nuaasar.service
sudo systemctl start nuaasar.service

# 配置 Nginx
sudo sed -i 's|root .*;|root '"$FRONTEND_PATH"';|' $NGINX_CONF

# 重启 Nginx
sudo systemctl restart nginx

# 运行 Certbot 获取新的 SSL 证书
sudo certbot --nginx -d $DOMAIN -d www.$DOMAIN

# 再次重启 Nginx 以应用新的 SSL 配置
sudo systemctl restart nginx

echo "部署完成！"