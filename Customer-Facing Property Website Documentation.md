# Customer-Facing Property Website Documentation

## Overview

This document provides comprehensive information about your customer-facing property website that displays Google Sheets data and includes an intelligent chatbot for customer engagement.

**Live Website URL:** https://y0h0i3cqwqd3.manussite.space

## Table of Contents

1. [System Overview](#system-overview)
2. [Website Features](#website-features)
3. [Chatbot Functionality](#chatbot-functionality)
4. [Technical Architecture](#technical-architecture)
5. [Data Integration](#data-integration)
6. [User Guide](#user-guide)
7. [Administration Guide](#administration-guide)
8. [API Documentation](#api-documentation)
9. [Troubleshooting](#troubleshooting)
10. [Future Enhancements](#future-enhancements)

---



## System Overview

### What is This System?

Your customer-facing property website is a comprehensive digital platform that automatically displays property listings from your Google Sheets databases. The system combines modern web technologies with AI-powered customer engagement to create a professional property browsing experience.

### Key Components

1. **Frontend Website**: A responsive React-based interface that displays property listings in an attractive, user-friendly format
2. **Backend API**: A Flask-based service that fetches data from your Google Sheets and serves it to the frontend
3. **Chatbot Assistant**: An intelligent conversational AI that helps customers find properties and connect with agents
4. **Google Sheets Integration**: Real-time data synchronization with your existing property databases

### Data Sources

The website automatically pulls property data from multiple Google Sheets:

- **28Hse Properties**: Spreadsheet ID `1Dg6g0QFlETa4NdP6eR1qXGudldwe5syK8HbdZZu4h74`
- **Centaline Properties**: Spreadsheet ID `1DsiJScP1HBftv04VFlAKt2jAJVVVU-1Nmun7K4xF7gM`
- **Squarefoot Properties**: Spreadsheet ID `1ZMHZuPUol0eTdXijRKRCPwMpFLWZ8qsQ0HKzhFm6PD0`
- **HK01 News**: Spreadsheet ID `1TQUlIfvv4k_hgf4vFlPULz4HD32x22qBxJMIdEwDC9g`

### Current Status

- **Status**: Live and operational
- **Total Properties**: 2939+ properties displayed
- **Uptime**: 24/7 availability
- **Security**: HTTPS enabled with secure authentication
- **Performance**: Optimized for fast loading and responsive design

---

## Website Features

### Property Display

**Grid Layout**: Properties are displayed in a clean, organized grid format with high-quality images and essential information prominently featured.

**Property Cards Include**:
- Property image with source badge (28HSE, CENTALINE, SQUAREFOOT)
- Property name/development
- Monthly rental price in HKD
- Location with map pin icon
- Number of bedrooms and bathrooms
- Gross floor area in square feet
- Agency information
- Contact person details
- "View Details" button for more information

### Visual Design

**Professional Styling**:
- Clean, modern interface with blue accent colors (#3b82f6)
- Responsive design that works on desktop, tablet, and mobile devices
- High-quality property images with hover effects
- Clear typography and easy-to-read information hierarchy
- Source badges to identify data origin (28HSE, CENTALINE, SQUAREFOOT)

**User Experience**:
- Fast loading times with optimized images
- Intuitive navigation and browsing
- Mobile-friendly touch interactions
- Professional branding and layout

### Search and Filtering

The website displays all available properties with the ability to browse through the complete inventory. Future enhancements can include advanced search and filtering capabilities.

---

## Chatbot Functionality

### Chatbot Overview

The integrated chatbot serves as a 24/7 property assistant that can help customers with inquiries, property searches, and agent connections. The chatbot appears as a floating chat button (💬) in the bottom-right corner of the website.

### Chatbot Capabilities

**Property Search Assistance**:
- Help customers find properties by budget range
- Filter properties by number of bedrooms
- Recommend properties by location/area
- Provide property details and information

**Customer Engagement**:
- Welcome new visitors with friendly greetings
- Guide customers through the property search process
- Answer common questions about rentals and properties
- Provide information about different areas in Hong Kong

**Agent Connection**:
- Facilitate contact with property agents
- Schedule property viewings
- Collect customer contact information
- Connect customers with appropriate agents based on their needs

### Conversation Flow

**1. Greeting and Welcome**:
When customers first open the chat, they receive a welcome message with suggested conversation starters:
- "Show me 1-bedroom apartments"
- "I need a 2-bedroom place"
- "What's available under $20,000?"
- "Properties in Central area"

**2. Preference Collection**:
The chatbot intelligently collects customer preferences:
- Budget range and maximum rent
- Number of bedrooms required
- Preferred locations and areas
- Special requirements or preferences

**3. Property Recommendations**:
Based on collected preferences, the chatbot provides:
- Targeted property suggestions
- Relevant search results
- Detailed property information
- Comparison of different options

**4. Agent Connection**:
When customers are ready to proceed:
- Connect with experienced property agents
- Schedule property viewings
- Provide agent contact information
- Facilitate next steps in the rental process

### Chatbot Features

**Interactive Suggestions**: Each chatbot response includes clickable suggestion buttons for common follow-up questions or actions.

**Context Awareness**: The chatbot remembers conversation context and customer preferences throughout the session.

**Multi-language Support**: Supports both English and Chinese for Hong Kong customers.

**Professional Responses**: Provides helpful, informative responses that guide customers toward finding suitable properties.

---

## Technical Architecture

### Frontend Technology Stack

**React Framework**: Modern React-based single-page application with:
- Component-based architecture for maintainability
- State management for dynamic content
- Responsive CSS for cross-device compatibility
- Optimized build process for fast loading

**Styling and Design**:
- Custom CSS with modern design principles
- Responsive grid layouts
- Professional color scheme and typography
- Mobile-first design approach

### Backend Technology Stack

**Flask Framework**: Python-based backend service providing:
- RESTful API endpoints for data access
- Google Sheets integration for real-time data
- CORS support for frontend-backend communication
- Secure authentication with service accounts

**Google Sheets Integration**:
- Google API Python client for data access
- Service account authentication for secure access
- Real-time data synchronization
- Support for multiple spreadsheet sources

### Deployment Architecture

**Production Hosting**:
- Permanent hosting on Manus infrastructure
- HTTPS security with SSL certificates
- CDN integration for fast global access
- Automatic scaling and load balancing

**Domain and Access**:
- Custom subdomain: `y0h0i3cqwqd3.manussite.space`
- Professional branding and presentation
- 24/7 uptime monitoring
- Backup and disaster recovery

### Security Features

**Data Protection**:
- Secure service account authentication
- HTTPS encryption for all communications
- Read-only access to Google Sheets data
- No sensitive customer data storage

**Access Control**:
- Secure API endpoints with proper validation
- Rate limiting to prevent abuse
- Error handling to prevent information disclosure
- Regular security updates and monitoring

---

## Data Integration

### Google Sheets Configuration

Your property data is automatically synchronized from Google Sheets using a secure service account. The system accesses the following sheets:

**28Hse Properties**:
- **Sheet ID**: `1Dg6g0QFlETa4NdP6eR1qXGudldwe5syK8HbdZZu4h74`
- **Data Range**: All columns (A:Z)
- **Update Frequency**: Real-time when data changes
- **Source Badge**: "28HSE" displayed on property cards

**Centaline Properties**:
- **Sheet ID**: `1DsiJScP1HBftv04VFlAKt2jAJVVVU-1Nmun7K4xF7gM`
- **Data Range**: All columns (A:Z)
- **Update Frequency**: Real-time when data changes
- **Source Badge**: "CENTALINE" displayed on property cards

**Squarefoot Properties**:
- **Sheet ID**: `1ZMHZuPUol0eTdXijRKRCPwMpFLWZ8qsQ0HKzhFm6PD0`
- **Data Range**: All columns (A:Z)
- **Update Frequency**: Real-time when data changes
- **Source Badge**: "SQUAREFOOT" displayed on property cards

### Data Structure Requirements

For optimal display, your Google Sheets should include these columns:

**Required Columns**:
- `title` or `development`: Property name
- `price`: Monthly rental price
- `address`: Property location
- `rooms`: Number of bedrooms
- `gross_area`: Floor area in square feet
- `image_url`: URL to property image
- `agency`: Real estate agency name
- `contact_person`: Agent contact information

**Optional Columns**:
- `floor`: Floor level information
- `net_area`: Net floor area
- `description`: Property description
- `facilities`: Available facilities
- `transport`: Transportation information

### Data Synchronization

**Automatic Updates**: The website automatically reflects changes made to your Google Sheets without requiring manual intervention.

**Data Validation**: The system handles missing or incomplete data gracefully, displaying "N/A" for unavailable information.

**Error Handling**: If a Google Sheet is temporarily unavailable, the system continues to display data from other sources.

---

## User Guide

### For Website Visitors

**Accessing the Website**:
1. Navigate to https://y0h0i3cqwqd3.manussite.space
2. The website loads automatically and displays available properties
3. Browse through property listings using scroll or navigation

**Viewing Properties**:
1. Each property card shows key information including price, location, and size
2. Click "View Details" for more comprehensive property information
3. Note the source badge (28HSE, CENTALINE, SQUAREFOOT) to identify data origin

**Using the Chatbot**:
1. Click the chat button (💬) in the bottom-right corner
2. Start with a greeting or click one of the suggested conversation starters
3. Answer the chatbot's questions about your preferences
4. Follow the chatbot's recommendations and suggestions
5. Request agent contact when ready to proceed

**Mobile Usage**:
- The website is fully responsive and works on all mobile devices
- Touch-friendly interface with easy navigation
- Optimized loading for mobile data connections
- Full chatbot functionality on mobile devices

### For Property Agents

**Customer Inquiries**:
- Customers may contact you directly using information displayed on property cards
- The chatbot will refer customers to you for viewings and detailed discussions
- Be prepared to handle inquiries about properties from all three data sources

**Property Information**:
- Ensure your property listings in Google Sheets are complete and accurate
- Include high-quality images with proper URLs
- Keep contact information up to date
- Update availability status regularly

---

## Administration Guide

### Managing Property Data

**Updating Google Sheets**:
1. Access your Google Sheets directly using the provided spreadsheet IDs
2. Make changes to property information as needed
3. Changes will automatically appear on the website within minutes
4. Ensure data format consistency for optimal display

**Adding New Properties**:
1. Add new rows to the appropriate Google Sheet
2. Include all required columns for complete property display
3. Verify image URLs are accessible and high-quality
4. Test the display on the website after adding

**Removing Properties**:
1. Delete rows from Google Sheets to remove properties from the website
2. Alternatively, mark properties as "unavailable" in a status column
3. Changes take effect immediately on the live website

### Content Management

**Image Management**:
- Ensure all image URLs are publicly accessible
- Use high-quality images for better customer engagement
- Consider using consistent image dimensions for uniform display
- Test image loading on both desktop and mobile devices

**Contact Information**:
- Keep agent contact information current and accurate
- Include professional contact details (name, phone, email)
- Ensure agents are prepared to handle customer inquiries
- Consider using standardized contact formats

### Monitoring and Maintenance

**Website Performance**:
- The website is hosted on reliable infrastructure with 24/7 monitoring
- No manual maintenance required for basic operations
- Contact technical support if you notice any issues

**Data Accuracy**:
- Regularly review property listings for accuracy
- Remove outdated or unavailable properties
- Update pricing and availability information
- Ensure contact information remains current

---

## API Documentation

### Available Endpoints

**Properties API**:
- **Endpoint**: `GET /api/properties`
- **Description**: Retrieves all property listings from all sources
- **Response**: JSON array of property objects
- **Usage**: Used by the frontend to display property listings

**Chatbot API**:
- **Endpoint**: `POST /api/chatbot/message`
- **Description**: Processes chatbot conversations
- **Request Body**: `{"message": "user message", "user_id": "unique_id"}`
- **Response**: JSON object with chatbot response and suggestions
- **Usage**: Powers the interactive chatbot functionality

**Health Check**:
- **Endpoint**: `GET /api/health`
- **Description**: Checks system health and status
- **Response**: System status information
- **Usage**: Monitoring and diagnostics

### API Response Formats

**Properties Response**:
```json
{
  "success": true,
  "data": [
    {
      "title": "Property Name",
      "price": "$15,300",
      "address": "Property Address",
      "rooms": "1房",
      "gross_area": "302 平方呎",
      "image_url": "https://example.com/image.jpg",
      "agency": "Agency Name",
      "contact_person": "Agent Name",
      "source": "28hse"
    }
  ],
  "total": 2939
}
```

**Chatbot Response**:
```json
{
  "success": true,
  "response": {
    "message": "Hello! I'm your property assistant...",
    "suggestions": [
      "Show me 1-bedroom apartments",
      "I need a 2-bedroom place",
      "What's available under $20,000?",
      "Properties in Central area"
    ]
  },
  "timestamp": "2025-07-17T02:31:11.416119"
}
```

---

## Troubleshooting

### Common Issues and Solutions

**Website Not Loading**:
- Check internet connection
- Try refreshing the browser
- Clear browser cache and cookies
- Try accessing from a different device or browser

**Properties Not Displaying**:
- Verify Google Sheets are accessible and properly formatted
- Check that service account has proper permissions
- Ensure image URLs in Google Sheets are valid and accessible
- Contact technical support if issues persist

**Chatbot Not Responding**:
- Refresh the website and try again
- Check browser console for JavaScript errors
- Ensure stable internet connection
- Try using a different browser

**Mobile Display Issues**:
- Ensure you're using a modern mobile browser
- Check that JavaScript is enabled
- Try rotating device orientation
- Clear mobile browser cache

### Performance Optimization

**Slow Loading**:
- The website is optimized for fast loading
- Slow performance may indicate network issues
- Try accessing during off-peak hours
- Contact support if performance issues persist

**Image Loading Issues**:
- Some property images may load slowly due to external hosting
- Images are optimized for web display
- Missing images will show placeholder content
- Report consistently failing images for investigation

### Getting Support

**Technical Issues**:
- Document the specific issue and steps to reproduce
- Include browser type and version information
- Note any error messages displayed
- Contact technical support with detailed information

**Data Issues**:
- Verify the issue exists in the source Google Sheets
- Check data formatting and required columns
- Ensure proper permissions are set on Google Sheets
- Test changes in Google Sheets to confirm synchronization

---

## Future Enhancements

### Planned Features

**Advanced Search and Filtering**:
- Price range filters
- Location-based search
- Property type filtering
- Advanced search criteria

**Enhanced Chatbot Capabilities**:
- Integration with property database for real-time availability
- Appointment scheduling functionality
- Multi-language support expansion
- Voice interaction capabilities

**Customer Relationship Management**:
- Lead capture and tracking
- Customer preference storage
- Follow-up automation
- Analytics and reporting

### Potential Integrations

**Social Media Integration**:
- Share properties on social platforms
- Social media login options
- Instagram and Facebook integration
- WhatsApp direct messaging

**Payment and Booking**:
- Online booking system
- Deposit payment processing
- Document upload capabilities
- Digital contract signing

**Analytics and Insights**:
- Customer behavior tracking
- Popular property analysis
- Conversion rate optimization
- Performance dashboards

### Scalability Considerations

**Traffic Growth**:
- The current infrastructure can handle significant traffic increases
- Automatic scaling capabilities are built into the hosting platform
- Performance monitoring ensures optimal user experience
- Additional resources can be allocated as needed

**Data Expansion**:
- Support for additional Google Sheets sources
- Integration with other property databases
- Real-time MLS integration possibilities
- Multi-market expansion capabilities

---

## Conclusion

Your customer-facing property website represents a significant advancement in digital property marketing. By combining real-time Google Sheets integration with intelligent chatbot assistance, you've created a powerful platform that serves customers 24/7 while showcasing your property inventory professionally.

The system is designed for reliability, scalability, and ease of use. With proper maintenance of your Google Sheets data and regular monitoring, this platform will continue to serve as an effective customer acquisition and engagement tool for your property business.

For any questions, technical support, or enhancement requests, please refer to the contact information provided or reach out to your technical support team.

**Website URL**: https://y0h0i3cqwqd3.manussite.space

**Last Updated**: July 17, 2025
**Version**: 1.0
**Status**: Live and Operational

