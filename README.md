# 28Hse Scraper Flask App

## Overview
This Flask application scrapes rental listings from 28hse.com and provides them via a REST API.

## Endpoints
- `GET /` - Health check endpoint
- `GET /health` - Service health status
- `GET /run` - Execute scraper and return JSON results

## Local Development
```bash
cd 28hse-scraper
source venv/bin/activate
pip install -r requirements.txt
python src/main.py
```

## Deployment to Render

### Prerequisites
1. Create a GitHub repository for this project
2. Push the code to GitHub
3. Create a Render account

### Steps
1. Connect your GitHub repository to Render
2. Create a new Web Service
3. Use the following settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python src/main.py`
   - **Environment**: Python 3
   - **Plan**: Free (or paid for better performance)

### Environment Variables
Set these in Render dashboard:
- `PORT`: 5000 (automatically set by Render)
- `PYTHON_VERSION`: 3.11.0

### Make.com Integration
Once deployed, use the Render URL in your Make.com scenarios:
- Health check: `https://your-app-name.onrender.com/health`
- Run scraper: `https://your-app-name.onrender.com/run`

## Features
- Headless Chrome scraping with Selenium
- Comprehensive data extraction (title, price, areas, agent info, images)
- JSON API response format
- Error handling and logging
- Production-ready configuration

## Data Structure
The scraper returns listings with the following fields:
- title, price, development, saleable_area, gross_area
- floor, rooms, address, agency, contact_person
- listing_url, scraped_at timestamp
- image_url (up to 20 images per listing)

## Scheduling
For automated scraping, set up Make.com scenarios to call the `/run` endpoint on a schedule (e.g., daily or hourly).

