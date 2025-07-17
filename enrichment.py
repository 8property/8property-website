from flask import Blueprint, request, jsonify
from src.services.content_enrichment import ContentEnrichmentService
import json

enrichment_bp = Blueprint('enrichment', __name__)

# Initialize the content enrichment service
enrichment_service = ContentEnrichmentService()

@enrichment_bp.route('/')
def home():
    return "✅ AI Content Enrichment Service is running."

@enrichment_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "ai-content-enrichment",
        "version": "1.0.0"
    })

@enrichment_bp.route('/enrich/property', methods=['POST'])
def enrich_property():
    """
    Enrich a single property listing
    
    Expected JSON payload:
    {
        "property_data": {...},
        "options": {
            "caption_style": "engaging|professional|casual",
            "image_style": "modern|classic|minimal",
            "create_collage": true|false
        }
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'property_data' not in data:
            return jsonify({"error": "Missing property_data in request"}), 400
        
        property_data = data['property_data']
        options = data.get('options', {})
        
        # Enrich the property listing
        enriched_data = enrichment_service.enrich_property_listing(property_data, options)
        
        return jsonify({
            "success": True,
            "enriched_data": enriched_data
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@enrichment_bp.route('/enrich/properties/batch', methods=['POST'])
def enrich_properties_batch():
    """
    Enrich multiple property listings in batch
    
    Expected JSON payload:
    {
        "listings": [...],
        "options": {...}
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'listings' not in data:
            return jsonify({"error": "Missing listings in request"}), 400
        
        listings = data['listings']
        options = data.get('options', {})
        
        if not isinstance(listings, list):
            return jsonify({"error": "listings must be an array"}), 400
        
        # Enrich all listings
        enriched_listings = enrichment_service.batch_enrich_listings(listings, options)
        
        # Get statistics
        stats = enrichment_service.get_enrichment_stats(enriched_listings)
        
        return jsonify({
            "success": True,
            "enriched_listings": enriched_listings,
            "stats": stats
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@enrichment_bp.route('/enrich/news', methods=['POST'])
def enrich_news():
    """
    Enrich a news article for social media
    
    Expected JSON payload:
    {
        "news_data": {...}
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'news_data' not in data:
            return jsonify({"error": "Missing news_data in request"}), 400
        
        news_data = data['news_data']
        
        # Enrich the news article
        enriched_data = enrichment_service.enrich_news_article(news_data)
        
        return jsonify({
            "success": True,
            "enriched_data": enriched_data
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@enrichment_bp.route('/generate/instagram-post', methods=['POST'])
def generate_instagram_post():
    """
    Generate Instagram-ready post data from enriched property data
    
    Expected JSON payload:
    {
        "enriched_data": {...}
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'enriched_data' not in data:
            return jsonify({"error": "Missing enriched_data in request"}), 400
        
        enriched_data = data['enriched_data']
        
        # Create Instagram post data
        post_data = enrichment_service.create_instagram_post_data(enriched_data)
        
        return jsonify({
            "success": True,
            "post_data": post_data
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@enrichment_bp.route('/process/scraper-data', methods=['POST'])
def process_scraper_data():
    """
    Process data directly from scrapers and return Instagram-ready posts
    
    Expected JSON payload:
    {
        "source": "28hse|squarefoot|centaline",
        "listings": [...],
        "options": {...}
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'listings' not in data:
            return jsonify({"error": "Missing listings in request"}), 400
        
        source = data.get('source', 'unknown')
        listings = data['listings']
        options = data.get('options', {})
        
        if not isinstance(listings, list):
            return jsonify({"error": "listings must be an array"}), 400
        
        # Add source to each listing
        for listing in listings:
            listing['source'] = source
        
        # Enrich all listings
        enriched_listings = enrichment_service.batch_enrich_listings(listings, options)
        
        # Create Instagram post data for each enriched listing
        instagram_posts = []
        for enriched_data in enriched_listings:
            if 'enrichment_error' not in enriched_data:  # Only process successful enrichments
                post_data = enrichment_service.create_instagram_post_data(enriched_data)
                instagram_posts.append(post_data)
        
        # Get statistics
        stats = enrichment_service.get_enrichment_stats(enriched_listings)
        stats['instagram_posts_created'] = len(instagram_posts)
        
        return jsonify({
            "success": True,
            "instagram_posts": instagram_posts,
            "enriched_listings": enriched_listings,
            "stats": stats
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@enrichment_bp.route('/test/sample-enrichment', methods=['GET'])
def test_sample_enrichment():
    """Test endpoint with sample data"""
    try:
        # Sample property data
        sample_property = {
            "title": "太古城 3房2廳 海景單位",
            "price": "45000",
            "development": "太古城",
            "saleable_area": "1200呎",
            "rooms": "3房",
            "address": "香港島太古城",
            "floor": "高層",
            "image_url": "https://via.placeholder.com/800x600/0066cc/ffffff?text=Sample+Property",
            "listing_url": "https://example.com/property/123"
        }
        
        # Enrich with default options
        enriched_data = enrichment_service.enrich_property_listing(sample_property)
        
        # Create Instagram post data
        post_data = enrichment_service.create_instagram_post_data(enriched_data)
        
        return jsonify({
            "success": True,
            "sample_enriched_data": enriched_data,
            "sample_post_data": post_data
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

