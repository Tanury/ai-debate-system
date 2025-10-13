/**
# Deployment Guide

## Production Deployment

### Prerequisites
- Ubuntu 22.04 LTS server
- Docker & Docker Compose
- Domain name with SSL certificate
- Minimum 4GB RAM, 2 CPU cores

### Step 1: Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Create application user
sudo useradd -m -s /bin/bash debateapp
sudo usermod -aG docker debateapp
```

### Step 2: Application Deployment

```bash
# Clone repository
cd /home/debateapp
sudo -u debateapp git clone https://github.com/Tanury/ai-debate-system.git
cd ai-debate-system

# Configure environment
sudo -u debateapp cp backend/.env.example backend/.env
sudo -u debateapp nano backend/.env
# Add production values

# Start services
sudo -u debateapp docker-compose -f docker-compose.prod.yml up -d

# Check status
docker-compose ps
```

### Step 3: SSL Configuration

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal
sudo certbot renew --dry-run
```

### Step 4: Nginx Configuration

```nginx
# /etc/nginx/sites-available/debate-system
server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /ws/ {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

## Kubernetes Deployment

See `deployment/kubernetes/` directory for manifests.

## Monitoring

```bash
# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Monitor resources
docker stats
```

## Backup Strategy

```bash
# Daily database backup
docker exec postgres pg_dump -U debate_user debate_db > backup_$(date +%Y%m%d).sql

# Vector store backup
tar -czf vector_store_$(date +%Y%m%d).tar.gz data/vector_store/
```

## Rollback Procedure

```bash
# Stop current version
docker-compose down

# Checkout previous version
git checkout <previous-tag>

# Rebuild and restart
docker-compose up --build -d
```
*/