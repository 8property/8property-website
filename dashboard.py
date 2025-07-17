from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
import requests
import json
from datetime import datetime, timedelta

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')

# Mock service URLs - these would be your actual deployed service URLs
SERVICE_URLS = {
    'crm': 'http://localhost:5001',
    'analytics': 'http://localhost:5002',
    'scrapers': {
        '28hse': 'http://localhost:5003',
        'squarefoot': 'http://localhost:5004',
        'centaline': 'http://localhost:5005'
    },
    'ai_enrichment': 'http://localhost:5006'
}

@dashboard_bp.route('/metrics', methods=['GET'])
@cross_origin()
def get_dashboard_metrics():
    """Get key dashboard metrics"""
    try:
        # Mock data - in production, this would aggregate from various services
        metrics = {
            'total_leads': 1247,
            'total_leads_change': 12.5,
            'active_properties': 342,
            'active_properties_change': 8.2,
            'conversion_rate': 24.8,
            'conversion_rate_change': -2.1,
            'system_uptime': 99.9,
            'system_uptime_change': 0.1,
            'content_engagement': 8.7,
            'content_engagement_change': 2.3
        }
        
        return jsonify({
            'success': True,
            'data': metrics
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@dashboard_bp.route('/activity', methods=['GET'])
@cross_origin()
def get_recent_activity():
    """Get recent system activity"""
    try:
        # Mock recent activities
        activities = [
            {
                'id': 1,
                'type': 'scrape',
                'message': 'New properties scraped from 28Hse',
                'time': '2024-01-15T10:30:00Z',
                'count': 15
            },
            {
                'id': 2,
                'type': 'lead',
                'message': 'High-quality lead generated',
                'time': '2024-01-15T10:25:00Z',
                'score': 95
            },
            {
                'id': 3,
                'type': 'post',
                'message': 'Instagram post published',
                'time': '2024-01-15T10:18:00Z',
                'engagement': '2.3k views'
            },
            {
                'id': 4,
                'type': 'conversion',
                'message': 'Lead converted to viewing',
                'time': '2024-01-15T10:12:00Z',
                'agent': 'Sarah Chen'
            },
            {
                'id': 5,
                'type': 'ai',
                'message': 'Content enrichment completed',
                'time': '2024-01-15T10:05:00Z',
                'count': 8
            }
        ]
        
        return jsonify({
            'success': True,
            'data': activities
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@dashboard_bp.route('/charts/leads', methods=['GET'])
@cross_origin()
def get_lead_trend_data():
    """Get lead generation trend data"""
    try:
        # Mock chart data
        data = [
            {'name': 'Mon', 'leads': 12, 'conversions': 3},
            {'name': 'Tue', 'leads': 19, 'conversions': 5},
            {'name': 'Wed', 'leads': 15, 'conversions': 4},
            {'name': 'Thu', 'leads': 22, 'conversions': 7},
            {'name': 'Fri', 'leads': 28, 'conversions': 8},
            {'name': 'Sat', 'leads': 35, 'conversions': 12},
            {'name': 'Sun', 'leads': 31, 'conversions': 10}
        ]
        
        return jsonify({
            'success': True,
            'data': data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@dashboard_bp.route('/charts/content', methods=['GET'])
@cross_origin()
def get_content_performance_data():
    """Get content performance data"""
    try:
        # Mock content performance data
        data = [
            {'name': 'Property Photos', 'engagement': 85},
            {'name': 'Collages', 'engagement': 92},
            {'name': 'Market News', 'engagement': 67},
            {'name': 'Agent Highlights', 'engagement': 74}
        ]
        
        return jsonify({
            'success': True,
            'data': data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@dashboard_bp.route('/charts/sources', methods=['GET'])
@cross_origin()
def get_source_distribution():
    """Get data source distribution"""
    try:
        # Mock source distribution data
        data = [
            {'name': '28Hse', 'value': 45, 'color': '#3B82F6'},
            {'name': 'Squarefoot', 'value': 35, 'color': '#10B981'},
            {'name': 'Centaline', 'value': 20, 'color': '#F59E0B'}
        ]
        
        return jsonify({
            'success': True,
            'data': data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@dashboard_bp.route('/system-status', methods=['GET'])
@cross_origin()
def get_system_status():
    """Get system status for all services"""
    try:
        # Mock system status - in production, this would ping actual services
        status = {
            'scrapers': 'online',
            'ai_enrichment': 'online',
            'crm': 'online',
            'analytics': 'online',
            'make_automation': 'online'
        }
        
        return jsonify({
            'success': True,
            'data': status
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@dashboard_bp.route('/trigger-scraper', methods=['POST'])
@cross_origin()
def trigger_scraper():
    """Manually trigger a scraper"""
    try:
        data = request.get_json()
        scraper_type = data.get('type', '28hse')
        
        # Mock scraper trigger - in production, this would call actual scraper services
        result = {
            'message': f'{scraper_type} scraper triggered successfully',
            'job_id': f'job_{datetime.now().strftime("%Y%m%d_%H%M%S")}',
            'estimated_completion': (datetime.now() + timedelta(minutes=5)).isoformat()
        }
        
        return jsonify({
            'success': True,
            'data': result
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

