from flask import Blueprint, request, jsonify
from src.models.lead import db, Lead, Agent, Interaction, Property
from datetime import datetime, timedelta
from sqlalchemy import func, and_, or_
import json

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/analytics/dashboard', methods=['GET'])
def get_dashboard_metrics():
    """Get key metrics for dashboard"""
    try:
        # Get date range
        days = request.args.get('days', 30, type=int)
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Total leads
        total_leads = Lead.query.count()
        new_leads = Lead.query.filter(Lead.created_at >= start_date).count()
        
        # Leads by status
        leads_by_status = db.session.query(
            Lead.status, 
            func.count(Lead.id)
        ).group_by(Lead.status).all()
        
        status_counts = {status: count for status, count in leads_by_status}
        
        # Leads by source
        leads_by_source = db.session.query(
            Lead.source, 
            func.count(Lead.id)
        ).group_by(Lead.source).all()
        
        source_counts = {source: count for source, count in leads_by_source}
        
        # Conversion metrics
        converted_leads = Lead.query.filter(
            Lead.status == 'converted',
            Lead.updated_at >= start_date
        ).count()
        
        conversion_rate = (converted_leads / new_leads * 100) if new_leads > 0 else 0
        
        # Agent performance
        agent_performance = db.session.query(
            Agent.name,
            func.count(Lead.id).label('total_leads'),
            func.sum(func.case([(Lead.status == 'converted', 1)], else_=0)).label('converted')
        ).outerjoin(Lead).group_by(Agent.id, Agent.name).all()
        
        agents_data = []
        for name, total, converted in agent_performance:
            agents_data.append({
                'name': name,
                'total_leads': total or 0,
                'converted_leads': converted or 0,
                'conversion_rate': (converted / total * 100) if total and total > 0 else 0
            })
        
        # Recent activity
        recent_interactions = Interaction.query.filter(
            Interaction.created_at >= start_date
        ).count()
        
        # Response time
        response_times = db.session.query(
            func.avg(
                func.julianday(Interaction.created_at) - func.julianday(Lead.created_at)
            ).label('avg_response_days')
        ).join(Lead).filter(
            Interaction.direction == 'outbound',
            Interaction.created_at >= start_date
        ).first()
        
        avg_response_hours = (response_times[0] * 24) if response_times[0] else 0
        
        return jsonify({
            'success': True,
            'metrics': {
                'period_days': days,
                'total_leads': total_leads,
                'new_leads': new_leads,
                'converted_leads': converted_leads,
                'conversion_rate': round(conversion_rate, 2),
                'recent_interactions': recent_interactions,
                'avg_response_hours': round(avg_response_hours, 2),
                'leads_by_status': status_counts,
                'leads_by_source': source_counts,
                'agent_performance': agents_data
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/analytics/leads-trend', methods=['GET'])
def get_leads_trend():
    """Get leads trend over time"""
    try:
        days = request.args.get('days', 30, type=int)
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Daily lead creation
        daily_leads = db.session.query(
            func.date(Lead.created_at).label('date'),
            func.count(Lead.id).label('count')
        ).filter(
            Lead.created_at >= start_date
        ).group_by(func.date(Lead.created_at)).order_by('date').all()
        
        # Daily conversions
        daily_conversions = db.session.query(
            func.date(Lead.updated_at).label('date'),
            func.count(Lead.id).label('count')
        ).filter(
            Lead.status == 'converted',
            Lead.updated_at >= start_date
        ).group_by(func.date(Lead.updated_at)).order_by('date').all()
        
        # Format data
        leads_data = [{'date': str(date), 'leads': count} for date, count in daily_leads]
        conversions_data = [{'date': str(date), 'conversions': count} for date, count in daily_conversions]
        
        return jsonify({
            'success': True,
            'trend_data': {
                'leads': leads_data,
                'conversions': conversions_data
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/analytics/source-performance', methods=['GET'])
def get_source_performance():
    """Get performance metrics by lead source"""
    try:
        days = request.args.get('days', 30, type=int)
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Source performance
        source_performance = db.session.query(
            Lead.source,
            func.count(Lead.id).label('total_leads'),
            func.sum(func.case([(Lead.status == 'converted', 1)], else_=0)).label('converted'),
            func.avg(Lead.score).label('avg_score'),
            func.sum(func.case([(Lead.priority == 'high', 1)], else_=0)).label('high_priority')
        ).filter(
            Lead.created_at >= start_date
        ).group_by(Lead.source).all()
        
        source_data = []
        for source, total, converted, avg_score, high_priority in source_performance:
            source_data.append({
                'source': source,
                'total_leads': total,
                'converted_leads': converted or 0,
                'conversion_rate': (converted / total * 100) if total > 0 else 0,
                'avg_score': round(avg_score or 0, 2),
                'high_priority_leads': high_priority or 0
            })
        
        return jsonify({
            'success': True,
            'source_performance': source_data
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/analytics/agent-comparison', methods=['GET'])
def get_agent_comparison():
    """Get detailed agent performance comparison"""
    try:
        days = request.args.get('days', 30, type=int)
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Agent metrics
        agent_metrics = db.session.query(
            Agent.id,
            Agent.name,
            func.count(Lead.id).label('total_leads'),
            func.sum(func.case([(Lead.status == 'converted', 1)], else_=0)).label('converted'),
            func.avg(Lead.score).label('avg_lead_score'),
            func.count(Interaction.id).label('total_interactions')
        ).outerjoin(Lead).outerjoin(Interaction, and_(
            Interaction.lead_id == Lead.id,
            Interaction.agent_id == Agent.id
        )).filter(
            or_(Lead.created_at >= start_date, Lead.created_at.is_(None))
        ).group_by(Agent.id, Agent.name).all()
        
        agent_data = []
        for agent_id, name, total, converted, avg_score, interactions in agent_metrics:
            # Calculate response time for this agent
            response_times = db.session.query(
                func.avg(
                    func.julianday(Interaction.created_at) - func.julianday(Lead.created_at)
                ).label('avg_response_days')
            ).join(Lead).filter(
                Interaction.agent_id == agent_id,
                Interaction.direction == 'outbound',
                Interaction.created_at >= start_date
            ).first()
            
            avg_response_hours = (response_times[0] * 24) if response_times[0] else 0
            
            agent_data.append({
                'agent_id': agent_id,
                'name': name,
                'total_leads': total or 0,
                'converted_leads': converted or 0,
                'conversion_rate': (converted / total * 100) if total and total > 0 else 0,
                'avg_lead_score': round(avg_score or 0, 2),
                'total_interactions': interactions or 0,
                'avg_response_hours': round(avg_response_hours, 2)
            })
        
        return jsonify({
            'success': True,
            'agent_comparison': agent_data
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/analytics/property-performance', methods=['GET'])
def get_property_performance():
    """Get property listing performance metrics"""
    try:
        days = request.args.get('days', 30, type=int)
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Property inquiry metrics
        property_inquiries = db.session.query(
            Lead.source_property_id,
            func.count(Lead.id).label('inquiries'),
            func.sum(func.case([(Lead.status == 'converted', 1)], else_=0)).label('conversions'),
            func.avg(Lead.score).label('avg_lead_quality')
        ).filter(
            Lead.source_property_id.isnot(None),
            Lead.created_at >= start_date
        ).group_by(Lead.source_property_id).order_by(func.count(Lead.id).desc()).limit(20).all()
        
        property_data = []
        for prop_id, inquiries, conversions, avg_quality in property_inquiries:
            # Get property details if available
            property_info = Property.query.filter_by(source_id=prop_id).first()
            
            property_data.append({
                'property_id': prop_id,
                'title': property_info.title if property_info else f'Property {prop_id}',
                'price': property_info.price if property_info else None,
                'area': property_info.area if property_info else None,
                'inquiries': inquiries,
                'conversions': conversions or 0,
                'conversion_rate': (conversions / inquiries * 100) if inquiries > 0 else 0,
                'avg_lead_quality': round(avg_quality or 0, 2)
            })
        
        return jsonify({
            'success': True,
            'property_performance': property_data
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/analytics/funnel', methods=['GET'])
def get_conversion_funnel():
    """Get conversion funnel metrics"""
    try:
        days = request.args.get('days', 30, type=int)
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Funnel stages
        funnel_data = {}
        
        # Stage 1: Total leads
        total_leads = Lead.query.filter(Lead.created_at >= start_date).count()
        funnel_data['total_leads'] = total_leads
        
        # Stage 2: Contacted leads
        contacted_leads = Lead.query.filter(
            Lead.created_at >= start_date,
            Lead.status.in_(['contacted', 'qualified', 'viewing_scheduled', 'applied', 'converted'])
        ).count()
        funnel_data['contacted_leads'] = contacted_leads
        
        # Stage 3: Qualified leads
        qualified_leads = Lead.query.filter(
            Lead.created_at >= start_date,
            Lead.status.in_(['qualified', 'viewing_scheduled', 'applied', 'converted'])
        ).count()
        funnel_data['qualified_leads'] = qualified_leads
        
        # Stage 4: Viewing scheduled
        viewing_leads = Lead.query.filter(
            Lead.created_at >= start_date,
            Lead.status.in_(['viewing_scheduled', 'applied', 'converted'])
        ).count()
        funnel_data['viewing_leads'] = viewing_leads
        
        # Stage 5: Applied
        applied_leads = Lead.query.filter(
            Lead.created_at >= start_date,
            Lead.status.in_(['applied', 'converted'])
        ).count()
        funnel_data['applied_leads'] = applied_leads
        
        # Stage 6: Converted
        converted_leads = Lead.query.filter(
            Lead.created_at >= start_date,
            Lead.status == 'converted'
        ).count()
        funnel_data['converted_leads'] = converted_leads
        
        # Calculate conversion rates
        funnel_rates = {}
        if total_leads > 0:
            funnel_rates['contact_rate'] = contacted_leads / total_leads * 100
            funnel_rates['qualification_rate'] = qualified_leads / total_leads * 100
            funnel_rates['viewing_rate'] = viewing_leads / total_leads * 100
            funnel_rates['application_rate'] = applied_leads / total_leads * 100
            funnel_rates['conversion_rate'] = converted_leads / total_leads * 100
        
        return jsonify({
            'success': True,
            'funnel': {
                'counts': funnel_data,
                'rates': funnel_rates
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/analytics/lead-scoring', methods=['GET'])
def get_lead_scoring_analysis():
    """Get lead scoring distribution and effectiveness"""
    try:
        # Score distribution
        score_ranges = [
            (0, 20, 'Very Low'),
            (21, 40, 'Low'),
            (41, 60, 'Medium'),
            (61, 80, 'High'),
            (81, 100, 'Very High')
        ]
        
        score_distribution = []
        for min_score, max_score, label in score_ranges:
            count = Lead.query.filter(
                Lead.score >= min_score,
                Lead.score <= max_score
            ).count()
            
            converted = Lead.query.filter(
                Lead.score >= min_score,
                Lead.score <= max_score,
                Lead.status == 'converted'
            ).count()
            
            score_distribution.append({
                'range': f'{min_score}-{max_score}',
                'label': label,
                'count': count,
                'converted': converted,
                'conversion_rate': (converted / count * 100) if count > 0 else 0
            })
        
        # Score vs conversion correlation
        avg_score_by_status = db.session.query(
            Lead.status,
            func.avg(Lead.score).label('avg_score'),
            func.count(Lead.id).label('count')
        ).group_by(Lead.status).all()
        
        status_scores = [
            {
                'status': status,
                'avg_score': round(avg_score or 0, 2),
                'count': count
            }
            for status, avg_score, count in avg_score_by_status
        ]
        
        return jsonify({
            'success': True,
            'scoring_analysis': {
                'score_distribution': score_distribution,
                'status_scores': status_scores
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/analytics/export', methods=['GET'])
def export_analytics_data():
    """Export analytics data for external analysis"""
    try:
        days = request.args.get('days', 30, type=int)
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Export lead data
        leads = Lead.query.filter(Lead.created_at >= start_date).all()
        leads_data = [lead.to_dict() for lead in leads]
        
        # Export interaction data
        interactions = Interaction.query.filter(
            Interaction.created_at >= start_date
        ).all()
        interactions_data = [interaction.to_dict() for interaction in interactions]
        
        # Export agent data
        agents = Agent.query.all()
        agents_data = [agent.to_dict() for agent in agents]
        
        return jsonify({
            'success': True,
            'export_data': {
                'period_days': days,
                'export_date': datetime.utcnow().isoformat(),
                'leads': leads_data,
                'interactions': interactions_data,
                'agents': agents_data
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

