# 教师管理系统部署指南

## 1. 服务器环境配置

```bash
# 更新系统
sudo apt update
sudo apt upgrade -y

# 安装必要的软件包
sudo apt install -y python3 python3-pip python3-venv nginx git

# 创建项目目录
sudo mkdir /var/www
sudo chown $USER:$USER /var/www
cd /var/www
```

## 2. 部署项目代码

```bash
# 克隆项目代码
git clone [您的git仓库地址] university-admin-system
cd university-admin-system

# 创建并激活虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装项目依赖
pip install -r requirements.txt
pip install gunicorn  # 用于生产环境的WSGI服务器
```

## 3. 配置 Gunicorn 服务

创建系统服务文件：
```bash
sudo nano /etc/systemd/system/university-admin.service
```

添加以下内容：
```ini
[Unit]
Description=University Admin System
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/university-admin-system
Environment="PATH=/var/www/university-admin-system/venv/bin"
ExecStart=/var/www/university-admin-system/venv/bin/gunicorn --workers 3 --bind unix:university-admin.sock -m 007 backend.app:app

[Install]
WantedBy=multi-user.target
```

## 4. 配置 Nginx

创建 Nginx 配置文件：
```bash
sudo nano /etc/nginx/sites-available/university-admin
```

添加以下内容：
```nginx
server {
    listen 80;
    server_name your_domain.com;  # 替换为您的域名或服务器IP

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/university-admin-system/university-admin.sock;
    }

    location /static {
        alias /var/www/university-admin-system/frontend/static;
    }
}
```

启用站点：
```bash
sudo ln -s /etc/nginx/sites-available/university-admin /etc/nginx/sites-enabled
sudo nginx -t  # 测试配置
sudo systemctl restart nginx
```

## 5. 启动服务

```bash
# 设置权限
sudo chown -R www-data:www-data /var/www/university-admin-system
sudo chmod -R 755 /var/www/university-admin-system

# 启动服务
sudo systemctl start university-admin
sudo systemctl enable university-admin

# 查看服务状态
sudo systemctl status university-admin
```

## 6. 数据库迁移

```bash
# 激活虚拟环境
source /var/www/university-admin-system/venv/bin/activate

# 初始化数据库
cd /var/www/university-admin-system
python init_teachers.py
```

## 7. 安全配置

1. 配置防火墙：
```bash
sudo ufw allow 80/tcp  # HTTP
sudo ufw allow 443/tcp  # HTTPS（如果使用）
sudo ufw allow 22/tcp  # SSH
sudo ufw enable
```

2. 设置 SSL（可选，推荐）：
```bash
# 安装 Certbot
sudo apt install certbot python3-certbot-nginx

# 获取并配置 SSL 证书
sudo certbot --nginx -d your_domain.com
```

## 8. 维护说明

- 查看日志：
  ```bash
  sudo journalctl -u university-admin
  sudo tail -f /var/log/nginx/error.log
  ```

- 重启服务：
  ```bash
  sudo systemctl restart university-admin
  sudo systemctl restart nginx
  ```

- 更新代码：
  ```bash
  cd /var/www/university-admin-system
  git pull
  source venv/bin/activate
  pip install -r requirements.txt
  sudo systemctl restart university-admin
  ``` 