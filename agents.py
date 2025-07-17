from flask import Blueprint, request, jsonify
from src.models.lead import db, Agent, Lead, Interaction
from datetime import datetime, timedelta
import json

agents_bp = Blueprint('agents', __name__)

@agents_bp.route('/agents', methods=['GET'])
def get_agents():
    """Get all agents"""
    try:
        agents = Agent.query.all()
        return jsonify({
            'success': True,
            'agents': [agent.to_dict() for agent in agents]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@agents_bp.route('/agents', methods=['POST'])
def create_agent():
    """Create a new agent"""
    try:
        data = request.get_json()
        
        if not data or not data.get('name') or not data.get('email'):
            return jsonify({'error': 'Name and email are required'}), 400
        
        # Check if email already exists
        existing_agent = Agent.query.filter_by(email=data['email']).first()
        if existing_agent:
            return jsonify({'error': 'Agent with this email already exists'}), 400
        
        agent = Agent()
        agent.name = data['name']
        agent.email = data['email']
        agent.phone = data.get('phone')
        agent.whatsapp_number = data.get('whatsapp_number')
        agent.max_leads = data.get('max_leads', 50)
        agent.is_active = data.get('is_active', True)
        
        # Handle JSON fields
        if data.get('specialization_areas'):
            agent.specialization_areas = json.dumps(data['specialization_areas'])
        if data.get('specialization_types'):
            agent.specialization_types = json.dumps(data['specialization_types'])
        if data.get('languages'):
            agent.languages = json.dumps(data['languages'])
        
        db.session.add(agent)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'agent': agent.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@agents_bp.route('/agents/<int:agent_id>', methods=['GET'])
def get_agent(agent_id):
    """Get a specific agent"""
    try:
        agent = Agent.query.get_or_404(agent_id)
        return jsonify({
            'success': True,
            'agent': agent.to_dict()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@agents_bp.route('/agents/<int:agent_id>', methods=['PUT'])
def update_agent(agent_id):
    """Update an agent"""
    try:
        agent = Agent.query.get_or_404(agent_id)
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Update basic fields
        for field in ['name', 'email', 'phone', 'whatsapp_number', 'max_leads', 'is_active']:
            if field in data:
                setattr(agent, field, data[field])
        
        # Handle JSON fields
        if 'specialization_areas' in data:
            agent.specialization_areas = json.dumps(data['specialization_areas'])
        if 'specialization_types' in data:
            agent.specialization_types = json.dumps(data['specialization_types'])
        if 'languages' in data:
            agent.languages = json.dumps(data['languages'])
        
        agent.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'agent': agent.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@agents_bp.route('/agents/<int:agent_id>/leads', methods=['GET'])
def get_agent_leads(agent_id):
    """Get all leads assigned to an agent"""
    try:
        agent = Agent.query.get_or_404(agent_id)
        
        # Query parameters
        status = request.args.get('status')
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 100)
        
        # Build query
        query = Lead.query.filter_by(assigned_agent_id=agent_id)
        
        if status:
            query = query.filter(Lead.status == status)
        
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
            'agent': agent.to_dict(),
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

@agents_bp.route('/agents/<int:agent_id>/performance', methods=['GET'])
def get_agent_performance(agent_id):
    """Get agent performance metrics"""
    try:
        agent = Agent.query.get_or_404(agent_id)
        
        # Get date range
        days = request.args.get('days', 30, type=int)
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Current leads by status
        current_leads = db.session.query(
            Lead.status, 
            db.func.count(Lead.id)
        ).filter_by(assigned_agent_id=agent_id).group_by(Lead.status).all()
        
        leads_by_status = {status: count for status, count in current_leads}
        
        # Leads created in period
        new_leads = Lead.query.filter(
            Lead.assigned_agent_id == agent_id,
            Lead.created_at >= start_date
        ).count()
        
        # Interactions in period
        interactions = Interaction.query.filter(
            Interaction.agent_id == agent_id,
            Interaction.created_at >= start_date
        ).count()
        
        # Response time calculation
        response_times = db.session.query(
            Interaction.created_at,
            Lead.created_at
        ).join(Lead).filter(
            Interaction.agent_id == agent_id,
            Interaction.direction == 'outbound',
            Interaction.created_at >= start_date
        ).all()
        
        avg_response_time = 0
        if response_times:
            total_response_time = sum([
                (interaction_time - lead_time).total_seconds() / 60
                for interaction_time, lead_time in response_times
                if interaction_time > lead_time
            ])
            avg_response_time = total_response_time / len(response_times)
        
        # Conversion rate
        converted_leads = Lead.query.filter(
            Lead.assigned_agent_id == agent_id,
            Lead.status == 'converted',
            Lead.updated_at >= start_date
        ).count()
        
        conversion_rate = (converted_leads / new_leads * 100) if new_leads > 0 else 0
        
        return jsonify({
            'success': True,
            'agent': agent.to_dict(),
            'performance': {
                'period_days': days,
                'leads_by_status': leads_by_status,
                'new_leads': new_leads,
                'interactions': interactions,
                'avg_response_time_minutes': round(avg_response_time, 2),
                'converted_leads': converted_leads,
                'conversion_rate': round(conversion_rate, 2)
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@agents_bp.route('/agents/<int:agent_id>/workload', methods=['GET'])
def get_agent_workload(agent_id):
    """Get agent current workload"""
    try:
        agent = Agent.query.get_or_404(agent_id)
        
        # Current active leads
        active_leads = Lead.query.filter(
            Lead.assigned_agent_id == agent_id,
            Lead.status.in_(['new', 'contacted', 'qualified', 'viewing_scheduled'])
        ).count()
        
        # Overdue follow-ups
        overdue_followups = Lead.query.filter(
            Lead.assigned_agent_id == agent_id,
            Lead.next_follow_up_at < datetime.utcnow(),
            Lead.status.in_(['new', 'contacted', 'qualified'])
        ).count()
        
        # Today's scheduled interactions
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1)
        
        scheduled_today = Interaction.query.filter(
            Interaction.agent_id == agent_id,
            Interaction.scheduled_at >= today_start,
            Interaction.scheduled_at < today_end,
            Interaction.completed_at.is_(None)
        ).count()
        
        # High priority leads
        high_priority_leads = Lead.query.filter(
            Lead.assigned_agent_id == agent_id,
            Lead.priority == 'high',
            Lead.status.in_(['new', 'contacted', 'qualified'])
        ).count()
        
        # Workload capacity
        capacity_percentage = (active_leads / agent.max_leads * 100) if agent.max_leads > 0 else 0
        
        return jsonify({
            'success': True,
            'agent': agent.to_dict(),
            'workload': {
                'active_leads': active_leads,
                'max_leads': agent.max_leads,
                'capacity_percentage': round(capacity_percentage, 2),
                'overdue_followups': overdue_followups,
                'scheduled_today': scheduled_today,
                'high_priority_leads': high_priority_leads,
                'can_take_more_leads': agent.can_take_lead()
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@agents_bp.route('/agents/assign-lead', methods=['POST'])
def assign_lead():
    """Manually assign a lead to an agent"""
    try:
        data = request.get_json()
        
        if not data or not data.get('lead_id') or not data.get('agent_id'):
            return jsonify({'error': 'Lead ID and Agent ID are required'}), 400
        
        lead = Lead.query.get_or_404(data['lead_id'])
        agent = Agent.query.get_or_404(data['agent_id'])
        
        if not agent.can_take_lead():
            return jsonify({'error': 'Agent has reached maximum lead capacity'}), 400
        
        # Update lead assignment
        old_agent_id = lead.assigned_agent_id
        lead.assigned_agent_id = agent.id
        lead.updated_at = datetime.utcnow()
        
        # Create interaction record for assignment
        interaction = Interaction()
        interaction.lead_id = lead.id
        interaction.type = 'assignment'
        interaction.channel = 'system'
        interaction.direction = 'outbound'
        interaction.message = f"Lead assigned to {agent.name}"
        interaction.agent_id = agent.id
        interaction.is_automated = True
        
        db.session.add(interaction)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'lead': lead.to_dict(),
            'message': f'Lead assigned to {agent.name}'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@agents_bp.route('/agents/auto-assign', methods=['POST'])
def auto_assign_leads():
    """Auto-assign unassigned leads to available agents"""
    try:
        # Get unassigned leads
        unassigned_leads = Lead.query.filter(
            Lead.assigned_agent_id.is_(None),
            Lead.status.in_(['new', 'contacted'])
        ).order_by(Lead.priority.desc(), Lead.created_at.asc()).all()
        
        assigned_count = 0
        
        for lead in unassigned_leads:
            # Find best available agent
            from src.routes.leads import find_best_agent
            agent = find_best_agent(lead)
            
            if agent:
                lead.assigned_agent_id = agent.id
                lead.updated_at = datetime.utcnow()
                
                # Create interaction record
                interaction = Interaction()
                interaction.lead_id = lead.id
                interaction.type = 'assignment'
                interaction.channel = 'system'
                interaction.direction = 'outbound'
                interaction.message = f"Lead auto-assigned to {agent.name}"
                interaction.agent_id = agent.id
                interaction.is_automated = True
                
                db.session.add(interaction)
                assigned_count += 1
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'assigned_count': assigned_count,
            'message': f'Successfully assigned {assigned_count} leads'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

