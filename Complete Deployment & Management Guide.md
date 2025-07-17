# Complete Deployment & Management Guide
## AI-Driven Property Agency Ecosystem

This guide provides step-by-step instructions for deploying and managing your entire property website system independently.

## Table of Contents

1. [System Overview](#system-overview)
2. [Prerequisites](#prerequisites)
3. [Deployment Options](#deployment-options)
4. [Step-by-Step Deployment](#step-by-step-deployment)
5. [Database Management](#database-management)
6. [Scraping System Setup](#scraping-system-setup)
7. [Automation & Scheduling](#automation--scheduling)
8. [Monitoring & Maintenance](#monitoring--maintenance)
9. [Troubleshooting](#troubleshooting)
10. [Scaling & Optimization](#scaling--optimization)

---

## System Overview

Your AI-driven property agency ecosystem consists of:

### Core Components
1. **Web Scrapers** - Automated data collection from property websites
2. **Google Sheets Database** - Centralized data storage and management
3. **Flask Backend API** - Data processing and API services
4. **React Frontend** - Customer-facing website
5. **Chatbot System** - AI-powered customer engagement
6. **Automation Layer** - Scheduled tasks and data updates

### Current Architecture
```
Property Websites → Scrapers → Google Sheets → Flask API → React Website
                                     ↓
                              Chatbot System ← Customer Interactions
```

---

## Prerequisites

### Required Accounts & Services
1. **Google Cloud Platform Account**
   - For Google Sheets API access
   - Service account credentials
   
2. **Hosting Platform** (Choose one):
   - **Render.com** (Recommended for beginners)
   - **Heroku**
   - **DigitalOcean**
   - **AWS/GCP** (Advanced users)
   - **VPS/Dedicated Server**

3. **Domain Name** (Optional but recommended)
   - For professional branding
   - SSL certificate support

4. **Development Environment**
   - Python 3.8+
   - Node.js 16+
   - Git
   - Code editor (VS Code recommended)

### Required Skills
- Basic Python programming
- Basic web development knowledge
- Command line familiarity
- Understanding of APIs and databases

---

## Deployment Options

### Option 1: Cloud Platform Deployment (Recommended)

**Best for**: Beginners, quick setup, automatic scaling

**Platforms**:
- **Render.com** - Free tier available, easy deployment
- **Heroku** - Popular, good documentation
- **Railway** - Modern, developer-friendly

**Pros**:
- Automatic deployments from Git
- Built-in SSL certificates
- Easy scaling
- Monitoring included

**Cons**:
- Monthly costs for production use
- Platform-specific configurations

### Option 2: VPS/Server Deployment

**Best for**: Advanced users, full control, cost optimization

**Providers**:
- **DigitalOcean Droplets**
- **Linode**
- **AWS EC2**
- **Google Cloud Compute**

**Pros**:
- Full control over environment
- Cost-effective for high traffic
- Custom configurations

**Cons**:
- Requires server management skills
- Manual SSL setup
- Security management responsibility

### Option 3: Hybrid Approach

**Best for**: Balanced control and convenience

**Setup**:
- Backend API on cloud platform
- Frontend on CDN (Netlify/Vercel)
- Database on managed service
- Scrapers on VPS/cron jobs

---

## Step-by-Step Deployment

### Phase 1: Prepare Your Code

#### 1.1 Download System Files
```bash
# Create project directory
mkdir property-agency-system
cd property-agency-system

# Clone or download your system files
# (You'll need to package the files from the current working system)
```

#### 1.2 Set Up Google Sheets API
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable Google Sheets API
4. Create service account credentials
5. Download JSON credentials file
6. Share your Google Sheets with the service account email

#### 1.3 Prepare Environment Variables
Create `.env` file:
```env
# Google Sheets Configuration
GOOGLE_CREDENTIALS={"type":"service_account",...}
SHEET_28HSE_ID=1Dg6g0QFlETa4NdP6eR1qXGudldwe5syK8HbdZZu4h74
SHEET_CENTALINE_ID=1DsiJScP1HBftv04VFlAKt2jAJVVVU-1Nmun7K4xF7gM
SHEET_SQUAREFOOT_ID=1ZMHZuPUol0eTdXijRKRCPwMpFLWZ8qsQ0HKzhFm6PD0

# Flask Configuration
FLASK_ENV=production
SECRET_KEY=your-secret-key-here

# Database Configuration (if using external DB)
DATABASE_URL=postgresql://user:pass@host:port/dbname

# API Keys (for chatbot, if using external AI services)
OPENAI_API_KEY=your-openai-key
```

### Phase 2: Deploy Backend (Flask API)

#### 2.1 Using Render.com (Recommended)

1. **Prepare Backend Files**:
```
backend/
├── src/
│   ├── main.py
│   ├── routes/
│   │   ├── properties.py
│   │   └── chatbot.py
│   └── services/
│       └── google_sheets_service.py
├── requirements.txt
├── .env
└── render.yaml
```

2. **Create render.yaml**:
```yaml
services:
  - type: web
    name: property-backend
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python src/main.py
    envVars:
      - key: FLASK_ENV
        value: production
      - key: GOOGLE_CREDENTIALS
        sync: false
```

3. **Deploy Steps**:
   - Push code to GitHub repository
   - Connect Render to your GitHub repo
   - Set environment variables in Render dashboard
   - Deploy automatically

#### 2.2 Using Heroku

1. **Install Heroku CLI**
2. **Create Procfile**:
```
web: python src/main.py
```

3. **Deploy Commands**:
```bash
heroku create your-app-name
heroku config:set GOOGLE_CREDENTIALS="your-json-credentials"
git push heroku main
```

#### 2.3 Using VPS/Server

1. **Server Setup**:
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3 python3-pip nginx supervisor -y

# Install application
git clone your-repo
cd property-backend
pip3 install -r requirements.txt
```

2. **Configure Nginx**:
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

3. **Configure Supervisor**:
```ini
[program:property-backend]
command=python3 /path/to/your/app/src/main.py
directory=/path/to/your/app
user=www-data
autostart=true
autorestart=true
```

### Phase 3: Deploy Frontend (React Website)

#### 3.1 Build Frontend
```bash
cd frontend/
npm install
npm run build
```

#### 3.2 Deploy Options

**Option A: Serve from Backend (Current Setup)**
- Copy `dist/` files to backend `static/` folder
- Backend serves both API and frontend

**Option B: Separate Frontend Deployment**
- Deploy to Netlify/Vercel
- Update API URLs to point to backend
- Better performance and scaling

**Option C: CDN Deployment**
- Upload build files to AWS S3/CloudFront
- Configure for SPA routing
- Highest performance

### Phase 4: Set Up Scrapers

#### 4.1 Scraper Deployment Options

**Option A: Same Server as Backend**
```bash
# Add scrapers to your backend server
crontab -e
# Add: 0 */6 * * * /usr/bin/python3 /path/to/scraper/28hse_scraper.py
```

**Option B: Separate Scraper Server**
```bash
# Deploy scrapers to dedicated server
# Use GitHub Actions or similar for automation
```

**Option C: Cloud Functions**
- Deploy each scraper as serverless function
- Schedule with cloud cron services
- Cost-effective for infrequent scraping

#### 4.2 Scraper Configuration

1. **Update Scraper Code**:
```python
# In each scraper file
import gspread
from google.oauth2.service_account import Credentials

# Configure Google Sheets access
def update_google_sheet(data):
    credentials = Credentials.from_service_account_info(
        json.loads(os.environ['GOOGLE_CREDENTIALS']),
        scopes=['https://www.googleapis.com/auth/spreadsheets']
    )
    gc = gspread.authorize(credentials)
    sheet = gc.open_by_key(SHEET_ID).sheet1
    # Update sheet with scraped data
```

2. **Schedule Scrapers**:
```bash
# Linux cron jobs
0 6 * * * /usr/bin/python3 /path/to/28hse_scraper.py
0 12 * * * /usr/bin/python3 /path/to/centaline_scraper.py
0 18 * * * /usr/bin/python3 /path/to/squarefoot_scraper.py
```

---


## Database Management

### Current Setup: Google Sheets as Database

Your system currently uses Google Sheets as the primary database, which offers several advantages:

**Advantages**:
- Easy to view and edit data manually
- No database server maintenance
- Built-in sharing and collaboration
- Automatic backups by Google
- Free for reasonable usage

**Limitations**:
- API rate limits (100 requests per 100 seconds per user)
- Not suitable for high-frequency updates
- Limited query capabilities
- Potential performance issues with large datasets

### Database Management Tasks

#### 1. Google Sheets Maintenance

**1.1 Regular Data Cleanup**:
```python
# Script to remove duplicate entries
import gspread
import pandas as pd

def remove_duplicates(sheet_id):
    gc = gspread.service_account()
    sheet = gc.open_by_key(sheet_id).sheet1
    
    # Get all data
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    
    # Remove duplicates based on property URL or unique identifier
    df_clean = df.drop_duplicates(subset=['listing_url'])
    
    # Clear sheet and update with clean data
    sheet.clear()
    sheet.update([df_clean.columns.values.tolist()] + df_clean.values.tolist())
```

**1.2 Data Validation**:
```python
def validate_property_data(sheet_id):
    gc = gspread.service_account()
    sheet = gc.open_by_key(sheet_id).sheet1
    data = sheet.get_all_records()
    
    issues = []
    for i, row in enumerate(data, 2):  # Start from row 2 (after header)
        # Check required fields
        if not row.get('title'):
            issues.append(f"Row {i}: Missing title")
        if not row.get('price'):
            issues.append(f"Row {i}: Missing price")
        if not row.get('image_url'):
            issues.append(f"Row {i}: Missing image URL")
    
    return issues
```

**1.3 Backup Strategy**:
```python
import json
from datetime import datetime

def backup_sheet_data(sheet_id, backup_path):
    gc = gspread.service_account()
    sheet = gc.open_by_key(sheet_id).sheet1
    data = sheet.get_all_records()
    
    backup_file = f"{backup_path}/backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(backup_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"Backup saved to {backup_file}")
```

#### 2. Migration to Traditional Database (Optional)

If you need better performance or more advanced features, consider migrating to a traditional database:

**2.1 PostgreSQL Setup**:
```sql
-- Create properties table
CREATE TABLE properties (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    price VARCHAR(50),
    address TEXT,
    rooms VARCHAR(20),
    gross_area VARCHAR(50),
    image_url TEXT,
    listing_url TEXT UNIQUE,
    agency VARCHAR(100),
    contact_person VARCHAR(100),
    source VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index for faster searches
CREATE INDEX idx_properties_source ON properties(source);
CREATE INDEX idx_properties_price ON properties(price);
CREATE INDEX idx_properties_rooms ON properties(rooms);
```

**2.2 Migration Script**:
```python
import psycopg2
import gspread
from datetime import datetime

def migrate_sheets_to_postgres():
    # Connect to PostgreSQL
    conn = psycopg2.connect(
        host="your-host",
        database="your-db",
        user="your-user",
        password="your-password"
    )
    cur = conn.cursor()
    
    # Get data from Google Sheets
    gc = gspread.service_account()
    
    sheets = {
        '28hse': '1Dg6g0QFlETa4NdP6eR1qXGudldwe5syK8HbdZZu4h74',
        'centaline': '1DsiJScP1HBftv04VFlAKt2jAJVVVU-1Nmun7K4xF7gM',
        'squarefoot': '1ZMHZuPUol0eTdXijRKRCPwMpFLWZ8qsQ0HKzhFm6PD0'
    }
    
    for source, sheet_id in sheets.items():
        sheet = gc.open_by_key(sheet_id).sheet1
        data = sheet.get_all_records()
        
        for row in data:
            cur.execute("""
                INSERT INTO properties (title, price, address, rooms, gross_area, 
                                      image_url, listing_url, agency, contact_person, source)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (listing_url) DO UPDATE SET
                    title = EXCLUDED.title,
                    price = EXCLUDED.price,
                    updated_at = CURRENT_TIMESTAMP
            """, (
                row.get('title', ''),
                row.get('price', ''),
                row.get('address', ''),
                row.get('rooms', ''),
                row.get('gross_area', ''),
                row.get('image_url', ''),
                row.get('listing_url', ''),
                row.get('agency', ''),
                row.get('contact_person', ''),
                source
            ))
    
    conn.commit()
    cur.close()
    conn.close()
```

### Database Monitoring

#### 1. Data Quality Monitoring
```python
def monitor_data_quality():
    checks = {
        'total_properties': count_total_properties(),
        'properties_with_images': count_properties_with_images(),
        'properties_with_prices': count_properties_with_prices(),
        'duplicate_urls': count_duplicate_urls(),
        'last_update': get_last_update_time()
    }
    
    # Send alerts if quality drops below threshold
    if checks['properties_with_images'] / checks['total_properties'] < 0.8:
        send_alert("Image coverage below 80%")
    
    return checks
```

#### 2. Performance Monitoring
```python
import time
import requests

def monitor_api_performance():
    start_time = time.time()
    response = requests.get('https://your-api.com/api/properties')
    response_time = time.time() - start_time
    
    metrics = {
        'response_time': response_time,
        'status_code': response.status_code,
        'data_count': len(response.json().get('data', [])),
        'timestamp': datetime.now()
    }
    
    # Log metrics or send to monitoring service
    return metrics
```

---

## Scraping System Setup

### 1. Scraper Architecture

Your scraping system should follow this structure:
```
scrapers/
├── common/
│   ├── base_scraper.py
│   ├── utils.py
│   └── config.py
├── 28hse/
│   ├── scraper.py
│   └── parser.py
├── centaline/
│   ├── scraper.py
│   └── parser.py
├── squarefoot/
│   ├── scraper.py
│   └── parser.py
└── scheduler.py
```

### 2. Base Scraper Class
```python
# common/base_scraper.py
import requests
from bs4 import BeautifulSoup
import time
import random
from abc import ABC, abstractmethod

class BaseScraper(ABC):
    def __init__(self, name, sheet_id):
        self.name = name
        self.sheet_id = sheet_id
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get_page(self, url, retries=3):
        for attempt in range(retries):
            try:
                response = self.session.get(url, timeout=30)
                response.raise_for_status()
                return response
            except Exception as e:
                if attempt == retries - 1:
                    raise e
                time.sleep(random.uniform(1, 3))
    
    @abstractmethod
    def scrape_listings(self):
        pass
    
    @abstractmethod
    def parse_property(self, element):
        pass
    
    def save_to_sheet(self, data):
        # Implementation to save data to Google Sheets
        pass
    
    def run(self):
        print(f"Starting {self.name} scraper...")
        listings = self.scrape_listings()
        self.save_to_sheet(listings)
        print(f"Completed {self.name} scraper. Found {len(listings)} properties.")
```

### 3. Deployment Strategies

#### 3.1 Cron Job Deployment
```bash
# Install on your server
sudo crontab -e

# Add scraping schedule
0 6 * * * /usr/bin/python3 /path/to/scrapers/28hse/scraper.py >> /var/log/scraper.log 2>&1
0 12 * * * /usr/bin/python3 /path/to/scrapers/centaline/scraper.py >> /var/log/scraper.log 2>&1
0 18 * * * /usr/bin/python3 /path/to/scrapers/squarefoot/scraper.py >> /var/log/scraper.log 2>&1
```

#### 3.2 GitHub Actions Deployment
```yaml
# .github/workflows/scraper.yml
name: Property Scraper
on:
  schedule:
    - cron: '0 6,12,18 * * *'  # Run 3 times daily
  workflow_dispatch:  # Allow manual trigger

jobs:
  scrape:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run scrapers
        env:
          GOOGLE_CREDENTIALS: ${{ secrets.GOOGLE_CREDENTIALS }}
        run: |
          python scrapers/28hse/scraper.py
          python scrapers/centaline/scraper.py
          python scrapers/squarefoot/scraper.py
```

#### 3.3 Cloud Function Deployment
```python
# For Google Cloud Functions
import functions_framework
from scrapers.28hse.scraper import HSEScraper

@functions_framework.http
def scrape_28hse(request):
    scraper = HSEScraper()
    results = scraper.run()
    return {'status': 'success', 'count': len(results)}
```

### 4. Scraper Monitoring

#### 4.1 Health Checks
```python
def scraper_health_check():
    checks = {
        'last_run_28hse': get_last_scraper_run('28hse'),
        'last_run_centaline': get_last_scraper_run('centaline'),
        'last_run_squarefoot': get_last_scraper_run('squarefoot'),
        'data_freshness': check_data_freshness(),
        'error_rate': calculate_error_rate()
    }
    
    # Alert if any scraper hasn't run in 24 hours
    for scraper, last_run in checks.items():
        if last_run and (datetime.now() - last_run).hours > 24:
            send_alert(f"{scraper} hasn't run in 24 hours")
    
    return checks
```

#### 4.2 Error Handling and Logging
```python
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)

class ScraperLogger:
    def __init__(self, scraper_name):
        self.logger = logging.getLogger(scraper_name)
    
    def log_start(self):
        self.logger.info(f"Scraper started at {datetime.now()}")
    
    def log_success(self, count):
        self.logger.info(f"Successfully scraped {count} properties")
    
    def log_error(self, error):
        self.logger.error(f"Scraper error: {str(error)}")
    
    def log_warning(self, message):
        self.logger.warning(message)
```

---

## Automation & Scheduling

### 1. Automated Data Pipeline

Create a complete automated pipeline:

```python
# automation/pipeline.py
import schedule
import time
from datetime import datetime
from scrapers.runner import run_all_scrapers
from database.maintenance import cleanup_old_data, backup_data
from monitoring.health_check import run_health_checks
from notifications.alerts import send_daily_report

def daily_pipeline():
    """Complete daily automation pipeline"""
    print(f"Starting daily pipeline at {datetime.now()}")
    
    # 1. Run scrapers
    scraper_results = run_all_scrapers()
    
    # 2. Clean up old data
    cleanup_old_data(days_to_keep=30)
    
    # 3. Backup data
    backup_data()
    
    # 4. Run health checks
    health_status = run_health_checks()
    
    # 5. Send daily report
    send_daily_report(scraper_results, health_status)
    
    print(f"Daily pipeline completed at {datetime.now()}")

# Schedule tasks
schedule.every().day.at("06:00").do(daily_pipeline)
schedule.every().hour.do(run_health_checks)
schedule.every().day.at("23:00").do(backup_data)

# Keep the scheduler running
while True:
    schedule.run_pending()
    time.sleep(60)
```

### 2. Make.com Integration

Set up Make.com workflows for social media automation:

**2.1 Property Posting Workflow**:
1. **Trigger**: New property added to Google Sheets
2. **Filter**: Property has image and price
3. **Format**: Create Instagram post content
4. **Action**: Post to Instagram
5. **Log**: Record posting activity

**2.2 Lead Capture Workflow**:
1. **Trigger**: Instagram comment or DM
2. **Process**: Extract contact information
3. **Action**: Add to CRM (HubSpot/Airtable)
4. **Follow-up**: Send automated response

### 3. Monitoring and Alerts

```python
# monitoring/alerts.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class AlertSystem:
    def __init__(self, smtp_server, email, password):
        self.smtp_server = smtp_server
        self.email = email
        self.password = password
    
    def send_alert(self, subject, message, recipients):
        msg = MIMEMultipart()
        msg['From'] = self.email
        msg['To'] = ', '.join(recipients)
        msg['Subject'] = subject
        
        msg.attach(MIMEText(message, 'plain'))
        
        server = smtplib.SMTP(self.smtp_server, 587)
        server.starttls()
        server.login(self.email, self.password)
        server.send_message(msg)
        server.quit()
    
    def check_system_health(self):
        issues = []
        
        # Check API response time
        if self.check_api_response_time() > 5:
            issues.append("API response time > 5 seconds")
        
        # Check data freshness
        if self.check_data_age() > 24:
            issues.append("Data is more than 24 hours old")
        
        # Check scraper status
        failed_scrapers = self.check_scraper_status()
        if failed_scrapers:
            issues.append(f"Failed scrapers: {', '.join(failed_scrapers)}")
        
        if issues:
            self.send_alert(
                "System Health Alert",
                "\n".join(issues),
                ["your-email@example.com"]
            )
```

---

