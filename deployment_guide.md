# Deployment Guide for Property Scrapers

## Overview
This guide covers deploying the 28Hse and Squarefoot scrapers to Render and integrating them with Make.com for automated operation.

## Step 1: Prepare GitHub Repositories

### For 28Hse Scraper:
1. Create a new GitHub repository named `28hse-scraper`
2. Upload the contents of the `28hse-scraper` folder
3. Ensure the following files are included:
   - `src/main.py` (Flask application entry point)
   - `src/scraper.py` (Scraping logic)
   - `src/routes/scraper.py` (API routes)
   - `requirements.txt` (Python dependencies)
   - `render.yaml` (Render configuration)
   - `README.md` (Documentation)

### For Squarefoot Scraper:
1. Create a new GitHub repository named `squarefoot-scraper`
2. Upload the contents of the `squarefoot-scraper` folder
3. Ensure the same file structure as above

## Step 2: Deploy to Render

### Deploy 28Hse Scraper:
1. Log in to [Render](https://render.com)
2. Click "New" → "Web Service"
3. Connect your GitHub account and select the `28hse-scraper` repository
4. Configure the service:
   - **Name**: `28hse-scraper`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python src/main.py`
   - **Plan**: Free (or paid for better performance)
5. Click "Create Web Service"
6. Wait for deployment to complete
7. Note the deployed URL (e.g., `https://28hse-scraper.onrender.com`)

### Deploy Squarefoot Scraper:
1. Repeat the same process for the `squarefoot-scraper` repository
2. Use the name `squarefoot-scraper`
3. Note the deployed URL (e.g., `https://squarefoot-scraper.onrender.com`)

## Step 3: Test Deployed Services

### Test 28Hse Scraper:
- Health check: `GET https://28hse-scraper.onrender.com/health`
- Run scraper: `GET https://28hse-scraper.onrender.com/run`

### Test Squarefoot Scraper:
- Health check: `GET https://squarefoot-scraper.onrender.com/health`
- Run scraper: `GET https://squarefoot-scraper.onrender.com/run`

## Step 4: Set Up Make.com Automation

### Create Make.com Scenarios:

#### Scenario 1: 28Hse Data Collection
1. **Trigger**: Schedule (e.g., daily at 9 AM)
2. **HTTP Module**: 
   - URL: `https://28hse-scraper.onrender.com/run`
   - Method: GET
3. **Data Processing**: Parse JSON response
4. **Storage**: Save to database/Google Sheets/Airtable
5. **Notification**: Send status update

#### Scenario 2: Squarefoot Data Collection
1. **Trigger**: Schedule (e.g., daily at 10 AM)
2. **HTTP Module**: 
   - URL: `https://squarefoot-scraper.onrender.com/run`
   - Method: GET
3. **Data Processing**: Parse JSON response
4. **Storage**: Save to database/Google Sheets/Airtable
5. **Notification**: Send status update

#### Scenario 3: Content Generation & Posting
1. **Trigger**: New data available (webhook or schedule)
2. **Data Retrieval**: Get latest listings from storage
3. **AI Processing**: Generate captions and process images
4. **Instagram Posting**: Post to Instagram with generated content
5. **Tracking**: Log post metrics

## Step 5: Monitoring and Maintenance

### Health Monitoring:
- Set up Make.com scenarios to check health endpoints regularly
- Configure alerts for service downtime
- Monitor scraping success rates

### Performance Optimization:
- Monitor Render service metrics
- Upgrade to paid plans if needed for better performance
- Optimize scraping frequency based on data freshness needs

### Error Handling:
- Implement retry logic in Make.com scenarios
- Set up error notifications
- Regular review of scraping logs

## Step 6: Data Flow Integration

### Current State:
- HK01 News Scraper: ✅ Deployed and integrated
- Centaline Scraper: ✅ Deployed and integrated
- 28Hse Scraper: 🔄 Ready for deployment
- Squarefoot Scraper: 🔄 Ready for deployment

### Next Steps:
1. Deploy both new scrapers
2. Update Make.com scenarios to include new data sources
3. Implement unified data storage
4. Set up AI content enrichment pipeline
5. Integrate with CRM system

## Important Notes:

### Render Free Tier Limitations:
- Services may sleep after 15 minutes of inactivity
- 750 hours per month limit
- Consider upgrading for production use

### Chrome/Selenium in Production:
- Render supports Chrome and ChromeDriver
- Headless mode is essential for server deployment
- Monitor memory usage as Selenium can be resource-intensive

### Rate Limiting:
- Implement delays between requests to avoid being blocked
- Monitor target websites for anti-bot measures
- Consider rotating user agents and IP addresses if needed

This deployment strategy ensures all scrapers are consistently available and can be orchestrated through Make.com for automated data collection and content generation.

