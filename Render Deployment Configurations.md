# Render Deployment Configurations

## Service Configurations for Render Deployment

### 1. 28Hse Scraper Service

**Repository**: `28hse-scraper`
**Service Type**: Web Service

```yaml
# render.yaml
services:
  - type: web
    name: 28hse-scraper
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python src/main.py
    plan: free
    envVars:
      - key: PORT
        value: 5000
```

**Manual Configuration**:
- **Name**: `28hse-scraper`
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python src/main.py`
- **Auto-Deploy**: Yes

### 2. Squarefoot Scraper Service

**Repository**: `squarefoot-scraper`
**Service Type**: Web Service

```yaml
# render.yaml
services:
  - type: web
    name: squarefoot-scraper
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python src/main.py
    plan: free
    envVars:
      - key: PORT
        value: 5000
```

**Manual Configuration**:
- **Name**: `squarefoot-scraper`
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python src/main.py`
- **Auto-Deploy**: Yes

### 3. AI Content Enrichment Service

**Repository**: `ai-content-enrichment`
**Service Type**: Web Service

```yaml
# render.yaml
services:
  - type: web
    name: ai-content-enrichment
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python src/main.py
    plan: free
    envVars:
      - key: PORT
        value: 5000
      - key: OPENAI_API_KEY
        sync: false
      - key: OPENAI_API_BASE
        value: https://api.openai.com/v1
      - key: CLOUDINARY_CLOUD_NAME
        sync: false
      - key: CLOUDINARY_API_KEY
        sync: false
      - key: CLOUDINARY_API_SECRET
        sync: false
```

**Manual Configuration**:
- **Name**: `ai-content-enrichment`
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python src/main.py`
- **Auto-Deploy**: Yes

**Environment Variables** (Set in Render Dashboard):
```
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_API_BASE=https://api.openai.com/v1
CLOUDINARY_CLOUD_NAME=your_cloudinary_cloud_name
CLOUDINARY_API_KEY=your_cloudinary_api_key
CLOUDINARY_API_SECRET=your_cloudinary_api_secret
```

### 4. Property CRM Service

**Repository**: `property-crm`
**Service Type**: Web Service

```yaml
# render.yaml
services:
  - type: web
    name: property-crm
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python src/main.py
    plan: free
    envVars:
      - key: PORT
        value: 5000
```

**Manual Configuration**:
- **Name**: `property-crm`
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python src/main.py`
- **Auto-Deploy**: Yes

## Deployment Steps

### Step 1: Prepare GitHub Repositories

For each service, create a GitHub repository and upload the corresponding files:

#### 28Hse Scraper Repository Structure:
```
28hse-scraper/
├── src/
│   ├── main.py
│   ├── scraper.py
│   └── routes/
│       └── scraper.py
├── requirements.txt
├── render.yaml
└── README.md
```

#### Squarefoot Scraper Repository Structure:
```
squarefoot-scraper/
├── src/
│   ├── main.py
│   ├── scraper.py
│   └── routes/
│       └── scraper.py
├── requirements.txt
├── render.yaml
└── README.md
```

#### AI Content Enrichment Repository Structure:
```
ai-content-enrichment/
├── src/
│   ├── main.py
│   ├── services/
│   │   ├── image_processor.py
│   │   ├── text_generator.py
│   │   └── content_enrichment.py
│   └── routes/
│       └── enrichment.py
├── requirements.txt
├── render.yaml
└── README.md
```

#### Property CRM Repository Structure:
```
property-crm/
├── src/
│   ├── main.py
│   ├── models/
│   │   └── lead.py
│   ├── routes/
│   │   ├── leads.py
│   │   ├── agents.py
│   │   └── analytics.py
│   └── database/
├── requirements.txt
├── render.yaml
└── README.md
```

### Step 2: Deploy Services to Render

#### For Each Service:

1. **Log in to Render**: Go to [render.com](https://render.com)

2. **Create New Web Service**:
   - Click "New" → "Web Service"
   - Connect your GitHub account
   - Select the repository

3. **Configure Service**:
   - Use the configurations provided above
   - Set environment variables (especially for AI service)
   - Choose appropriate plan (Free for testing, Starter+ for production)

4. **Deploy**:
   - Click "Create Web Service"
   - Monitor build logs for any issues
   - Wait for deployment to complete

5. **Test Deployment**:
   - Access the service URL
   - Test health endpoint: `https://your-service.onrender.com/health`

### Step 3: Service URLs

After deployment, you'll have the following service URLs:

```
28Hse Scraper: https://28hse-scraper.onrender.com
Squarefoot Scraper: https://squarefoot-scraper.onrender.com
AI Content Enrichment: https://ai-content-enrichment.onrender.com
Property CRM: https://property-crm.onrender.com
```

## Environment Variables Configuration

### AI Content Enrichment Service

**Required Environment Variables**:

1. **OpenAI Configuration**:
   ```
   OPENAI_API_KEY=sk-your-openai-api-key-here
   OPENAI_API_BASE=https://api.openai.com/v1
   ```

2. **Cloudinary Configuration**:
   ```
   CLOUDINARY_CLOUD_NAME=your-cloud-name
   CLOUDINARY_API_KEY=your-api-key
   CLOUDINARY_API_SECRET=your-api-secret
   ```

**How to Set in Render**:
1. Go to your service dashboard
2. Click "Environment" tab
3. Add each environment variable
4. Click "Save Changes"
5. Service will automatically redeploy

### Optional Environment Variables

For enhanced functionality, you can add:

```
# For enhanced logging
LOG_LEVEL=INFO

# For custom configurations
MAX_BATCH_SIZE=20
DEFAULT_CAPTION_STYLE=engaging
DEFAULT_IMAGE_STYLE=modern
```

## Monitoring and Health Checks

### Health Check Endpoints

Each service provides a health check endpoint:

```bash
# 28Hse Scraper
curl https://28hse-scraper.onrender.com/health

# Squarefoot Scraper
curl https://squarefoot-scraper.onrender.com/health

# AI Content Enrichment
curl https://ai-content-enrichment.onrender.com/health

# Property CRM
curl https://property-crm.onrender.com/health
```

Expected Response:
```json
{
  "status": "healthy",
  "service": "service-name",
  "version": "1.0.0"
}
```

### Render Dashboard Monitoring

Monitor the following metrics in Render dashboard:

1. **Service Status**: Running/Stopped/Failed
2. **Build Status**: Success/Failed
3. **Response Time**: Average response time
4. **Memory Usage**: RAM consumption
5. **CPU Usage**: Processing load
6. **Request Volume**: Number of requests

### Automated Monitoring

Set up automated monitoring using Make.com:

```json
{
  "scenario": "Health Check Monitor",
  "trigger": "Schedule (every 15 minutes)",
  "actions": [
    {
      "type": "HTTP Request",
      "url": "https://28hse-scraper.onrender.com/health",
      "method": "GET"
    },
    {
      "type": "Condition",
      "condition": "HTTP Status != 200",
      "true_action": "Send Alert Email"
    }
  ]
}
```

## Troubleshooting

### Common Deployment Issues

#### Build Failures:
1. **Missing Dependencies**: Ensure `requirements.txt` is complete
2. **Python Version**: Render uses Python 3.7+ by default
3. **File Paths**: Use relative paths in imports

#### Runtime Errors:
1. **Port Binding**: Ensure app listens on `0.0.0.0:PORT`
2. **Environment Variables**: Verify all required vars are set
3. **Database Issues**: Check SQLite file permissions

#### Performance Issues:
1. **Cold Starts**: Free tier services sleep after 15 minutes
2. **Memory Limits**: Free tier has 512MB RAM limit
3. **Request Timeouts**: Default 30-second timeout

### Service-Specific Issues

#### Scraper Services:
- **Chrome Issues**: Render includes Chrome and ChromeDriver
- **Selenium Timeouts**: Increase timeout values for slow pages
- **Memory Usage**: Selenium can be memory-intensive

#### AI Content Enrichment:
- **OpenAI Rate Limits**: Monitor API usage and implement backoff
- **Image Processing**: Large images may cause memory issues
- **Cloudinary Limits**: Monitor upload quota

#### Property CRM:
- **Database Growth**: SQLite file size limits
- **Concurrent Access**: SQLite limitations with multiple users

## Production Considerations

### Scaling Recommendations

#### For Production Use:
1. **Upgrade Plans**: Move from Free to Starter or Professional
2. **Database**: Consider PostgreSQL for CRM service
3. **Caching**: Implement Redis for frequently accessed data
4. **CDN**: Use Cloudinary or similar for image delivery

#### Performance Optimization:
1. **Connection Pooling**: For database connections
2. **Request Batching**: Group API calls when possible
3. **Async Processing**: For long-running tasks
4. **Load Balancing**: For high-traffic scenarios

### Security Enhancements

#### For Production:
1. **API Authentication**: Add JWT or API key authentication
2. **Rate Limiting**: Implement request rate limiting
3. **Input Validation**: Strict validation on all inputs
4. **HTTPS Only**: Ensure all communications use HTTPS
5. **Secret Management**: Use Render's secret management

### Backup and Recovery

#### Data Backup:
1. **Database Exports**: Regular CRM database backups
2. **Configuration Backup**: Save environment variables
3. **Code Backup**: Maintain GitHub repositories
4. **Monitoring Data**: Export analytics and logs

#### Disaster Recovery:
1. **Service Redundancy**: Deploy to multiple regions
2. **Data Replication**: Backup critical data off-site
3. **Recovery Procedures**: Document recovery steps
4. **Testing**: Regular disaster recovery testing

This comprehensive deployment configuration ensures that all services are properly deployed, monitored, and maintained for reliable operation of your AI-driven property agency automation ecosystem.

