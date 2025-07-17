# Automation & Maintenance Guide
## Property Agency System

This guide covers automation setup, maintenance procedures, and operational best practices for your property agency system.

## Table of Contents

1. [Automation Overview](#automation-overview)
2. [Scraper Automation](#scraper-automation)
3. [Social Media Automation](#social-media-automation)
4. [System Monitoring](#system-monitoring)
5. [Maintenance Procedures](#maintenance-procedures)
6. [Performance Optimization](#performance-optimization)
7. [Troubleshooting](#troubleshooting)
8. [Scaling Strategies](#scaling-strategies)

---

## Automation Overview

### Complete Automation Pipeline

Your property agency system can be fully automated with the following workflow:

```
Data Collection → Processing → Publishing → Lead Management → Follow-up
      ↓              ↓           ↓            ↓              ↓
   Scrapers    → Database → Social Media → CRM System → Automation
```

### Key Automation Components

1. **Data Collection**: Automated scrapers running on schedule
2. **Data Processing**: Cleaning, validation, and enrichment
3. **Content Publishing**: Automated social media posting
4. **Lead Capture**: Automated response to inquiries
5. **CRM Integration**: Automatic lead tracking and follow-up
6. **Monitoring**: Health checks and alerting

---

## Scraper Automation

### 1. Production Scraper Setup

#### 1.1 Robust Scraper Architecture
```python
# scrapers/base/robust_scraper.py
import requests
import time
import random
import logging
from abc import ABC, abstractmethod
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

class RobustScraper(ABC):
    def __init__(self, name, sheet_id, config=None):
        self.name = name
        self.sheet_id = sheet_id
        self.config = config or {}
        self.session = self._create_session()
        self.logger = self._setup_logging()
        self.stats = {
            'start_time': None,
            'end_time': None,
            'properties_found': 0,
            'properties_saved': 0,
            'errors': 0
        }
    
    def _create_session(self):
        """Create a robust HTTP session with retries"""
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
        return session
    
    def _setup_logging(self):
        """Setup logging for the scraper"""
        logger = logging.getLogger(f"scraper_{self.name}")
        logger.setLevel(logging.INFO)
        
        handler = logging.FileHandler(f'/var/log/scraper_{self.name}.log')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    def get_page(self, url, retries=3, delay_range=(1, 3)):
        """Get page with retry logic and rate limiting"""
        for attempt in range(retries):
            try:
                # Random delay to avoid being blocked
                time.sleep(random.uniform(*delay_range))
                
                response = self.session.get(url, timeout=30)
                response.raise_for_status()
                
                self.logger.info(f"Successfully fetched: {url}")
                return response
                
            except requests.exceptions.RequestException as e:
                self.logger.warning(f"Attempt {attempt + 1} failed for {url}: {e}")
                if attempt == retries - 1:
                    self.logger.error(f"Failed to fetch {url} after {retries} attempts")
                    raise e
                time.sleep(random.uniform(2, 5))  # Longer delay between retries
    
    def save_to_sheets(self, properties):
        """Save properties to Google Sheets with error handling"""
        try:
            credentials = Credentials.from_service_account_info(
                json.loads(os.environ['GOOGLE_CREDENTIALS']),
                scopes=['https://www.googleapis.com/auth/spreadsheets']
            )
            gc = gspread.authorize(credentials)
            sheet = gc.open_by_key(self.sheet_id).sheet1
            
            # Get existing data to avoid duplicates
            existing_data = sheet.get_all_records()
            existing_urls = {row.get('listing_url') for row in existing_data}
            
            # Filter out duplicates
            new_properties = [
                prop for prop in properties 
                if prop.get('listing_url') not in existing_urls
            ]
            
            if new_properties:
                # Prepare data for batch insert
                values = []
                for prop in new_properties:
                    row = [
                        prop.get('title', ''),
                        prop.get('price', ''),
                        prop.get('address', ''),
                        prop.get('rooms', ''),
                        prop.get('gross_area', ''),
                        prop.get('image_url', ''),
                        prop.get('listing_url', ''),
                        prop.get('agency', ''),
                        prop.get('contact_person', ''),
                        datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    ]
                    values.append(row)
                
                # Batch insert
                sheet.append_rows(values)
                self.stats['properties_saved'] = len(new_properties)
                self.logger.info(f"Saved {len(new_properties)} new properties")
            else:
                self.logger.info("No new properties to save")
                
        except Exception as e:
            self.logger.error(f"Error saving to sheets: {e}")
            self.stats['errors'] += 1
            raise
    
    @abstractmethod
    def scrape_properties(self):
        """Implement property scraping logic"""
        pass
    
    def run(self):
        """Main scraper execution"""
        self.stats['start_time'] = datetime.now()
        self.logger.info(f"Starting {self.name} scraper")
        
        try:
            properties = self.scrape_properties()
            self.stats['properties_found'] = len(properties)
            
            if properties:
                self.save_to_sheets(properties)
            
            self.stats['end_time'] = datetime.now()
            duration = self.stats['end_time'] - self.stats['start_time']
            
            self.logger.info(f"Scraper completed in {duration.total_seconds():.2f} seconds")
            self.logger.info(f"Stats: {self.stats}")
            
            return self.stats
            
        except Exception as e:
            self.logger.error(f"Scraper failed: {e}")
            self.stats['errors'] += 1
            raise
```

#### 1.2 Deployment with Docker
```dockerfile
# Dockerfile for scrapers
FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Install Chrome for Selenium (if needed)
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable

# Copy scraper code
COPY . .

# Run scraper
CMD ["python", "run_scrapers.py"]
```

```yaml
# docker-compose.yml for scrapers
version: '3.8'
services:
  scraper-28hse:
    build: .
    environment:
      - GOOGLE_CREDENTIALS=${GOOGLE_CREDENTIALS}
      - SCRAPER_NAME=28hse
    volumes:
      - ./logs:/var/log
    restart: unless-stopped
  
  scraper-centaline:
    build: .
    environment:
      - GOOGLE_CREDENTIALS=${GOOGLE_CREDENTIALS}
      - SCRAPER_NAME=centaline
    volumes:
      - ./logs:/var/log
    restart: unless-stopped
```

#### 1.3 Kubernetes Deployment
```yaml
# k8s/scraper-cronjob.yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: property-scrapers
spec:
  schedule: "0 6,12,18 * * *"  # Run 3 times daily
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: scraper
            image: your-registry/property-scraper:latest
            env:
            - name: GOOGLE_CREDENTIALS
              valueFrom:
                secretKeyRef:
                  name: google-credentials
                  key: credentials.json
          restartPolicy: OnFailure
```

### 2. Advanced Scraping Features

#### 2.1 Anti-Detection Measures
```python
class AntiDetectionScraper(RobustScraper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.proxy_pool = self._load_proxy_pool()
        self.user_agents = self._load_user_agents()
    
    def _load_proxy_pool(self):
        """Load rotating proxy pool"""
        return [
            {'http': 'http://proxy1:port', 'https': 'https://proxy1:port'},
            {'http': 'http://proxy2:port', 'https': 'https://proxy2:port'},
            # Add more proxies
        ]
    
    def _load_user_agents(self):
        """Load rotating user agents"""
        return [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
            # Add more user agents
        ]
    
    def get_page(self, url, **kwargs):
        """Enhanced page fetching with anti-detection"""
        # Rotate user agent
        self.session.headers['User-Agent'] = random.choice(self.user_agents)
        
        # Rotate proxy (if available)
        if self.proxy_pool:
            proxy = random.choice(self.proxy_pool)
            self.session.proxies.update(proxy)
        
        # Random delay
        time.sleep(random.uniform(2, 8))
        
        return super().get_page(url, **kwargs)
```

#### 2.2 Data Enrichment
```python
class EnrichedScraper(AntiDetectionScraper):
    def enrich_property_data(self, property_data):
        """Enrich property data with additional information"""
        enriched = property_data.copy()
        
        # Add price per square foot
        if property_data.get('price') and property_data.get('gross_area'):
            try:
                price_num = int(re.sub(r'[^\d]', '', property_data['price']))
                area_num = int(re.sub(r'[^\d]', '', property_data['gross_area']))
                if area_num > 0:
                    enriched['price_per_sqft'] = f"${price_num // area_num:,}"
            except:
                pass
        
        # Add location coordinates (using geocoding API)
        if property_data.get('address'):
            coords = self.geocode_address(property_data['address'])
            if coords:
                enriched['latitude'] = coords['lat']
                enriched['longitude'] = coords['lng']
        
        # Add market analysis
        enriched['market_analysis'] = self.analyze_market_position(property_data)
        
        return enriched
    
    def geocode_address(self, address):
        """Geocode address to coordinates"""
        try:
            # Use Google Maps API or similar
            api_key = os.environ.get('GOOGLE_MAPS_API_KEY')
            if not api_key:
                return None
            
            url = f"https://maps.googleapis.com/maps/api/geocode/json"
            params = {'address': address, 'key': api_key}
            
            response = requests.get(url, params=params)
            data = response.json()
            
            if data['status'] == 'OK' and data['results']:
                location = data['results'][0]['geometry']['location']
                return {'lat': location['lat'], 'lng': location['lng']}
        except:
            pass
        return None
```

---

## Social Media Automation

### 1. Instagram Automation with Make.com

#### 1.1 Webhook Setup
```python
# webhook_handler.py
from flask import Flask, request, jsonify
import json
import requests

app = Flask(__name__)

@app.route('/webhook/new-property', methods=['POST'])
def handle_new_property():
    """Handle new property webhook from Google Sheets"""
    try:
        data = request.json
        
        # Validate required fields
        required_fields = ['title', 'price', 'image_url', 'listing_url']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Format property for Instagram
        instagram_post = format_for_instagram(data)
        
        # Send to Make.com webhook
        make_webhook_url = "https://hook.integromat.com/your-webhook-url"
        response = requests.post(make_webhook_url, json=instagram_post)
        
        if response.status_code == 200:
            return jsonify({'status': 'success'})
        else:
            return jsonify({'error': 'Failed to send to Make.com'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def format_for_instagram(property_data):
    """Format property data for Instagram posting"""
    caption = f"""
🏠 {property_data['title']}
💰 {property_data['price']}/month
📍 {property_data.get('address', 'Hong Kong')}
🛏️ {property_data.get('rooms', 'N/A')}
📐 {property_data.get('gross_area', 'N/A')}

Contact us for viewing! 📞
Link in bio for more details.

#HongKongRental #PropertyRental #RealEstate #HongKongProperty
"""
    
    return {
        'image_url': property_data['image_url'],
        'caption': caption.strip(),
        'listing_url': property_data['listing_url'],
        'property_id': property_data.get('id'),
        'source': property_data.get('source')
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
```

#### 1.2 Make.com Scenario Configuration

**Scenario 1: New Property Posting**
1. **Webhook Trigger**: Receive new property data
2. **Image Processing**: Download and resize image
3. **Content Generation**: Create engaging caption
4. **Instagram Post**: Publish to Instagram
5. **Database Update**: Mark as posted
6. **Slack Notification**: Notify team

**Scenario 2: Lead Capture**
1. **Instagram Trigger**: New comment or DM
2. **Text Analysis**: Extract contact intent
3. **CRM Integration**: Add lead to HubSpot/Airtable
4. **Auto Response**: Send automated reply
5. **Agent Notification**: Alert relevant agent

### 2. WhatsApp Business Integration

```python
# whatsapp_bot.py
from twilio.rest import Client
import os

class WhatsAppBot:
    def __init__(self):
        self.client = Client(
            os.environ['TWILIO_ACCOUNT_SID'],
            os.environ['TWILIO_AUTH_TOKEN']
        )
        self.from_number = 'whatsapp:+14155238886'  # Twilio sandbox
    
    def send_property_details(self, to_number, property_data):
        """Send property details via WhatsApp"""
        message = f"""
🏠 *{property_data['title']}*

💰 Price: {property_data['price']}/month
📍 Location: {property_data['address']}
🛏️ Rooms: {property_data['rooms']}
📐 Area: {property_data['gross_area']}

🏢 Agency: {property_data['agency']}
👤 Contact: {property_data['contact_person']}

View more details: {property_data['listing_url']}

Would you like to schedule a viewing? Reply with "YES" to connect with our agent.
"""
        
        self.client.messages.create(
            body=message,
            from_=self.from_number,
            to=f'whatsapp:{to_number}'
        )
    
    def handle_incoming_message(self, from_number, message_body):
        """Handle incoming WhatsApp messages"""
        message_lower = message_body.lower()
        
        if 'viewing' in message_lower or 'yes' in message_lower:
            # Connect with agent
            response = "Great! I'll connect you with one of our agents. They will contact you within 30 minutes to schedule a viewing."
            self.notify_agent(from_number, message_body)
        
        elif 'price' in message_lower:
            # Price inquiry
            response = "I can help you find properties within your budget. What's your preferred price range?"
        
        elif 'location' in message_lower:
            # Location inquiry
            response = "Which area are you interested in? We have properties across Hong Kong Island, Kowloon, and New Territories."
        
        else:
            # General response
            response = "Thanks for your interest! How can I help you find your perfect property? You can ask about price, location, or schedule a viewing."
        
        self.client.messages.create(
            body=response,
            from_=self.from_number,
            to=from_number
        )
    
    def notify_agent(self, customer_number, inquiry):
        """Notify agent about new lead"""
        agent_number = self.get_available_agent()
        
        message = f"""
🚨 *New Lead Alert*

Customer: {customer_number}
Inquiry: {inquiry}
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Please contact the customer within 30 minutes.
"""
        
        self.client.messages.create(
            body=message,
            from_=self.from_number,
            to=f'whatsapp:{agent_number}'
        )
```

---

## System Monitoring

### 1. Comprehensive Monitoring Setup

#### 1.1 Health Check System
```python
# monitoring/health_checker.py
import requests
import psutil
import gspread
from datetime import datetime, timedelta
import json

class SystemHealthChecker:
    def __init__(self, config):
        self.config = config
        self.alerts = []
    
    def check_api_health(self):
        """Check API endpoint health"""
        try:
            response = requests.get(f"{self.config['api_url']}/api/health", timeout=10)
            if response.status_code == 200:
                data = response.json()
                return {
                    'status': 'healthy',
                    'response_time': response.elapsed.total_seconds(),
                    'properties_count': data.get('total_properties', 0)
                }
            else:
                return {'status': 'unhealthy', 'error': f'HTTP {response.status_code}'}
        except Exception as e:
            return {'status': 'unhealthy', 'error': str(e)}
    
    def check_database_health(self):
        """Check Google Sheets database health"""
        try:
            gc = gspread.service_account()
            
            sheets_health = {}
            for name, sheet_id in self.config['sheets'].items():
                try:
                    sheet = gc.open_by_key(sheet_id).sheet1
                    data = sheet.get_all_records()
                    
                    sheets_health[name] = {
                        'status': 'healthy',
                        'record_count': len(data),
                        'last_updated': self.get_last_update_time(data)
                    }
                except Exception as e:
                    sheets_health[name] = {
                        'status': 'unhealthy',
                        'error': str(e)
                    }
            
            return sheets_health
        except Exception as e:
            return {'status': 'unhealthy', 'error': str(e)}
    
    def check_scraper_health(self):
        """Check scraper execution health"""
        scraper_health = {}
        
        for scraper in ['28hse', 'centaline', 'squarefoot']:
            log_file = f'/var/log/scraper_{scraper}.log'
            try:
                with open(log_file, 'r') as f:
                    lines = f.readlines()
                
                # Check last execution
                last_run = self.parse_last_run_time(lines)
                if last_run:
                    hours_since = (datetime.now() - last_run).total_seconds() / 3600
                    status = 'healthy' if hours_since < 24 else 'stale'
                else:
                    status = 'unknown'
                
                scraper_health[scraper] = {
                    'status': status,
                    'last_run': last_run.isoformat() if last_run else None,
                    'hours_since_last_run': hours_since if last_run else None
                }
                
            except Exception as e:
                scraper_health[scraper] = {
                    'status': 'error',
                    'error': str(e)
                }
        
        return scraper_health
    
    def check_system_resources(self):
        """Check system resource usage"""
        return {
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_percent': psutil.disk_usage('/').percent,
            'load_average': psutil.getloadavg() if hasattr(psutil, 'getloadavg') else None
        }
    
    def run_all_checks(self):
        """Run all health checks"""
        health_report = {
            'timestamp': datetime.now().isoformat(),
            'api': self.check_api_health(),
            'database': self.check_database_health(),
            'scrapers': self.check_scraper_health(),
            'system': self.check_system_resources()
        }
        
        # Check for alerts
        self.evaluate_alerts(health_report)
        
        return health_report
    
    def evaluate_alerts(self, health_report):
        """Evaluate health report and generate alerts"""
        # API alerts
        if health_report['api']['status'] != 'healthy':
            self.alerts.append(f"API is unhealthy: {health_report['api'].get('error')}")
        
        # Database alerts
        for name, status in health_report['database'].items():
            if isinstance(status, dict) and status.get('status') != 'healthy':
                self.alerts.append(f"Database {name} is unhealthy: {status.get('error')}")
        
        # Scraper alerts
        for name, status in health_report['scrapers'].items():
            if status['status'] == 'stale':
                self.alerts.append(f"Scraper {name} hasn't run in {status['hours_since_last_run']:.1f} hours")
        
        # System resource alerts
        system = health_report['system']
        if system['cpu_percent'] > 80:
            self.alerts.append(f"High CPU usage: {system['cpu_percent']:.1f}%")
        if system['memory_percent'] > 80:
            self.alerts.append(f"High memory usage: {system['memory_percent']:.1f}%")
        if system['disk_percent'] > 80:
            self.alerts.append(f"High disk usage: {system['disk_percent']:.1f}%")
```

#### 1.2 Alerting System
```python
# monitoring/alerting.py
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class AlertManager:
    def __init__(self, config):
        self.config = config
    
    def send_email_alert(self, subject, message, recipients):
        """Send email alert"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.config['smtp']['from_email']
            msg['To'] = ', '.join(recipients)
            msg['Subject'] = subject
            
            msg.attach(MIMEText(message, 'plain'))
            
            server = smtplib.SMTP(self.config['smtp']['server'], self.config['smtp']['port'])
            server.starttls()
            server.login(self.config['smtp']['username'], self.config['smtp']['password'])
            server.send_message(msg)
            server.quit()
            
            return True
        except Exception as e:
            print(f"Failed to send email alert: {e}")
            return False
    
    def send_slack_alert(self, message, channel='#alerts'):
        """Send Slack alert"""
        try:
            webhook_url = self.config['slack']['webhook_url']
            payload = {
                'channel': channel,
                'text': message,
                'username': 'Property System Monitor'
            }
            
            response = requests.post(webhook_url, json=payload)
            return response.status_code == 200
        except Exception as e:
            print(f"Failed to send Slack alert: {e}")
            return False
    
    def send_sms_alert(self, message, phone_numbers):
        """Send SMS alert via Twilio"""
        try:
            from twilio.rest import Client
            
            client = Client(
                self.config['twilio']['account_sid'],
                self.config['twilio']['auth_token']
            )
            
            for number in phone_numbers:
                client.messages.create(
                    body=message,
                    from_=self.config['twilio']['from_number'],
                    to=number
                )
            
            return True
        except Exception as e:
            print(f"Failed to send SMS alert: {e}")
            return False
    
    def process_alerts(self, alerts, severity='medium'):
        """Process and send alerts based on severity"""
        if not alerts:
            return
        
        message = f"Property System Alert ({severity.upper()}):\n\n"
        message += "\n".join(f"• {alert}" for alert in alerts)
        message += f"\n\nTime: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        # Send based on severity
        if severity == 'critical':
            self.send_email_alert("CRITICAL: Property System Alert", message, self.config['alerts']['critical_emails'])
            self.send_sms_alert(message, self.config['alerts']['critical_phones'])
            self.send_slack_alert(f"🚨 CRITICAL ALERT:\n{message}")
        
        elif severity == 'high':
            self.send_email_alert("HIGH: Property System Alert", message, self.config['alerts']['high_emails'])
            self.send_slack_alert(f"⚠️ HIGH ALERT:\n{message}")
        
        else:  # medium/low
            self.send_slack_alert(f"ℹ️ ALERT:\n{message}")
```

### 2. Performance Monitoring

#### 2.1 Metrics Collection
```python
# monitoring/metrics.py
import time
import psutil
import requests
from datetime import datetime
import json

class MetricsCollector:
    def __init__(self, config):
        self.config = config
        self.metrics = []
    
    def collect_api_metrics(self):
        """Collect API performance metrics"""
        endpoints = [
            '/api/properties',
            '/api/health',
            '/api/chatbot/message'
        ]
        
        for endpoint in endpoints:
            start_time = time.time()
            try:
                response = requests.get(f"{self.config['api_url']}{endpoint}", timeout=30)
                response_time = time.time() - start_time
                
                metric = {
                    'timestamp': datetime.now().isoformat(),
                    'type': 'api_performance',
                    'endpoint': endpoint,
                    'response_time': response_time,
                    'status_code': response.status_code,
                    'success': response.status_code == 200
                }
                
                if endpoint == '/api/properties' and response.status_code == 200:
                    data = response.json()
                    metric['properties_count'] = len(data.get('data', []))
                
                self.metrics.append(metric)
                
            except Exception as e:
                self.metrics.append({
                    'timestamp': datetime.now().isoformat(),
                    'type': 'api_performance',
                    'endpoint': endpoint,
                    'error': str(e),
                    'success': False
                })
    
    def collect_system_metrics(self):
        """Collect system performance metrics"""
        self.metrics.append({
            'timestamp': datetime.now().isoformat(),
            'type': 'system_performance',
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_percent': psutil.disk_usage('/').percent,
            'network_io': dict(psutil.net_io_counters()._asdict()),
            'disk_io': dict(psutil.disk_io_counters()._asdict())
        })
    
    def save_metrics(self):
        """Save metrics to file or database"""
        timestamp = datetime.now().strftime('%Y%m%d')
        filename = f'/var/log/metrics_{timestamp}.json'
        
        with open(filename, 'a') as f:
            for metric in self.metrics:
                f.write(json.dumps(metric) + '\n')
        
        self.metrics.clear()
```

---

