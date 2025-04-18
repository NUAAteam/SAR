FROM busybox:latest

# 创建必要的目录结构
RUN mkdir -p /var/www/html /etc/nginx /etc/nginx/ssl /run/nginx

# 复制前端文件夹内容将由 docker-compose 挂载

EXPOSE 80 443

# 使用 busybox httpd 提供 Web 服务
CMD ["httpd", "-f", "-p", "80", "-h", "/var/www/html"]
