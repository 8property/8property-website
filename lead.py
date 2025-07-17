from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class Lead(db.Model):
    __tablename__ = 'leads'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Contact Information
    name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    instagram_handle = db.Column(db.String(50))
    whatsapp_number = db.Column(db.String(20))
    
    # Lead Source and Context
    source = db.Column(db.String(50), nullable=False)  # instagram, whatsapp, direct, etc.
    source_post_id = db.Column(db.String(100))  # Instagram post ID that generated lead
    source_property_id = db.Column(db.String(100))  # Property listing that generated lead
    original_message = db.Column(db.Text)
    
    # Lead Qualification
    status = db.Column(db.String(20), default='new')  # new, contacted, qualified, viewing_scheduled, applied, converted, lost
    priority = db.Column(db.String(10), default='medium')  # low, medium, high, urgent
    score = db.Column(db.Integer, default=0)  # Lead scoring 0-100
    
    # Property Interests
    interested_properties = db.Column(db.Text)  # JSON array of property IDs
    budget_min = db.Column(db.Integer)
    budget_max = db.Column(db.Integer)
    preferred_areas = db.Column(db.Text)  # JSON array of area names
    property_type = db.Column(db.String(50))  # apartment, house, studio, etc.
    bedrooms = db.Column(db.Integer)
    move_in_date = db.Column(db.Date)
    
    # Agent Assignment
    assigned_agent_id = db.Column(db.Integer, db.ForeignKey('agents.id'))
    assigned_agent = db.relationship('Agent', backref='leads')
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_contact_at = db.Column(db.DateTime)
    next_follow_up_at = db.Column(db.DateTime)
    
    # Metadata
    tags = db.Column(db.Text)  # JSON array of tags
    notes = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Lead {self.id}: {self.name or self.instagram_handle or "Unknown"}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
            'instagram_handle': self.instagram_handle,
            'whatsapp_number': self.whatsapp_number,
            'source': self.source,
            'source_post_id': self.source_post_id,
            'source_property_id': self.source_property_id,
            'original_message': self.original_message,
            'status': self.status,
            'priority': self.priority,
            'score': self.score,
            'interested_properties': json.loads(self.interested_properties) if self.interested_properties else [],
            'budget_min': self.budget_min,
            'budget_max': self.budget_max,
            'preferred_areas': json.loads(self.preferred_areas) if self.preferred_areas else [],
            'property_type': self.property_type,
            'bedrooms': self.bedrooms,
            'move_in_date': self.move_in_date.isoformat() if self.move_in_date else None,
            'assigned_agent_id': self.assigned_agent_id,
            'assigned_agent': self.assigned_agent.to_dict() if self.assigned_agent else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'last_contact_at': self.last_contact_at.isoformat() if self.last_contact_at else None,
            'next_follow_up_at': self.next_follow_up_at.isoformat() if self.next_follow_up_at else None,
            'tags': json.loads(self.tags) if self.tags else [],
            'notes': self.notes
        }
    
    def update_score(self):
        """Calculate and update lead score based on various factors"""
        score = 0
        
        # Contact information completeness (0-20 points)
        if self.phone: score += 5
        if self.email: score += 5
        if self.name: score += 5
        if self.whatsapp_number: score += 5
        
        # Engagement level (0-30 points)
        if self.original_message and len(self.original_message) > 50: score += 10
        if self.budget_min and self.budget_max: score += 10
        if self.preferred_areas: score += 5
        if self.move_in_date: score += 5
        
        # Interaction history (0-25 points)
        interactions = Interaction.query.filter_by(lead_id=self.id).count()
        score += min(interactions * 5, 25)
        
        # Recency (0-15 points)
        if self.last_contact_at:
            days_since_contact = (datetime.utcnow() - self.last_contact_at).days
            if days_since_contact <= 1: score += 15
            elif days_since_contact <= 3: score += 10
            elif days_since_contact <= 7: score += 5
        
        # Property interest specificity (0-10 points)
        if self.interested_properties:
            properties = json.loads(self.interested_properties)
            score += min(len(properties) * 2, 10)
        
        self.score = min(score, 100)
        return self.score

class Agent(db.Model):
    __tablename__ = 'agents'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    whatsapp_number = db.Column(db.String(20))
    
    # Specializations
    specialization_areas = db.Column(db.Text)  # JSON array of areas
    specialization_types = db.Column(db.Text)  # JSON array of property types
    languages = db.Column(db.Text)  # JSON array of languages
    
    # Performance metrics
    total_leads = db.Column(db.Integer, default=0)
    converted_leads = db.Column(db.Integer, default=0)
    avg_response_time = db.Column(db.Integer, default=0)  # in minutes
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    max_leads = db.Column(db.Integer, default=50)  # Maximum concurrent leads
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Agent {self.id}: {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'whatsapp_number': self.whatsapp_number,
            'specialization_areas': json.loads(self.specialization_areas) if self.specialization_areas else [],
            'specialization_types': json.loads(self.specialization_types) if self.specialization_types else [],
            'languages': json.loads(self.languages) if self.languages else [],
            'total_leads': self.total_leads,
            'converted_leads': self.converted_leads,
            'conversion_rate': self.converted_leads / self.total_leads if self.total_leads > 0 else 0,
            'avg_response_time': self.avg_response_time,
            'is_active': self.is_active,
            'max_leads': self.max_leads,
            'current_leads': len(self.leads),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def can_take_lead(self):
        """Check if agent can take more leads"""
        current_active_leads = Lead.query.filter_by(
            assigned_agent_id=self.id
        ).filter(
            Lead.status.in_(['new', 'contacted', 'qualified', 'viewing_scheduled'])
        ).count()
        
        return self.is_active and current_active_leads < self.max_leads

class Interaction(db.Model):
    __tablename__ = 'interactions'
    
    id = db.Column(db.Integer, primary_key=True)
    lead_id = db.Column(db.Integer, db.ForeignKey('leads.id'), nullable=False)
    lead = db.relationship('Lead', backref='interactions')
    
    # Interaction details
    type = db.Column(db.String(20), nullable=False)  # message, call, email, meeting, viewing
    channel = db.Column(db.String(20))  # instagram, whatsapp, phone, email, in_person
    direction = db.Column(db.String(10))  # inbound, outbound
    
    # Content
    subject = db.Column(db.String(200))
    message = db.Column(db.Text)
    attachments = db.Column(db.Text)  # JSON array of attachment URLs
    
    # Metadata
    agent_id = db.Column(db.Integer, db.ForeignKey('agents.id'))
    agent = db.relationship('Agent', backref='interactions')
    is_automated = db.Column(db.Boolean, default=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    scheduled_at = db.Column(db.DateTime)  # For scheduled interactions
    completed_at = db.Column(db.DateTime)
    
    # Outcomes
    outcome = db.Column(db.String(50))  # interested, not_interested, viewing_scheduled, etc.
    next_action = db.Column(db.String(100))
    follow_up_date = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<Interaction {self.id}: {self.type} with Lead {self.lead_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'lead_id': self.lead_id,
            'type': self.type,
            'channel': self.channel,
            'direction': self.direction,
            'subject': self.subject,
            'message': self.message,
            'attachments': json.loads(self.attachments) if self.attachments else [],
            'agent_id': self.agent_id,
            'agent': self.agent.to_dict() if self.agent else None,
            'is_automated': self.is_automated,
            'created_at': self.created_at.isoformat(),
            'scheduled_at': self.scheduled_at.isoformat() if self.scheduled_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'outcome': self.outcome,
            'next_action': self.next_action,
            'follow_up_date': self.follow_up_date.isoformat() if self.follow_up_date else None
        }

class Property(db.Model):
    __tablename__ = 'properties'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Property details
    title = db.Column(db.String(200), nullable=False)
    development = db.Column(db.String(100))
    address = db.Column(db.String(200))
    area = db.Column(db.String(50))  # District/Area
    
    # Property specifications
    property_type = db.Column(db.String(50))
    bedrooms = db.Column(db.Integer)
    bathrooms = db.Column(db.Integer)
    saleable_area = db.Column(db.String(20))
    gross_area = db.Column(db.String(20))
    floor = db.Column(db.String(20))
    
    # Pricing
    price = db.Column(db.Integer)
    price_per_sqft = db.Column(db.Integer)
    
    # Source information
    source = db.Column(db.String(20))  # 28hse, squarefoot, centaline
    source_id = db.Column(db.String(100))
    listing_url = db.Column(db.String(500))
    
    # Images and media
    images = db.Column(db.Text)  # JSON array of image URLs
    enriched_images = db.Column(db.Text)  # JSON array of AI-processed image URLs
    
    # Agent information
    agent_name = db.Column(db.String(100))
    agent_phone = db.Column(db.String(20))
    agent_agency = db.Column(db.String(100))
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    is_featured = db.Column(db.Boolean, default=False)
    
    # Social media
    instagram_posts = db.Column(db.Text)  # JSON array of Instagram post IDs
    total_views = db.Column(db.Integer, default=0)
    total_inquiries = db.Column(db.Integer, default=0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    scraped_at = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<Property {self.id}: {self.title}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'development': self.development,
            'address': self.address,
            'area': self.area,
            'property_type': self.property_type,
            'bedrooms': self.bedrooms,
            'bathrooms': self.bathrooms,
            'saleable_area': self.saleable_area,
            'gross_area': self.gross_area,
            'floor': self.floor,
            'price': self.price,
            'price_per_sqft': self.price_per_sqft,
            'source': self.source,
            'source_id': self.source_id,
            'listing_url': self.listing_url,
            'images': json.loads(self.images) if self.images else [],
            'enriched_images': json.loads(self.enriched_images) if self.enriched_images else [],
            'agent_name': self.agent_name,
            'agent_phone': self.agent_phone,
            'agent_agency': self.agent_agency,
            'is_active': self.is_active,
            'is_featured': self.is_featured,
            'instagram_posts': json.loads(self.instagram_posts) if self.instagram_posts else [],
            'total_views': self.total_views,
            'total_inquiries': self.total_inquiries,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'scraped_at': self.scraped_at.isoformat() if self.scraped_at else None
        }

