# Deployment Guide - Outreach Scraping Toolkit

Production deployment instructions for the Outreach Scraping Toolkit.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Environment Setup](#environment-setup)
- [Building for Production](#building-for-production)
- [Deployment Options](#deployment-options)
- [Docker Deployment](#docker-deployment)
- [Cloud Deployment](#cloud-deployment)
- [Environment Variables](#environment-variables)
- [Security](#security)
- [Monitoring](#monitoring)
- [Performance Optimization](#performance-optimization)

## Prerequisites

### Production Server Requirements

- **OS:** Ubuntu 20.04+ LTS (recommended) or any Linux distribution
- **CPU:** Minimum 2 cores (4+ recommended)
- **Memory:** Minimum 4GB RAM (8GB+ recommended)
- **Storage:** 20GB+ available disk space
- **Network:** Public IP address with open ports 80/443
- **Domain:** Optional but recommended for HTTPS

### Required Software

- **Python:** 3.9 or higher
- **Node.js:** 16.x or higher
- **Nginx:** For reverse proxy
- **Certbot:** For SSL certificates (Let's Encrypt)
- **Docker:** Optional but recommended
- **Git:** For deployment from repository

## Environment Setup

### 1. Create Production User

```bash
# Create dedicated user
sudo adduser --system --group outreach
sudo usermod -aG sudo outreach

# Switch to production user
sudo su - outreach
```

### 2. Clone Repository

```bash
cd /opt
sudo git clone <your-repository-url> outreach-toolkit
sudo chown -R outreach:outreach outreach-toolkit
cd outreach-toolkit
```

### 3. Configure Environment

```bash
# Copy and edit environment file
cp .env.example .env
nano .env
```

**Production .env file:**

```bash
# REQUIRED: Apify API Token
APIFY_API_TOKEN=your_production_apify_token

# Backend Configuration
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000

# Frontend URL (for CORS)
FRONTEND_URL=https://yourdomain.com

# Database (if using PostgreSQL)
# DATABASE_URL=postgresql://user:password@localhost:5432/outreach_db

# Security
SECRET_KEY=your_random_secret_key_here

# Logging
LOG_LEVEL=INFO
SENTRY_DSN=your_sentry_dsn  # Optional: error tracking

# Email (for notifications)
# SMTP_HOST=smtp.gmail.com
# SMTP_PORT=587
# SMTP_USERNAME=your_email
# SMTP_PASSWORD=your_password
```

**Generate secret key:**

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## Building for Production

### Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install production server
pip install gunicorn

# Test backend
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Frontend Build

```bash
cd frontend

# Install dependencies
npm install

# Build for production
npm run build

# Output will be in frontend/dist/
ls -la dist/
```

**Build output:**
- Minified JavaScript bundles
- Optimized CSS files
- Static assets (images, fonts)
- `index.html` entry point

## Deployment Options

### Option 1: Manual Deployment (Process Manager)

Use systemd to manage backend and serve frontend with Nginx.

#### 1. Create Systemd Service for Backend

```bash
sudo nano /etc/systemd/system/outreach-backend.service
```

```ini
[Unit]
Description=Outreach Scraping Toolkit Backend
After=network.target

[Service]
Type=notify
User=outreach
Group=outreach
WorkingDirectory=/opt/outreach-toolkit/backend
Environment="PATH=/opt/outreach-toolkit/backend/venv/bin"
ExecStart=/opt/outreach-toolkit/backend/venv/bin/gunicorn main:app \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000 \
    --timeout 120 \
    --access-logfile /var/log/outreach/access.log \
    --error-logfile /var/log/outreach/error.log
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### 2. Create Log Directory

```bash
sudo mkdir -p /var/log/outreach
sudo chown -R outreach:outreach /var/log/outreach
```

#### 3. Enable and Start Service

```bash
sudo systemctl daemon-reload
sudo systemctl enable outreach-backend
sudo systemctl start outreach-backend
sudo systemctl status outreach-backend
```

#### 4. Configure Nginx

```bash
sudo apt update
sudo apt install nginx
sudo nano /etc/nginx/sites-available/outreach-toolkit
```

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    # Frontend (React build)
    location / {
        root /opt/outreach-toolkit/frontend/dist;
        try_files $uri $uri/ /index.html;

        # Cache static assets
        location ~* \.(js|css|png|jpg|jpeg|gif|svg|ico|woff|woff2)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Increase timeout for scraping operations
        proxy_read_timeout 300s;
        proxy_connect_timeout 75s;
    }

    # Backend root endpoints
    location ~ ^/(scrape|results|history|leads|download-csv|docs|redoc|openapi.json)$ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_read_timeout 300s;
        proxy_connect_timeout 75s;
    }

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
}
```

#### 5. Enable Site and Restart Nginx

```bash
sudo ln -s /etc/nginx/sites-available/outreach-toolkit /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 6. Setup SSL with Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

Certbot will automatically:
- Obtain SSL certificate
- Configure Nginx for HTTPS
- Setup auto-renewal

**Test auto-renewal:**

```bash
sudo certbot renew --dry-run
```

### Option 2: Docker Deployment (Recommended)

Docker provides isolated, reproducible deployments.

#### 1. Create Dockerfile for Backend

```bash
nano backend/Dockerfile
```

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy application
COPY . .

# Create data directory
RUN mkdir -p /app/data && chmod 755 /app/data

# Expose port
EXPOSE 8000

# Run with gunicorn
CMD ["gunicorn", "main:app", \
     "--workers", "4", \
     "--worker-class", "uvicorn.workers.UvicornWorker", \
     "--bind", "0.0.0.0:8000", \
     "--timeout", "120"]
```

#### 2. Create Dockerfile for Frontend

```bash
nano frontend/Dockerfile
```

```dockerfile
# Build stage
FROM node:18-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy built files
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

#### 3. Create Nginx Config for Frontend

```bash
nano frontend/nginx.conf
```

```nginx
server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;

    # Frontend routing
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Cache static assets
    location ~* \.(js|css|png|jpg|jpeg|gif|svg|ico|woff|woff2)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
}
```

#### 4. Create Docker Compose File

```bash
nano docker-compose.yml
```

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    container_name: outreach-backend
    restart: unless-stopped
    ports:
      - "8000:8000"
    environment:
      - APIFY_API_TOKEN=${APIFY_API_TOKEN}
      - FRONTEND_URL=${FRONTEND_URL:-http://localhost}
    volumes:
      - ./data:/app/data
      - ./config:/app/config:ro
      - ./docs:/app/docs:ro
    networks:
      - outreach-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/"]
      interval: 30s
      timeout: 10s
      retries: 3

  frontend:
    build: ./frontend
    container_name: outreach-frontend
    restart: unless-stopped
    ports:
      - "80:80"
    depends_on:
      - backend
    networks:
      - outreach-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost/"]
      interval: 30s
      timeout: 10s
      retries: 3

networks:
  outreach-network:
    driver: bridge

volumes:
  data:
```

#### 5. Deploy with Docker Compose

```bash
# Build and start services
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Restart specific service
docker-compose restart backend
```

## Cloud Deployment

### AWS Deployment

#### EC2 Instance

1. **Launch EC2 Instance:**
   - AMI: Ubuntu 20.04 LTS
   - Instance Type: t3.medium (2 vCPU, 4GB RAM)
   - Storage: 20GB gp3
   - Security Group: Allow 80, 443, 22

2. **Configure Elastic IP:**
   ```bash
   # Allocate and associate Elastic IP
   ```

3. **Setup Domain:**
   - Point A record to Elastic IP
   - Wait for DNS propagation

4. **Deploy Application:**
   ```bash
   ssh -i your-key.pem ubuntu@your-elastic-ip
   # Follow manual deployment steps above
   ```

#### Elastic Beanstalk (Alternative)

```bash
# Install EB CLI
pip install awsebcli

# Initialize Elastic Beanstalk
eb init -p python-3.11 outreach-toolkit

# Create environment
eb create outreach-production

# Deploy
eb deploy
```

### DigitalOcean Deployment

1. **Create Droplet:**
   - Image: Ubuntu 20.04
   - Plan: Basic ($24/mo - 2GB RAM)
   - Add SSH key

2. **Configure Firewall:**
   - Allow HTTP (80)
   - Allow HTTPS (443)
   - Allow SSH (22)

3. **Deploy:**
   ```bash
   ssh root@your-droplet-ip
   # Follow manual deployment steps
   ```

### Heroku Deployment (Simple)

```bash
# Install Heroku CLI
npm install -g heroku

# Login
heroku login

# Create app
heroku create outreach-toolkit

# Set buildpacks
heroku buildpacks:add heroku/python
heroku buildpacks:add heroku/nodejs

# Set environment variables
heroku config:set APIFY_API_TOKEN=your_token

# Deploy
git push heroku main
```

## Environment Variables

### Production Environment Variables

```bash
# Required
APIFY_API_TOKEN=xxx

# Backend
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
WORKERS=4

# Frontend
FRONTEND_URL=https://yourdomain.com

# Database (optional - for future PostgreSQL migration)
DATABASE_URL=postgresql://user:pass@host:5432/db

# Security
SECRET_KEY=xxx
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Monitoring
SENTRY_DSN=xxx
LOG_LEVEL=INFO

# Email (optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=xxx
SMTP_PASSWORD=xxx
```

## Security

### 1. Update Backend CORS

Edit `backend/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://yourdomain.com",
        "https://www.yourdomain.com"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["*"],
)
```

### 2. Add Authentication (Recommended)

Install FastAPI security:

```bash
pip install python-jose[cryptography] passlib[bcrypt] python-multipart
```

Add JWT authentication:

```python
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

# Add to main.py
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Protect endpoints
@app.get("/leads")
async def get_leads(token: str = Depends(oauth2_scheme)):
    # Verify token
    # Return leads
```

### 3. Environment Security

```bash
# Set proper file permissions
chmod 600 .env
chmod 600 data/*.json

# Restrict directory access
chmod 755 /opt/outreach-toolkit
chown -R outreach:outreach /opt/outreach-toolkit
```

### 4. Firewall Configuration

```bash
# Using UFW (Ubuntu)
sudo ufw allow 22/tcp   # SSH
sudo ufw allow 80/tcp   # HTTP
sudo ufw allow 443/tcp  # HTTPS
sudo ufw enable
```

### 5. Fail2Ban (Prevent Brute Force)

```bash
sudo apt install fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

## Monitoring

### 1. Application Monitoring

**Sentry (Error Tracking):**

```bash
pip install sentry-sdk
```

```python
# Add to backend/main.py
import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    traces_sample_rate=1.0,
)

app.add_middleware(SentryAsgiMiddleware)
```

### 2. Server Monitoring

**Install monitoring tools:**

```bash
# System monitoring
sudo apt install htop iotop nethogs

# Log monitoring
sudo apt install logwatch
```

### 3. Uptime Monitoring

Use services like:
- UptimeRobot (free)
- Pingdom
- StatusCake

Monitor endpoints:
- `https://yourdomain.com/` (frontend)
- `https://yourdomain.com/api/config/audience` (backend)

### 4. Log Management

**Centralized logging:**

```bash
# Install Papertrail agent
wget -qO - https://github.com/papertrail/remote_syslog2/releases/download/v0.20/remote_syslog_linux_amd64.tar.gz | tar xvz
sudo cp remote_syslog/remote_syslog /usr/local/bin/
```

**Configure log rotation:**

```bash
sudo nano /etc/logrotate.d/outreach
```

```
/var/log/outreach/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 outreach outreach
    sharedscripts
    postrotate
        systemctl reload outreach-backend > /dev/null 2>&1 || true
    endscript
}
```

## Performance Optimization

### 1. Enable Gzip Compression

Nginx config:

```nginx
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_types text/plain text/css text/xml text/javascript application/javascript application/json;
```

### 2. Add Caching

```nginx
# Cache API responses (optional, adjust TTL)
location /api/config/audience {
    proxy_pass http://localhost:8000;
    proxy_cache_valid 200 1h;
    add_header X-Cache-Status $upstream_cache_status;
}
```

### 3. Database Optimization

If migrating to PostgreSQL:

```python
# Add connection pooling
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20
)
```

### 4. CDN for Frontend

Use CloudFlare or AWS CloudFront:
- Cache static assets globally
- DDoS protection
- Automatic HTTPS

### 5. Rate Limiting

Add rate limiting middleware:

```bash
pip install slowapi
```

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/scrape")
@limiter.limit("10/minute")
async def scrape_leads(request: Request, ...):
    ...
```

## Backup Strategy

### 1. Database Backups

```bash
# Backup script
#!/bin/bash
BACKUP_DIR="/opt/backups/outreach"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR
cp -r /opt/outreach-toolkit/data $BACKUP_DIR/data_$DATE
gzip $BACKUP_DIR/data_$DATE/*.json

# Keep last 30 days
find $BACKUP_DIR -name "data_*" -mtime +30 -delete
```

### 2. Automated Backups

```bash
# Add to crontab
crontab -e
```

```
# Backup daily at 2 AM
0 2 * * * /opt/outreach-toolkit/scripts/backup.sh
```

### 3. Cloud Backups

Sync to S3:

```bash
# Install AWS CLI
pip install awscli

# Configure
aws configure

# Sync backups
aws s3 sync /opt/backups/outreach s3://your-bucket/outreach-backups/
```

## Troubleshooting

See [SETUP.md](./SETUP.md) troubleshooting section for common issues.

## Next Steps

- Setup monitoring and alerts
- Configure automated backups
- Implement authentication
- Add rate limiting
- Enable CDN
- Setup CI/CD pipeline
- Load testing

## Support

- Read [SETUP.md](./SETUP.md) for local development
- Review [API.md](./API.md) for API details
- Check [ARCHITECTURE.md](./ARCHITECTURE.md) for system design
