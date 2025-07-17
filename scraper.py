from flask import Blueprint, jsonify
from src.scraper import HseScraperService

scraper_bp = Blueprint('scraper', __name__)

@scraper_bp.route('/')
def home():
    return "✅ 28Hse Rent Scraper is running."

@scraper_bp.route('/run', methods=['GET'])
def run_scraper():
    """Run the 28Hse scraper and return JSON results"""
    try:
        scraper = HseScraperService()
        scraper.scrape_listings()
        results = scraper.get_results_as_json()
        
        return jsonify(results)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@scraper_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "28hse-scraper",
        "version": "1.0.0"
    })

