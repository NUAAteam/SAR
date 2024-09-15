#!/bin/bash

# 放在~目录下运行
# 创建一个日志文件
LOG_FILE="web_config_search_results.log"
echo "Web Configuration File Search Results" > $LOG_FILE
echo "======================================" >> $LOG_FILE
echo "Search performed on: $(date)" >> $LOG_FILE
echo "" >> $LOG_FILE

# 函数：搜索并记录结果
search_and_log() {
    echo "Searching for $1" >> $LOG_FILE
    echo "-------------------" >> $LOG_FILE
    eval $2 >> $LOG_FILE 2>&1
    echo "" >> $LOG_FILE
}

# Nginx 配置
search_and_log "Nginx configuration files" "sudo find /etc/nginx -type f -name '*.conf'"
search_and_log "Nginx sites-available" "ls -l /etc/nginx/sites-available/"
search_and_log "Nginx sites-enabled" "ls -l /etc/nginx/sites-enabled/"

# Apache 配置
search_and_log "Apache configuration files" "sudo find /etc/apache2 -type f -name '*.conf'"
search_and_log "Apache sites-available" "ls -l /etc/apache2/sites-available/"
search_and_log "Apache sites-enabled" "ls -l /etc/apache2/sites-enabled/"

# Python WSGI 文件
search_and_log "Python WSGI files" "find /home/ubuntu -type f -name '*.wsgi' -o -name 'wsgi.py'"
search_and_log "Gunicorn config files" "find /home/ubuntu -type f -name 'gunicorn.conf.py'"

# Flask 应用文件
search_and_log "Flask application files" "find /home/ubuntu -type f -name 'app.py' -o -name 'application.py'"

# 环境变量文件
search_and_log "Environment files" "find /home/ubuntu -type f -name '.env'"

# Requirements 文件
search_and_log "Requirements files" "find /home/ubuntu -type f -name 'requirements.txt'"

# 配置文件
search_and_log "Python config files" "find /home/ubuntu -type f -name 'config.py' -o -name 'settings.py'"

# Systemd 服务文件
search_and_log "Systemd service files" "sudo ls -l /etc/systemd/system/*.service | grep -i 'web\|app\|flask\|django\|gunicorn'"

# 日志文件
search_and_log "Log files" "sudo find /var/log -type f -name '*access.log' -o -name '*error.log'"

# SSL 证书文件
search_and_log "SSL certificate files" "sudo find /etc/letsencrypt -type f -name '*.pem'"
search_and_log "SSL key files" "sudo find /etc/ssl -type f -name '*.crt' -o -name '*.key'"

# 数据库配置文件
search_and_log "MySQL config files" "sudo find /etc -type f -name 'my.cnf' -o -name 'mysqld.cnf'"
search_and_log "PostgreSQL config files" "sudo find /etc/postgresql -type f -name 'postgresql.conf'"

# 最近修改的配置文件
search_and_log "Recently modified config files" "sudo find /etc -type f -mtime -7 | grep -E '\.conf$|\.ini$|\.yaml$|\.yml$'"

echo "Search completed. Results saved in $LOG_FILE"