# Property CRM System

## Overview
A comprehensive Customer Relationship Management (CRM) system specifically designed for property agencies. This system manages leads, agents, interactions, and provides detailed analytics for property marketing and sales operations.

## Features

### Lead Management
- **Comprehensive Lead Tracking**: Capture leads from multiple sources (Instagram, WhatsApp, direct contact)
- **Intelligent Lead Scoring**: Automatic scoring based on engagement, contact completeness, and behavior
- **Lead Qualification**: Track leads through the entire funnel from initial contact to conversion
- **Property Interest Tracking**: Monitor which properties generate the most interest and inquiries

### Agent Management
- **Agent Profiles**: Detailed agent information with specializations and performance metrics
- **Workload Management**: Track agent capacity and automatically distribute leads
- **Performance Analytics**: Monitor response times, conversion rates, and lead quality
- **Intelligent Assignment**: Auto-assign leads to the best available agent based on specialization and workload

### Interaction Tracking
- **Multi-Channel Communication**: Track interactions across Instagram, WhatsApp, phone, email, and in-person meetings
- **Conversation History**: Complete interaction timeline for each lead
- **Automated Responses**: Support for automated responses with human escalation
- **Follow-up Management**: Schedule and track follow-up activities

### Analytics and Reporting
- **Dashboard Metrics**: Real-time overview of key performance indicators
- **Conversion Funnel**: Track leads through each stage of the sales process
- **Source Performance**: Analyze which lead sources generate the highest quality prospects
- **Agent Comparison**: Compare agent performance across multiple metrics
- **Property Performance**: Identify which properties generate the most interest and conversions

## API Endpoints

### Lead Management
- `GET /leads` - Get all leads with filtering and pagination
- `POST /leads` - Create a new lead
- `GET /leads/{id}` - Get specific lead details
- `PUT /leads/{id}` - Update lead information
- `GET /leads/{id}/interactions` - Get all interactions for a lead
- `POST /leads/{id}/interactions` - Create new interaction
- `POST /leads/instagram-inquiry` - Handle Instagram inquiries
- `POST /leads/whatsapp-inquiry` - Handle WhatsApp inquiries

### Agent Management
- `GET /agents` - Get all agents
- `POST /agents` - Create new agent
- `GET /agents/{id}` - Get specific agent details
- `PUT /agents/{id}` - Update agent information
- `GET /agents/{id}/leads` - Get agent's assigned leads
- `GET /agents/{id}/performance` - Get agent performance metrics
- `GET /agents/{id}/workload` - Get agent current workload
- `POST /agents/assign-lead` - Manually assign lead to agent
- `POST /agents/auto-assign` - Auto-assign unassigned leads

### Analytics
- `GET /analytics/dashboard` - Get dashboard metrics
- `GET /analytics/leads-trend` - Get leads trend over time
- `GET /analytics/source-performance` - Get performance by lead source
- `GET /analytics/agent-comparison` - Get agent performance comparison
- `GET /analytics/property-performance` - Get property listing performance
- `GET /analytics/funnel` - Get conversion funnel metrics
- `GET /analytics/lead-scoring` - Get lead scoring analysis
- `GET /analytics/export` - Export analytics data

### Health Check
- `GET /health` - Service health status

## Data Models

### Lead
- Contact information (name, phone, email, Instagram, WhatsApp)
- Source tracking (Instagram post, WhatsApp, direct)
- Lead qualification (status, priority, score)
- Property interests (budget, areas, property type, bedrooms)
- Agent assignment
- Timestamps and follow-up scheduling

### Agent
- Personal information and contact details
- Specializations (areas, property types, languages)
- Performance metrics (total leads, conversions, response time)
- Workload management (active status, maximum leads)

### Interaction
- Interaction details (type, channel, direction)
- Content (subject, message, attachments)
- Agent assignment and automation status
- Outcomes and follow-up actions

### Property
- Property details (title, development, address, specifications)
- Pricing and area information
- Source tracking and listing URLs
- Agent information
- Social media performance metrics

## Integration with Automation Ecosystem

### Make.com Integration
The CRM system is designed to integrate seamlessly with Make.com automation workflows:

#### Instagram Lead Capture
```
Instagram Webhook → CRM API (/leads/instagram-inquiry) → Agent Assignment → Response Automation
```

#### WhatsApp Lead Management
```
WhatsApp Webhook → CRM API (/leads/whatsapp-inquiry) → Lead Scoring → Agent Notification
```

#### Lead Scoring and Assignment
```
New Lead → Automatic Scoring → Best Agent Assignment → Follow-up Scheduling
```

### API Integration Examples

#### Create Lead from Instagram Inquiry
```json
POST /leads/instagram-inquiry
{
  "instagram_handle": "@potential_tenant",
  "message": "Interested in the Tai Koo Shing apartment",
  "post_id": "instagram_post_123",
  "property_id": "property_456"
}
```

#### Handle WhatsApp Inquiry
```json
POST /leads/whatsapp-inquiry
{
  "whatsapp_number": "+85298765432",
  "name": "John Chan",
  "message": "Looking for 2-bedroom apartment in Central"
}
```

#### Get Agent Performance
```json
GET /agents/1/performance?days=30
{
  "success": true,
  "agent": {...},
  "performance": {
    "new_leads": 25,
    "converted_leads": 8,
    "conversion_rate": 32.0,
    "avg_response_time_minutes": 45.5
  }
}
```

## Lead Scoring Algorithm

The system uses an intelligent lead scoring algorithm that evaluates leads based on:

### Contact Information Completeness (0-20 points)
- Phone number: +5 points
- Email address: +5 points
- Full name: +5 points
- WhatsApp number: +5 points

### Engagement Level (0-30 points)
- Detailed message (>50 characters): +10 points
- Budget information provided: +10 points
- Preferred areas specified: +5 points
- Move-in date provided: +5 points

### Interaction History (0-25 points)
- Each interaction: +5 points (max 25)

### Recency (0-15 points)
- Contact within 24 hours: +15 points
- Contact within 3 days: +10 points
- Contact within 7 days: +5 points

### Property Interest Specificity (0-10 points)
- Each specific property of interest: +2 points (max 10)

## Agent Assignment Logic

The system automatically assigns leads to the best available agent based on:

### Specialization Match
- Area specialization match: +20 points
- Property type specialization: +15 points

### Workload Balance
- Fewer current leads: +10 points (scaled)

### Performance History
- Higher conversion rate: +10 points (scaled)

### Availability
- Agent must be active and under maximum lead capacity

## Deployment

### Local Development
```bash
cd property-crm
source venv/bin/activate
pip install -r requirements.txt
python src/main.py
```

### Production Deployment (Render)
1. Create new Web Service on Render
2. Connect GitHub repository
3. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python src/main.py`
   - **Environment**: Python 3
4. Deploy

### Environment Variables
```bash
PORT=5000  # Automatically set by Render
```

## Database Schema

The system uses SQLite for development and can be easily migrated to PostgreSQL for production. Key tables:

- **leads**: Core lead information and tracking
- **agents**: Agent profiles and performance metrics
- **interactions**: Communication history and outcomes
- **properties**: Property listings and performance data

## Security Considerations

- Input validation on all API endpoints
- SQL injection prevention through SQLAlchemy ORM
- Rate limiting recommended for production deployment
- Authentication can be added for multi-tenant usage

## Performance Optimization

- Database indexing on frequently queried fields
- Pagination for large result sets
- Efficient queries with proper joins
- Caching recommendations for high-traffic scenarios

## Monitoring and Maintenance

### Health Monitoring
- `/health` endpoint for service status
- Database connection monitoring
- Performance metrics tracking

### Data Backup
- Regular SQLite database backups
- Export functionality for data migration
- Analytics data export for external analysis

## Future Enhancements

### Planned Features
- Email integration for lead communication
- SMS/WhatsApp API integration for automated responses
- Advanced reporting with charts and visualizations
- Mobile app for agent access
- Integration with property listing platforms
- Machine learning for improved lead scoring

### Scalability Considerations
- Database migration to PostgreSQL
- Redis caching layer
- Microservices architecture
- Load balancing for high availability

This CRM system provides a solid foundation for managing property agency operations while integrating seamlessly with the broader automation ecosystem. The modular design allows for easy extension and customization based on specific business requirements.

