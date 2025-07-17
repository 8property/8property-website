from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
import requests
import json
from datetime import datetime

properties_bp = Blueprint('properties', __name__, url_prefix='/api/properties')

@properties_bp.route('/', methods=['GET'])
@cross_origin()
def get_properties():
    """Get all properties with filtering and pagination"""
    try:
        # Get query parameters
        search = request.args.get('search', '')
        status = request.args.get('status', 'all')
        source = request.args.get('source', 'all')
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 20))
        
        # Mock properties data
        properties = [
            {
                'id': 1,
                'title': 'Modern 2BR Apartment in Central',
                'location': 'Central, Hong Kong Island',
                'price': 45000,
                'currency': 'HKD',
                'period': 'month',
                'bedrooms': 2,
                'bathrooms': 2,
                'area': 800,
                'image': '/api/placeholder/400/300',
                'source': '28hse',
                'status': 'published',
                'engagement': {
                    'views': 1250,
                    'likes': 89,
                    'comments': 12,
                    'shares': 5
                },
                'ai_generated': {
                    'caption': 'Stunning modern apartment in the heart of Central! ✨ This beautifully designed 2-bedroom unit offers breathtaking city views and premium finishes. Perfect for professionals seeking luxury living in Hong Kong\'s financial district. 🏙️ #CentralLiving #ModernApartment #HongKongRental',
                    'hashtags': ['#CentralLiving', '#ModernApartment', '#HongKongRental', '#LuxuryLiving', '#CityViews'],
                    'style': 'engaging'
                },
                'posted_at': '2024-01-15T10:30:00Z',
                'scraped_at': '2024-01-15T09:15:00Z'
            },
            {
                'id': 2,
                'title': 'Cozy Studio in Causeway Bay',
                'location': 'Causeway Bay, Hong Kong Island',
                'price': 28000,
                'currency': 'HKD',
                'period': 'month',
                'bedrooms': 0,
                'bathrooms': 1,
                'area': 450,
                'image': '/api/placeholder/400/300',
                'source': 'squarefoot',
                'status': 'pending',
                'engagement': {
                    'views': 0,
                    'likes': 0,
                    'comments': 0,
                    'shares': 0
                },
                'ai_generated': {
                    'caption': 'Charming studio apartment in vibrant Causeway Bay! 🌟 Perfectly located near shopping and dining, this cozy space is ideal for young professionals. Efficient layout maximizes every square foot. 🏠 #CausewayBay #StudioApartment #ConvenientLiving',
                    'hashtags': ['#CausewayBay', '#StudioApartment', '#ConvenientLiving', '#YoungProfessionals'],
                    'style': 'professional'
                },
                'posted_at': None,
                'scraped_at': '2024-01-15T11:45:00Z'
            },
            {
                'id': 3,
                'title': 'Luxury 3BR Penthouse in Mid-Levels',
                'location': 'Mid-Levels, Hong Kong Island',
                'price': 85000,
                'currency': 'HKD',
                'period': 'month',
                'bedrooms': 3,
                'bathrooms': 3,
                'area': 1200,
                'image': '/api/placeholder/400/300',
                'source': 'centaline',
                'status': 'published',
                'engagement': {
                    'views': 2100,
                    'likes': 156,
                    'comments': 28,
                    'shares': 15
                },
                'ai_generated': {
                    'caption': 'Exclusive penthouse living in prestigious Mid-Levels! 🏙️ This magnificent 3-bedroom residence features panoramic harbor views, premium appliances, and elegant finishes throughout. Experience the pinnacle of Hong Kong luxury. ✨ #MidLevels #PenthouseLiving #LuxuryRental',
                    'hashtags': ['#MidLevels', '#PenthouseLiving', '#LuxuryRental', '#HarborViews', '#Exclusive'],
                    'style': 'professional'
                },
                'posted_at': '2024-01-14T16:20:00Z',
                'scraped_at': '2024-01-14T15:30:00Z'
            },
            {
                'id': 4,
                'title': 'Spacious Family Home in Tai Koo',
                'location': 'Tai Koo, Hong Kong Island',
                'price': 55000,
                'currency': 'HKD',
                'period': 'month',
                'bedrooms': 3,
                'bathrooms': 2,
                'area': 950,
                'image': '/api/placeholder/400/300',
                'source': '28hse',
                'status': 'draft',
                'engagement': {
                    'views': 0,
                    'likes': 0,
                    'comments': 0,
                    'shares': 0
                },
                'ai_generated': {
                    'caption': 'Perfect family home in peaceful Tai Koo! 🏡 This spacious 3-bedroom apartment offers comfort and convenience for growing families. Close to schools, parks, and MTR station. Your family\'s new chapter starts here! 👨‍👩‍👧‍👦 #TaiKoo #FamilyHome #SpaciousLiving',
                    'hashtags': ['#TaiKoo', '#FamilyHome', '#SpaciousLiving', '#FamilyFriendly', '#Convenient'],
                    'style': 'casual'
                },
                'posted_at': None,
                'scraped_at': '2024-01-15T12:00:00Z'
            }
        ]
        
        # Apply filters
        filtered_properties = properties
        
        if search:
            filtered_properties = [p for p in filtered_properties 
                                 if search.lower() in p['title'].lower() or 
                                    search.lower() in p['location'].lower()]
        
        if status != 'all':
            filtered_properties = [p for p in filtered_properties if p['status'] == status]
            
        if source != 'all':
            filtered_properties = [p for p in filtered_properties if p['source'] == source]
        
        # Apply pagination
        start = (page - 1) * limit
        end = start + limit
        paginated_properties = filtered_properties[start:end]
        
        return jsonify({
            'success': True,
            'data': {
                'properties': paginated_properties,
                'total': len(filtered_properties),
                'page': page,
                'limit': limit,
                'total_pages': (len(filtered_properties) + limit - 1) // limit
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@properties_bp.route('/<int:property_id>', methods=['GET'])
@cross_origin()
def get_property(property_id):
    """Get a specific property by ID"""
    try:
        # Mock property detail - in production, this would query the database
        property_detail = {
            'id': property_id,
            'title': 'Modern 2BR Apartment in Central',
            'location': 'Central, Hong Kong Island',
            'price': 45000,
            'currency': 'HKD',
            'period': 'month',
            'bedrooms': 2,
            'bathrooms': 2,
            'area': 800,
            'images': [
                '/api/placeholder/800/600',
                '/api/placeholder/800/600',
                '/api/placeholder/800/600'
            ],
            'source': '28hse',
            'status': 'published',
            'description': 'Beautiful modern apartment with stunning city views...',
            'amenities': ['Air Conditioning', 'Gym', 'Swimming Pool', 'Parking'],
            'engagement': {
                'views': 1250,
                'likes': 89,
                'comments': 12,
                'shares': 5
            },
            'ai_generated': {
                'caption': 'Stunning modern apartment in the heart of Central! ✨',
                'hashtags': ['#CentralLiving', '#ModernApartment'],
                'style': 'engaging'
            },
            'posted_at': '2024-01-15T10:30:00Z',
            'scraped_at': '2024-01-15T09:15:00Z'
        }
        
        return jsonify({
            'success': True,
            'data': property_detail
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@properties_bp.route('/<int:property_id>/publish', methods=['POST'])
@cross_origin()
def publish_property(property_id):
    """Publish a property to Instagram"""
    try:
        data = request.get_json()
        platform = data.get('platform', 'instagram')
        
        # Mock publishing - in production, this would trigger the Make.com workflow
        result = {
            'message': f'Property {property_id} published to {platform}',
            'post_id': f'post_{datetime.now().strftime("%Y%m%d_%H%M%S")}',
            'scheduled_time': datetime.now().isoformat()
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

@properties_bp.route('/<int:property_id>/generate-content', methods=['POST'])
@cross_origin()
def generate_content(property_id):
    """Generate AI content for a property"""
    try:
        data = request.get_json()
        style = data.get('style', 'engaging')
        
        # Mock AI content generation - in production, this would call the AI service
        generated_content = {
            'caption': f'Amazing property with {style} style content generated!',
            'hashtags': ['#PropertyListing', '#HongKong', '#Rental'],
            'image_overlay': '/api/placeholder/400/300',
            'style': style
        }
        
        return jsonify({
            'success': True,
            'data': generated_content
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@properties_bp.route('/stats', methods=['GET'])
@cross_origin()
def get_property_stats():
    """Get property statistics"""
    try:
        stats = {
            'total_properties': 342,
            'published': 156,
            'pending': 89,
            'draft': 97,
            'by_source': {
                '28hse': 145,
                'squarefoot': 112,
                'centaline': 85
            },
            'avg_engagement': 8.7,
            'top_performing': [
                {'id': 3, 'title': 'Luxury 3BR Penthouse', 'engagement': 2100},
                {'id': 1, 'title': 'Modern 2BR Apartment', 'engagement': 1250}
            ]
        }
        
        return jsonify({
            'success': True,
            'data': stats
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

