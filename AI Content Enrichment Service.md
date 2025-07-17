# AI Content Enrichment Service

## Overview
This Flask application provides AI-powered content enrichment for property listings and news articles. It generates Instagram-ready captions, processes images with overlays, and creates engaging social media content.

## Features

### Text Generation
- **Instagram Captions**: AI-generated captions in Traditional Chinese with multiple styles (engaging, professional, casual)
- **Property Summaries**: Concise summaries for image overlays
- **Hashtag Generation**: Relevant hashtags for better discoverability
- **News Summaries**: Engaging social media content for property news

### Image Processing
- **Property Overlays**: Add property information overlays to images with multiple styles (modern, classic, minimal)
- **Image Collages**: Create multi-image collages from property photos
- **Cloudinary Integration**: Automatic image hosting and optimization
- **Instagram-ready Formats**: 1080x1080 square format for optimal Instagram display

### Content Enrichment
- **Batch Processing**: Enrich multiple listings simultaneously
- **Flexible Options**: Customizable styles and formats
- **Error Handling**: Graceful fallbacks for failed enrichments
- **Statistics**: Detailed processing statistics and success rates

## API Endpoints

### Health Check
- `GET /health` - Service health status

### Property Enrichment
- `POST /enrich/property` - Enrich a single property listing
- `POST /enrich/properties/batch` - Enrich multiple properties in batch
- `POST /process/scraper-data` - Process data directly from scrapers

### News Enrichment
- `POST /enrich/news` - Enrich news articles for social media

### Instagram Integration
- `POST /generate/instagram-post` - Generate Instagram-ready post data

### Testing
- `GET /test/sample-enrichment` - Test with sample data

## Request/Response Examples

### Enrich Property Listing
```json
POST /enrich/property
{
  "property_data": {
    "title": "太古城 3房2廳 海景單位",
    "price": "45000",
    "development": "太古城",
    "saleable_area": "1200呎",
    "rooms": "3房",
    "address": "香港島太古城",
    "image_url": "https://example.com/image.jpg"
  },
  "options": {
    "caption_style": "engaging",
    "image_style": "modern",
    "create_collage": false
  }
}
```

Response:
```json
{
  "success": true,
  "enriched_data": {
    "title": "太古城 3房2廳 海景單位",
    "price": "45000",
    "ai_caption": "🏠 太古城海景3房單位！\n💰 租金: $45,000\n📍 實用面積1200呎...",
    "ai_summary": "太古城\n$45,000\n面積: 1200呎",
    "ai_hashtags": ["#租屋", "#香港租屋", "#太古城"],
    "ai_enriched_image": "https://res.cloudinary.com/...",
    "enrichment_metadata": {...}
  }
}
```

### Process Scraper Data
```json
POST /process/scraper-data
{
  "source": "28hse",
  "listings": [...],
  "options": {
    "caption_style": "engaging",
    "image_style": "modern"
  }
}
```

Response:
```json
{
  "success": true,
  "instagram_posts": [
    {
      "image_url": "https://res.cloudinary.com/...",
      "caption": "🏠 太古城海景3房單位！...",
      "listing_url": "https://...",
      "post_type": "property_listing"
    }
  ],
  "stats": {
    "total_listings": 10,
    "successful_enrichments": 9,
    "success_rate": 0.9,
    "instagram_posts_created": 9
  }
}
```

## Environment Variables

Required environment variables:
```bash
# OpenAI API (for text generation)
OPENAI_API_KEY=your_openai_api_key
OPENAI_API_BASE=https://api.openai.com/v1

# Cloudinary (for image hosting)
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

# Flask
PORT=5000
```

## Local Development
```bash
cd ai-content-enrichment
source venv/bin/activate
pip install -r requirements.txt

# Set environment variables
export OPENAI_API_KEY=your_key
export CLOUDINARY_CLOUD_NAME=your_name
export CLOUDINARY_API_KEY=your_key
export CLOUDINARY_API_SECRET=your_secret

python src/main.py
```

## Deployment to Render

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Use these settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python src/main.py`
   - **Environment**: Python 3
4. Set environment variables in Render dashboard
5. Deploy

## Integration with Make.com

### Workflow Example:
1. **Trigger**: New data from scrapers (28Hse, Squarefoot, Centaline)
2. **HTTP Request**: POST to `/process/scraper-data` with scraper data
3. **Response Processing**: Extract `instagram_posts` array
4. **Instagram Posting**: Use Instagram API to post each enriched listing
5. **Tracking**: Log post metrics and engagement

### Make.com Scenario Structure:
```
Scraper Webhook → AI Enrichment → Instagram API → Analytics
```

## Content Styles

### Caption Styles:
- **Engaging**: Exciting, emoji-rich, creates urgency
- **Professional**: Factual, informative, business-focused
- **Casual**: Friendly, approachable, conversational

### Image Styles:
- **Modern**: Gradient overlay, clean typography
- **Classic**: Solid overlay, traditional layout
- **Minimal**: Simple price badge, clean design

## Error Handling

The service includes comprehensive error handling:
- Graceful fallbacks for AI generation failures
- Default captions and summaries when AI is unavailable
- Image processing fallbacks
- Detailed error reporting in batch operations

## Performance Considerations

- **Rate Limiting**: OpenAI API has rate limits
- **Image Processing**: Can be memory-intensive
- **Batch Size**: Recommend processing 10-20 listings per batch
- **Caching**: Consider implementing caching for repeated requests

## Monitoring

Monitor these metrics:
- Enrichment success rate
- Image processing success rate
- API response times
- Error rates by type
- Cloudinary usage and costs

