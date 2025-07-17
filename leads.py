from flask import Blueprint, request, jsonify
from src.models.lead import db, Lead, Agent, Interaction, Property
from datetime import datetime, timedelta
import json

leads_bp = Blueprint('leads', __name__)

@leads_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "property-crm",
        "version": "1.0.0"
    })

@leads_bp.route('/leads', methods=['GET'])
def get_leads():
    """Get all leads with filtering and pagination"""
    try:
        # Query parameters
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 100)
        status = request.args.get('status')
        priority = request.args.get('priority')
        agent_id = request.args.get('agent_id', type=int)
        source = request.args.get('source')
        
        # Build query
        query = Lead.query
        
        if status:
            query = query.filter(Lead.status == status)
        if priority:
            query = query.filter(Lead.priority == priority)
        if agent_id:
            query = query.filter(Lead.assigned_agent_id == agent_id)
        if source:
            query = query.filter(Lead.source == source)
        
        # Order by priority and creation date
        query = query.order_by(
            Lead.priority.desc(),
            Lead.created_at.desc()
        )
        
        # Paginate
        leads = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        return jsonify({
            'success': True,
            'leads': [lead.to_dict() for lead in leads.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': leads.total,
                'pages': leads.pages,
                'has_next': leads.has_next,
                'has_prev': leads.has_prev
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@leads_bp.route('/leads', methods=['POST'])
def create_lead():
    """Create a new lead"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Create new lead
        lead = Lead()
        
        # Contact information
        lead.name = data.get('name')
        lead.phone = data.get('phone')
        lead.email = data.get('email')
        lead.instagram_handle = data.get('instagram_handle')
        lead.whatsapp_number = data.get('whatsapp_number')
        
        # Source information
        lead.source = data.get('source', 'unknown')
        lead.source_post_id = data.get('source_post_id')
        lead.source_property_id = data.get('source_property_id')
        lead.original_message = data.get('original_message')
        
        # Lead qualification
        lead.status = data.get('status', 'new')
        lead.priority = data.get('priority', 'medium')
        
        # Property interests
        if data.get('interested_properties'):
            lead.interested_properties = json.dumps(data['interested_properties'])
        lead.budget_min = data.get('budget_min')
        lead.budget_max = data.get('budget_max')
        if data.get('preferred_areas'):
            lead.preferred_areas = json.dumps(data['preferred_areas'])
        lead.property_type = data.get('property_type')
        lead.bedrooms = data.get('bedrooms')
        if data.get('move_in_date'):
            lead.move_in_date = datetime.fromisoformat(data['move_in_date']).date()
        
        # Tags and notes
        if data.get('tags'):
            lead.tags = json.dumps(data['tags'])
        lead.notes = data.get('notes')
        
        # Auto-assign agent if not specified
        if data.get('assigned_agent_id'):
            lead.assigned_agent_id = data['assigned_agent_id']
        else:
            # Find best available agent
            agent = find_best_agent(lead)
            if agent:
                lead.assigned_agent_id = agent.id
        
        # Calculate initial score
        db.session.add(lead)
        db.session.flush()  # Get the ID
        lead.update_score()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'lead': lead.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@leads_bp.route('/leads/<int:lead_id>', methods=['GET'])
def get_lead(lead_id):
    """Get a specific lead"""
    try:
        lead = Lead.query.get_or_404(lead_id)
        return jsonify({
            'success': True,
            'lead': lead.to_dict()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@leads_bp.route('/leads/<int:lead_id>', methods=['PUT'])
def update_lead(lead_id):
    """Update a lead"""
    try:
        lead = Lead.query.get_or_404(lead_id)
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Update fields
        for field in ['name', 'phone', 'email', 'instagram_handle', 'whatsapp_number',
                     'status', 'priority', 'budget_min', 'budget_max', 'property_type',
                     'bedrooms', 'notes', 'assigned_agent_id']:
            if field in data:
                setattr(lead, field, data[field])
        
        # Handle JSON fields
        if 'interested_properties' in data:
            lead.interested_properties = json.dumps(data['interested_properties'])
        if 'preferred_areas' in data:
            lead.preferred_areas = json.dumps(data['preferred_areas'])
        if 'tags' in data:
            lead.tags = json.dumps(data['tags'])
        
        # Handle date fields
        if 'move_in_date' in data and data['move_in_date']:
            lead.move_in_date = datetime.fromisoformat(data['move_in_date']).date()
        if 'next_follow_up_at' in data and data['next_follow_up_at']:
            lead.next_follow_up_at = datetime.fromisoformat(data['next_follow_up_at'])
        
        # Update score
        lead.update_score()
        lead.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'lead': lead.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@leads_bp.route('/leads/<int:lead_id>/interactions', methods=['GET'])
def get_lead_interactions(lead_id):
    """Get all interactions for a lead"""
    try:
        lead = Lead.query.get_or_404(lead_id)
        interactions = Interaction.query.filter_by(lead_id=lead_id).order_by(
            Interaction.created_at.desc()
        ).all()
        
        return jsonify({
            'success': True,
            'interactions': [interaction.to_dict() for interaction in interactions]
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@leads_bp.route('/leads/<int:lead_id>/interactions', methods=['POST'])
def create_interaction():
    """Create a new interaction for a lead"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        interaction = Interaction()
        interaction.lead_id = lead_id
        interaction.type = data.get('type', 'message')
        interaction.channel = data.get('channel')
        interaction.direction = data.get('direction', 'outbound')
        interaction.subject = data.get('subject')
        interaction.message = data.get('message')
        interaction.agent_id = data.get('agent_id')
        interaction.is_automated = data.get('is_automated', False)
        interaction.outcome = data.get('outcome')
        interaction.next_action = data.get('next_action')
        
        if data.get('attachments'):
            interaction.attachments = json.dumps(data['attachments'])
        if data.get('scheduled_at'):
            interaction.scheduled_at = datetime.fromisoformat(data['scheduled_at'])
        if data.get('follow_up_date'):
            interaction.follow_up_date = datetime.fromisoformat(data['follow_up_date'])
        
        # Update lead's last contact time
        lead = Lead.query.get(lead_id)
        lead.last_contact_at = datetime.utcnow()
        
        db.session.add(interaction)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'interaction': interaction.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@leads_bp.route('/leads/instagram-inquiry', methods=['POST'])
def handle_instagram_inquiry():
    """Handle Instagram inquiry and create/update lead"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        instagram_handle = data.get('instagram_handle')
        message = data.get('message')
        post_id = data.get('post_id')
        property_id = data.get('property_id')
        
        if not instagram_handle or not message:
            return jsonify({'error': 'Instagram handle and message are required'}), 400
        
        # Check if lead already exists
        existing_lead = Lead.query.filter_by(instagram_handle=instagram_handle).first()
        
        if existing_lead:
            # Update existing lead
            lead = existing_lead
            lead.last_contact_at = datetime.utcnow()
            
            # Add to interested properties if new
            if property_id:
                interested = json.loads(lead.interested_properties) if lead.interested_properties else []
                if property_id not in interested:
                    interested.append(property_id)
                    lead.interested_properties = json.dumps(interested)
        else:
            # Create new lead
            lead = Lead()
            lead.instagram_handle = instagram_handle
            lead.source = 'instagram'
            lead.source_post_id = post_id
            lead.source_property_id = property_id
            lead.original_message = message
            lead.status = 'new'
            
            if property_id:
                lead.interested_properties = json.dumps([property_id])
            
            # Auto-assign agent
            agent = find_best_agent(lead)
            if agent:
                lead.assigned_agent_id = agent.id
            
            db.session.add(lead)
            db.session.flush()
        
        # Create interaction record
        interaction = Interaction()
        interaction.lead_id = lead.id
        interaction.type = 'message'
        interaction.channel = 'instagram'
        interaction.direction = 'inbound'
        interaction.message = message
        interaction.is_automated = False
        
        db.session.add(interaction)
        
        # Update lead score
        lead.update_score()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'lead': lead.to_dict(),
            'is_new_lead': existing_lead is None
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@leads_bp.route('/leads/whatsapp-inquiry', methods=['POST'])
def handle_whatsapp_inquiry():
    """Handle WhatsApp inquiry and create/update lead"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        whatsapp_number = data.get('whatsapp_number')
        message = data.get('message')
        name = data.get('name')
        
        if not whatsapp_number or not message:
            return jsonify({'error': 'WhatsApp number and message are required'}), 400
        
        # Check if lead already exists
        existing_lead = Lead.query.filter_by(whatsapp_number=whatsapp_number).first()
        
        if existing_lead:
            lead = existing_lead
            lead.last_contact_at = datetime.utcnow()
            if name and not lead.name:
                lead.name = name
        else:
            # Create new lead
            lead = Lead()
            lead.whatsapp_number = whatsapp_number
            lead.name = name
            lead.source = 'whatsapp'
            lead.original_message = message
            lead.status = 'new'
            
            # Auto-assign agent
            agent = find_best_agent(lead)
            if agent:
                lead.assigned_agent_id = agent.id
            
            db.session.add(lead)
            db.session.flush()
        
        # Create interaction record
        interaction = Interaction()
        interaction.lead_id = lead.id
        interaction.type = 'message'
        interaction.channel = 'whatsapp'
        interaction.direction = 'inbound'
        interaction.message = message
        interaction.is_automated = False
        
        db.session.add(interaction)
        
        # Update lead score
        lead.update_score()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'lead': lead.to_dict(),
            'is_new_lead': existing_lead is None
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

def find_best_agent(lead):
    """Find the best available agent for a lead"""
    try:
        # Get all active agents who can take more leads
        available_agents = Agent.query.filter_by(is_active=True).all()
        available_agents = [agent for agent in available_agents if agent.can_take_lead()]
        
        if not available_agents:
            return None
        
        # Score agents based on specialization and workload
        best_agent = None
        best_score = -1
        
        for agent in available_agents:
            score = 0
            
            # Specialization match
            if lead.preferred_areas and agent.specialization_areas:
                agent_areas = json.loads(agent.specialization_areas)
                lead_areas = json.loads(lead.preferred_areas)
                if any(area in agent_areas for area in lead_areas):
                    score += 20
            
            if lead.property_type and agent.specialization_types:
                agent_types = json.loads(agent.specialization_types)
                if lead.property_type in agent_types:
                    score += 15
            
            # Workload (prefer agents with fewer current leads)
            current_leads = len(agent.leads)
            workload_score = max(0, 10 - current_leads)
            score += workload_score
            
            # Performance (conversion rate)
            if agent.total_leads > 0:
                conversion_rate = agent.converted_leads / agent.total_leads
                score += conversion_rate * 10
            
            if score > best_score:
                best_score = score
                best_agent = agent
        
        return best_agent
        
    except Exception as e:
        print(f"Error finding best agent: {e}")
        return None

