# Complete Automation Ecosystem Deployment and Testing Guide

## Overview

This guide provides step-by-step instructions for deploying and testing the complete AI-driven property agency automation ecosystem. The system consists of multiple interconnected services that work together to create a seamless content-to-lead funnel.

## System Architecture

The automation ecosystem consists of the following components:

### Core Services
1. **28Hse Scraper** - Flask app for scraping 28Hse rental listings
2. **Squarefoot Scraper** - Flask app for scraping Squarefoot rental listings  
3. **AI Content Enrichment Service** - AI-powered content generation and image processing
4. **Property CRM System** - Lead management and analytics platform

### Existing Services (Already Deployed)
1. **HK01 News Scraper** - Property news content automation
2. **Centaline Scraper** - Rental listing scraper with image generation

### Integration Layer
1. **Make.com Workflows** - Orchestration and automation scenarios
2. **Instagram API Integration** - Social media posting and engagement
3. **WhatsApp Business API** - Lead communication and nurturing

## Pre-Deployment Checklist

### Environment Setup
- [ ] GitHub repositories created for each service
- [ ] Render account configured and ready
- [ ] Make.com account with sufficient operations quota
- [ ] Instagram Business account with API access
- [ ] WhatsApp Business API access (optional but recommended)
- [ ] Cloudinary account for image hosting
- [ ] OpenAI API key for content generation

### Required Environment Variables
```bash
# AI Content Enrichment Service
OPENAI_API_KEY=your_openai_api_key
OPENAI_API_BASE=https://api.openai.com/v1
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

# All Services
PORT=5000  # Automatically set by Render
```

## Deployment Instructions

### Step 1: Deploy 28Hse Scraper

#### 1.1 Prepare Repository
```bash
# Create GitHub repository: 28hse-scraper
# Upload contents of /home/ubuntu/28hse-scraper/
```

#### 1.2 Deploy to Render
1. Log in to [Render](https://render.com)
2. Click "New" → "Web Service"
3. Connect GitHub and select `28hse-scraper` repository
4. Configure service:
   - **Name**: `28hse-scraper`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python src/main.py`
   - **Plan**: Free (upgrade for production)
5. Deploy and note the URL: `https://28hse-scraper.onrender.com`

#### 1.3 Test Deployment
```bash
# Health check
curl https://28hse-scraper.onrender.com/health

# Test scraping (may take 2-3 minutes)
curl https://28hse-scraper.onrender.com/run
```

### Step 2: Deploy Squarefoot Scraper

#### 2.1 Prepare Repository
```bash
# Create GitHub repository: squarefoot-scraper
# Upload contents of /home/ubuntu/squarefoot-scraper/
```

#### 2.2 Deploy to Render
1. Follow same process as 28Hse scraper
2. Use repository: `squarefoot-scraper`
3. Note URL: `https://squarefoot-scraper.onrender.com`

#### 2.3 Test Deployment
```bash
# Health check
curl https://squarefoot-scraper.onrender.com/health

# Test scraping
curl https://squarefoot-scraper.onrender.com/run
```

### Step 3: Deploy AI Content Enrichment Service

#### 3.1 Prepare Repository
```bash
# Create GitHub repository: ai-content-enrichment
# Upload contents of /home/ubuntu/ai-content-enrichment/
```

#### 3.2 Deploy to Render
1. Deploy following same process
2. **Important**: Set environment variables in Render dashboard:
   - `OPENAI_API_KEY`
   - `CLOUDINARY_CLOUD_NAME`
   - `CLOUDINARY_API_KEY`
   - `CLOUDINARY_API_SECRET`
3. Note URL: `https://ai-content-enrichment.onrender.com`

#### 3.3 Test Deployment
```bash
# Health check
curl https://ai-content-enrichment.onrender.com/health

# Test with sample data
curl https://ai-content-enrichment.onrender.com/test/sample-enrichment
```

### Step 4: Deploy Property CRM System

#### 4.1 Prepare Repository
```bash
# Create GitHub repository: property-crm
# Upload contents of /home/ubuntu/property-crm/
```

#### 4.2 Deploy to Render
1. Deploy following same process
2. Note URL: `https://property-crm.onrender.com`

#### 4.3 Test Deployment
```bash
# Health check
curl https://property-crm.onrender.com/health

# Test dashboard
curl https://property-crm.onrender.com/analytics/dashboard
```

## Make.com Workflow Configuration

### Scenario 1: Data Collection Hub

#### Configuration Steps:
1. **Create New Scenario** in Make.com
2. **Add Scheduled Trigger**:
   - Schedule: Every 4 hours during business hours
   - Timezone: Hong Kong (UTC+8)

3. **Add HTTP Modules** for each scraper:
   
   **28Hse Module:**
   - URL: `https://28hse-scraper.onrender.com/run`
   - Method: GET
   - Timeout: 300 seconds
   
   **Squarefoot Module:**
   - URL: `https://squarefoot-scraper.onrender.com/run`
   - Method: GET
   - Timeout: 300 seconds
   
   **Existing Scrapers:**
   - Include your existing Centaline and HK01 scrapers

4. **Add Data Processing Module**:
   - Combine data from all sources
   - Remove duplicates
   - Validate data quality

5. **Add Storage Module**:
   - Store in Google Sheets, Airtable, or database
   - Include timestamp and source information

#### Error Handling:
- Add error handling for each HTTP module
- Send notifications for failed scrapers
- Continue processing even if one scraper fails

### Scenario 2: AI Content Enrichment Pipeline

#### Configuration Steps:
1. **Trigger**: New data available from Scenario 1
2. **HTTP Module - AI Enrichment**:
   - URL: `https://ai-content-enrichment.onrender.com/process/scraper-data`
   - Method: POST
   - Headers: `Content-Type: application/json`
   - Body:
   ```json
   {
     "source": "{{source}}",
     "listings": {{listings_array}},
     "options": {
       "caption_style": "engaging",
       "image_style": "modern",
       "create_collage": false
     }
   }
   ```

3. **Response Processing**:
   - Extract `instagram_posts` array
   - Store enriched content
   - Update posting queue

### Scenario 3: Instagram Publishing

#### Configuration Steps:
1. **Trigger**: New enriched content available
2. **Content Selection Logic**:
   - Prioritize high-scoring properties
   - Ensure content variety
   - Check posting schedule

3. **Instagram API Module**:
   - Use Instagram Graph API
   - Post image with caption
   - Track post ID and metrics

4. **CRM Integration**:
   - URL: `https://property-crm.onrender.com/properties`
   - Method: POST
   - Store property and post information

### Scenario 4: Lead Capture

#### Configuration Steps:
1. **Instagram Webhook Trigger**:
   - Configure Instagram webhook for comments and DMs
   - Filter for property-related inquiries

2. **CRM Lead Creation**:
   - URL: `https://property-crm.onrender.com/leads/instagram-inquiry`
   - Method: POST
   - Body:
   ```json
   {
     "instagram_handle": "{{sender_username}}",
     "message": "{{message_text}}",
     "post_id": "{{post_id}}",
     "property_id": "{{property_id}}"
   }
   ```

3. **Agent Notification**:
   - Send notification to assigned agent
   - Include lead details and response suggestions

### Scenario 5: WhatsApp Integration

#### Configuration Steps:
1. **WhatsApp Webhook Trigger**:
   - Configure WhatsApp Business API webhook
   - Filter for new conversations

2. **CRM Lead Creation**:
   - URL: `https://property-crm.onrender.com/leads/whatsapp-inquiry`
   - Method: POST
   - Body:
   ```json
   {
     "whatsapp_number": "{{sender_number}}",
     "name": "{{sender_name}}",
     "message": "{{message_text}}"
   }
   ```

3. **Automated Response**:
   - Send welcome message
   - Provide property information
   - Schedule follow-up

## Testing Procedures

### Unit Testing

#### Test Each Service Individually:

**28Hse Scraper:**
```bash
# Test health
curl https://28hse-scraper.onrender.com/health

# Test scraping
curl -X GET https://28hse-scraper.onrender.com/run
# Expected: JSON array of property listings
```

**Squarefoot Scraper:**
```bash
# Test health
curl https://squarefoot-scraper.onrender.com/health

# Test scraping
curl -X GET https://squarefoot-scraper.onrender.com/run
# Expected: JSON array of property listings
```

**AI Content Enrichment:**
```bash
# Test health
curl https://ai-content-enrichment.onrender.com/health

# Test sample enrichment
curl https://ai-content-enrichment.onrender.com/test/sample-enrichment
# Expected: Enriched property data with AI-generated content
```

**Property CRM:**
```bash
# Test health
curl https://property-crm.onrender.com/health

# Test dashboard
curl https://property-crm.onrender.com/analytics/dashboard
# Expected: Dashboard metrics (may be empty initially)
```

### Integration Testing

#### Test 1: Data Flow from Scraper to Enrichment
```bash
# 1. Get data from scraper
SCRAPER_DATA=$(curl -s https://28hse-scraper.onrender.com/run)

# 2. Send to enrichment service
curl -X POST https://ai-content-enrichment.onrender.com/process/scraper-data \
  -H "Content-Type: application/json" \
  -d "{
    \"source\": \"28hse\",
    \"listings\": $SCRAPER_DATA,
    \"options\": {
      \"caption_style\": \"engaging\",
      \"image_style\": \"modern\"
    }
  }"
# Expected: Enriched listings with Instagram-ready content
```

#### Test 2: Lead Creation and Management
```bash
# 1. Create test lead
curl -X POST https://property-crm.onrender.com/leads/instagram-inquiry \
  -H "Content-Type: application/json" \
  -d '{
    "instagram_handle": "@test_user",
    "message": "Interested in 2-bedroom apartment",
    "post_id": "test_post_123",
    "property_id": "test_property_456"
  }'
# Expected: New lead created with automatic scoring

# 2. Check lead was created
curl https://property-crm.onrender.com/leads
# Expected: Array containing the test lead
```

#### Test 3: Agent Assignment
```bash
# 1. Create test agent
curl -X POST https://property-crm.onrender.com/agents \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Agent",
    "email": "test@example.com",
    "specialization_areas": ["Central", "Admiralty"],
    "specialization_types": ["apartment"]
  }'

# 2. Auto-assign leads
curl -X POST https://property-crm.onrender.com/agents/auto-assign
# Expected: Unassigned leads get assigned to available agents
```

### End-to-End Testing

#### Complete Workflow Test:
1. **Data Collection**: Verify scrapers collect fresh data
2. **Content Enrichment**: Confirm AI processing generates quality content
3. **Social Media Posting**: Test Instagram posting (use test account)
4. **Lead Capture**: Simulate Instagram inquiry and verify CRM capture
5. **Agent Assignment**: Confirm leads are properly assigned
6. **Analytics**: Verify metrics are tracked and displayed

#### Performance Testing:
- **Load Testing**: Test with multiple concurrent requests
- **Response Time**: Measure API response times under load
- **Error Handling**: Test behavior when services are unavailable
- **Data Quality**: Verify scraped data accuracy and completeness

## Monitoring and Maintenance

### Health Monitoring Setup

#### Create Monitoring Dashboard:
```bash
# Create monitoring script
cat > monitor_services.sh << 'EOF'
#!/bin/bash

SERVICES=(
  "https://28hse-scraper.onrender.com/health"
  "https://squarefoot-scraper.onrender.com/health"
  "https://ai-content-enrichment.onrender.com/health"
  "https://property-crm.onrender.com/health"
)

for service in "${SERVICES[@]}"; do
  echo "Checking $service"
  response=$(curl -s -o /dev/null -w "%{http_code}" "$service")
  if [ "$response" = "200" ]; then
    echo "✅ Service healthy"
  else
    echo "❌ Service unhealthy (HTTP $response)"
  fi
done
EOF

chmod +x monitor_services.sh
```

#### Set Up Alerts:
- Configure Make.com scenario to run health checks every 15 minutes
- Send notifications for service failures
- Monitor response times and error rates

### Performance Optimization

#### Render Service Optimization:
- Monitor service metrics in Render dashboard
- Upgrade to paid plans for better performance
- Consider using persistent disks for data storage

#### Database Optimization:
- Regular SQLite database maintenance
- Consider PostgreSQL for production
- Implement data archiving for old records

#### API Rate Limiting:
- Monitor OpenAI API usage and costs
- Implement caching for repeated requests
- Consider batch processing for efficiency

### Troubleshooting Guide

#### Common Issues:

**Service Won't Start:**
- Check Render build logs
- Verify requirements.txt is complete
- Ensure environment variables are set

**Scraper Returns Empty Data:**
- Check target website structure changes
- Verify Chrome/ChromeDriver compatibility
- Test locally with same configuration

**AI Enrichment Fails:**
- Verify OpenAI API key and quota
- Check Cloudinary configuration
- Test with simpler content first

**CRM Database Issues:**
- Check SQLite file permissions
- Verify database schema creation
- Test with fresh database

**Make.com Workflow Errors:**
- Check API endpoint URLs
- Verify request format and headers
- Test individual modules separately

## Security Considerations

### API Security:
- Implement rate limiting for production
- Add authentication for sensitive endpoints
- Validate all input data
- Use HTTPS for all communications

### Data Protection:
- Encrypt sensitive customer data
- Implement data retention policies
- Regular security audits
- Backup and recovery procedures

### Access Control:
- Limit Make.com webhook access
- Secure API keys and credentials
- Monitor for unauthorized access
- Regular credential rotation

## Scaling Considerations

### Horizontal Scaling:
- Load balancing for high traffic
- Database replication for read scaling
- CDN for image delivery
- Microservices architecture

### Vertical Scaling:
- Upgrade Render service plans
- Optimize database queries
- Implement caching layers
- Monitor resource utilization

### Cost Optimization:
- Monitor API usage costs
- Optimize image processing
- Implement efficient data storage
- Regular cost analysis and optimization

This comprehensive deployment and testing guide ensures that your AI-driven property agency automation ecosystem is properly deployed, thoroughly tested, and ready for production use. The modular architecture allows for easy maintenance and scaling as your business grows.

