# Deployment Guide — Project Volusia

> How to deploy Project Volusia in various environments.

---

## Table of Contents

1. [Local Development](#local-development)
2. [Windows Service](#windows-service)
3. [Production Deployment](#production-deployment)
4. [Cloud Deployment](#cloud-deployment)
5. [Docker (Future)](#docker-future)
6. [Troubleshooting](#troubleshooting)

---

## Local Development

### Prerequisites

- Python 3.11+
- Git
- Windows 10/11 or Linux/macOS

### Setup

```bash
# Clone repository
git clone https://github.com/ZQM-Labs/project-volusia.git
cd project-volusia

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install fastapi uvicorn matplotlib requests

# Run database initialization
cd Tools
python -c "from volusia_data.refresh_v2 import init_db; init_db()"

# Start portal
python -m volusia_data.portal_app
```

### Access

- Portal: http://localhost:8789
- API: http://localhost:8790
- Proxy: http://localhost:80

---

## Windows Service

### Using NSSM (Non-Sucking Service Manager)

```bash
# Download NSSM from https://nssm.cc/
# Install portal as service
nssm install ProjectVolusiaPortal "C:\Python311\python.exe" "-m volusia_data.portal_app"
nssm set ProjectVolusiaPortal AppDirectory "C:\Users\zqmco\project-volusia\Tools"
nssm set ProjectVolusiaPortal DisplayName "Project Volusia Portal"
nssm set ProjectVolusiaPortal Description "Open intelligence for Volusia County"
nssm start ProjectVolusiaPortal

# Install contribution API as service
nssm install ProjectVolusiaAPI "C:\Python311\python.exe" "-m volusia_data.contribution_api"
nssm set ProjectVolusiaAPI AppDirectory "C:\Users\zqmco\project-volusia\Tools"
nssm start ProjectVolusiaAPI
```

### Using Task Scheduler

```powershell
# Create scheduled task for portal
$action = New-ScheduledTaskAction -Execute "python.exe" -Argument "-m volusia_data.portal_app" -WorkingDirectory "C:\Users\zqmco\project-volusia\Tools"
$trigger = New-ScheduledTaskTrigger -AtStartup
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
Register-ScheduledTask -TaskName "ProjectVolusiaPortal" -Action $action -Trigger $trigger -Settings $settings -RunLevel Highest
```

### Using sc.exe

```bash
# Create service
sc create ProjectVolusiaPortal binPath= "C:\Python311\python.exe -m volusia_data.portal_app" start= auto
sc description ProjectVolusiaPortal "Open intelligence for Volusia County"
sc start ProjectVolusiaPortal
```

---

## Production Deployment

### Windows Server

#### 1. Install Python

```powershell
# Download Python 3.11+ from python.org
# Install with "Add to PATH" checked
```

#### 2. Clone and Setup

```powershell
cd C:\inetpub
git clone https://github.com/ZQM-Labs/project-volusia.git
cd project-volusia
pip install -r requirements.txt
```

#### 3. Configure IIS (Optional)

```powershell
# Install IIS with CGI feature
Install-WindowsFeature Web-Server, Web-CGI

# Create web.config for FastAPI
@"
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
  <system.webServer>
    <handlers>
      <add name="PythonHandler" path="*" verb="*" modules="CgiModule" scriptProcessor="C:\Python311\python.exe|C:\inetpub\project-volusia\Tools\volusia_data\portal_app.py" resourceType="Unspecified" />
    </handlers>
  </system.webServer>
</configuration>
"@ | Out-File -FilePath "C:\inetpub\project-volusia\web.config" -Encoding UTF8
```

#### 4. Configure Firewall

```powershell
# Allow port 80
New-NetFirewallRule -DisplayName "Project Volusia HTTP" -Direction Inbound -Protocol TCP -LocalPort 80 -Action Allow

# Allow port 8789 (optional, for direct access)
New-NetFirewallRule -DisplayName "Project Volusia Portal" -Direction Inbound -Protocol TCP -LocalPort 8789 -Action Allow
```

#### 5. Start Services

```powershell
# Start as background jobs
Start-Job -ScriptBlock { cd C:\inetpub\project-volusia\Tools; python -m volusia_data.portal_app }
Start-Job -ScriptBlock { cd C:\inetpub\project-volusia\Tools; python -m volusia_data.contribution_api }
```

### Linux (Ubuntu/Debian)

#### 1. Install Dependencies

```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip nginx
```

#### 2. Clone and Setup

```bash
cd /opt
sudo git clone https://github.com/ZQM-Labs/project-volusia.git
cd project-volusia
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 3. Create Systemd Service

```bash
# Create service file
sudo tee /etc/systemd/system/project-volusia.service > /dev/null <<EOF
[Unit]
Description=Project Volusia Portal
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/opt/project-volusia/Tools
Environment=PATH=/opt/project-volusia/venv/bin
ExecStart=/opt/project-volusia/venv/bin/python -m volusia_data.portal_app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable and start
sudo systemctl daemon-reload
sudo systemctl enable project-volusia
sudo systemctl start project-volusia
```

#### 4. Configure Nginx Reverse Proxy

```bash
sudo tee /etc/nginx/sites-available/project-volusia > /dev/null <<EOF
server {
    listen 80;
    server_name volusia.zqmlabs.com;

    location / {
        proxy_pass http://127.0.0.1:8789;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }

    location /api/v1/ {
        proxy_pass http://127.0.0.1:8790;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
EOF

sudo ln -s /etc/nginx/sites-available/project-volusia /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## Cloud Deployment

### AWS (Future)

#### EC2

```bash
# Launch EC2 instance
aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1f0 \
  --instance-type t3.micro \
  --key-name my-key \
  --security-group-ids sg-12345678 \
  --subnet-id subnet-12345678

# Connect and setup
ssh -i my-key.pem ec2-user@<public-ip>
sudo yum install python3.11 git
git clone https://github.com/ZQM-Labs/project-volusia.git
cd project-volusia
pip3.11 install -r requirements.txt
python3.11 -m volusia_data.portal_app
```

#### ECS (Future)

```json
{
  "family": "project-volusia",
  "containerDefinitions": [
    {
      "name": "portal",
      "image": "zqmlabs/project-volusia:latest",
      "portMappings": [
        {
          "containerPort": 8789,
          "hostPort": 8789
        }
      ],
      "essential": true
    }
  ]
}
```

### Azure (Future)

```bash
# Create resource group
az group create --name ProjectVolusia --location eastus

# Create App Service
az webapp create \
  --name project-volusia \
  --resource-group ProjectVolusia \
  --plan myAppServicePlan \
  --runtime "PYTHON:3.11"

# Deploy
az webapp deployment source config \
  --name project-volusia \
  --resource-group ProjectVolusia \
  --repo-url https://github.com/ZQM-Labs/project-volusia.git \
  --branch main
```

### GCP (Future)

```bash
# Create instance
gcloud compute instances create project-volusia \
  --machine-type e2-micro \
  --image-family ubuntu-2204-lts \
  --image-project ubuntu-os-cloud \
  --tags http-server

# Deploy
gcloud compute ssh project-volusia --command "git clone https://github.com/ZQM-Labs/project-volusia.git && cd project-volusia && pip install -r requirements.txt"
```

---

## Docker (Future)

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8789 8790

CMD ["python", "-m", "volusia_data.portal_app"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  portal:
    build: .
    ports:
      - "8789:8789"
    volumes:
      - ./data:/app/data
    environment:
      - DATABASE_URL=sqlite:///app/data/volusia.db
    restart: unless-stopped

  api:
    build: .
    command: python -m volusia_data.contribution_api
    ports:
      - "8790:8790"
    volumes:
      - ./data:/app/data
    restart: unless-stopped

  proxy:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - portal
      - api
    restart: unless-stopped
```

### Build and Run

```bash
# Build
docker-compose build

# Run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

---

## Troubleshooting

### Common Issues

#### Port Already in Use

```bash
# Find process using port
netstat -ano | grep ":8789"
# Kill process
taskkill /F /PID <pid>
```

#### Database Locked

```bash
# Close all connections
sqlite3 volusia.db "PRAGMA wal_checkpoint;"
# Delete WAL files
rm volusia.db-wal volusia.db-shm
```

#### Import Errors

```bash
# Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

#### Service Won't Start

```bash
# Check logs
journalctl -u project-volusia -f  # Linux
sc query ProjectVolusiaPortal      # Windows
```

### Health Checks

```bash
# Portal health
curl http://localhost:8789/api/health

# API health
curl http://localhost:8790/api/v1/health

# Database integrity
sqlite3 Tools/volusia_data/volusia.db "PRAGMA integrity_check;"
```

### Performance Tuning

```bash
# Increase SQLite cache
sqlite3 volusia.db "PRAGMA cache_size=10000;"

# Enable WAL mode
sqlite3 volusia.db "PRAGMA journal_mode=WAL;"

# Increase Python recursion limit
python -c "import sys; sys.setrecursionlimit(10000); from volusia_data.portal_app import app"
```

---

## Monitoring

### Log Files

| File | Location | Description |
|------|----------|-------------|
| Portal log | `logs/portal.log` | Portal access and errors |
| API log | `logs/api.log` | API access and errors |
| Pipeline log | `logs/pipeline.log` | Data pipeline runs |
| Quality log | `logs/quality.log` | Quality check results |

### Metrics

```bash
# Count indicators
sqlite3 volusia.db "SELECT COUNT(*) FROM indicators;"

# Count by category
sqlite3 volusia.db "SELECT category, COUNT(*) FROM indicators GROUP BY category;"

# Check freshness
sqlite3 volusia.db "SELECT COUNT(*) FROM indicators WHERE fetched_at < datetime('now', '-30 days');"
```

---

## Backup

### Database Backup

```bash
# SQLite backup
sqlite3 volusia.db ".backup volusia.db.backup"

# Or copy file
cp volusia.db volusia.db.$(date +%Y%m%d).backup
```

### Full Backup

```bash
# Create tar archive
tar -czf project-volusia-backup-$(date +%Y%m%d).tar.gz \
  --exclude='.git' \
  --exclude='__pycache__' \
  --exclude='*.pyc' \
  .
```

---

## Security Checklist

- [ ] Firewall configured (only ports 80/443 open)
- [ ] API keys set for write operations
- [ ] Database file permissions restricted
- [ ] Regular backups scheduled
- [ ] Log rotation configured
- [ ] SSL/TLS configured (production)
- [ ] Rate limiting enabled
- [ ] Input validation active

---

*Last updated: 2026-09-06*
