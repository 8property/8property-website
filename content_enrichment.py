from typing import Dict, Any, List, Optional
from .image_processor import ImageProcessor
from .text_generator import TextGenerator
import json

class ContentEnrichmentService:
    def __init__(self):
        self.image_processor = ImageProcessor()
        self.text_generator = TextGenerator()
    
    def enrich_property_listing(self, 
                              property_data: Dict[str, Any],
                              options: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Enrich a property listing with AI-generated content
        
        Args:
            property_data: Raw property data from scraper
            options: Enrichment options (style, format, etc.)
            
        Returns:
            Enriched property data with generated content
        """
        if options is None:
            options = {}
        
        enriched_data = property_data.copy()
        
        # Generate text content
        caption_style = options.get('caption_style', 'engaging')
        enriched_data['ai_caption'] = self.text_generator.generate_instagram_caption(
            property_data, caption_style
        )
        
        enriched_data['ai_summary'] = self.text_generator.generate_property_summary(
            property_data
        )
        
        enriched_data['ai_hashtags'] = self.text_generator.generate_hashtags(
            property_data
        )
        
        # Process images
        image_style = options.get('image_style', 'modern')
        create_collage = options.get('create_collage', False)
        
        # Get primary image
        primary_image_url = self._get_primary_image_url(property_data)
        if primary_image_url:
            enriched_image_url = self.image_processor.create_property_overlay(
                primary_image_url, property_data, image_style
            )
            if enriched_image_url:
                enriched_data['ai_enriched_image'] = enriched_image_url
        
        # Create collage if requested and multiple images available
        if create_collage:
            image_urls = self._get_all_image_urls(property_data)
            if len(image_urls) >= 2:
                collage_url = self.image_processor.create_collage(image_urls, property_data)
                if collage_url:
                    enriched_data['ai_collage_image'] = collage_url
        
        # Add metadata
        enriched_data['enrichment_metadata'] = {
            'processed_at': self._get_current_timestamp(),
            'caption_style': caption_style,
            'image_style': image_style,
            'has_enriched_image': 'ai_enriched_image' in enriched_data,
            'has_collage': 'ai_collage_image' in enriched_data,
            'hashtag_count': len(enriched_data.get('ai_hashtags', []))
        }
        
        return enriched_data
    
    def enrich_news_article(self, news_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enrich a news article with AI-generated social media content
        
        Args:
            news_data: Raw news data from scraper
            
        Returns:
            Enriched news data with generated content
        """
        enriched_data = news_data.copy()
        
        # Generate social media content
        enriched_data['ai_caption'] = self.text_generator.generate_news_summary(news_data)
        
        # Add metadata
        enriched_data['enrichment_metadata'] = {
            'processed_at': self._get_current_timestamp(),
            'content_type': 'news'
        }
        
        return enriched_data
    
    def batch_enrich_listings(self, 
                            listings: List[Dict[str, Any]],
                            options: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Enrich multiple property listings in batch
        
        Args:
            listings: List of property data dictionaries
            options: Enrichment options
            
        Returns:
            List of enriched property data
        """
        enriched_listings = []
        
        for i, listing in enumerate(listings):
            try:
                print(f"Enriching listing {i+1}/{len(listings)}")
                enriched_listing = self.enrich_property_listing(listing, options)
                enriched_listings.append(enriched_listing)
            except Exception as e:
                print(f"Error enriching listing {i+1}: {e}")
                # Add original listing with error metadata
                listing['enrichment_error'] = str(e)
                enriched_listings.append(listing)
        
        return enriched_listings
    
    def create_instagram_post_data(self, enriched_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create Instagram-ready post data from enriched property data
        
        Args:
            enriched_data: Enriched property data
            
        Returns:
            Instagram post data structure
        """
        # Determine best image to use
        image_url = None
        if 'ai_enriched_image' in enriched_data:
            image_url = enriched_data['ai_enriched_image']
        elif 'ai_collage_image' in enriched_data:
            image_url = enriched_data['ai_collage_image']
        else:
            image_url = self._get_primary_image_url(enriched_data)
        
        # Prepare caption
        caption = enriched_data.get('ai_caption', '')
        hashtags = enriched_data.get('ai_hashtags', [])
        
        if hashtags:
            caption += '\n\n' + ' '.join(hashtags)
        
        post_data = {
            'image_url': image_url,
            'caption': caption,
            'listing_url': enriched_data.get('listing_url', ''),
            'property_title': enriched_data.get('title', ''),
            'price': enriched_data.get('price', ''),
            'source': enriched_data.get('source', 'unknown'),
            'post_type': 'property_listing'
        }
        
        return post_data
    
    def _get_primary_image_url(self, data: Dict[str, Any]) -> Optional[str]:
        """Get the primary image URL from property data"""
        # Try different possible image field names
        image_fields = ['image_url', 'photo_url', 'image_url1']
        
        for field in image_fields:
            if field in data and data[field]:
                return data[field]
        
        return None
    
    def _get_all_image_urls(self, data: Dict[str, Any]) -> List[str]:
        """Get all image URLs from property data"""
        image_urls = []
        
        # Check for numbered image fields (image_url1, image_url2, etc.)
        for i in range(1, 21):  # Check up to 20 images
            field_name = 'image_url' if i == 1 else f'image_url{i}'
            if field_name in data and data[field_name]:
                image_urls.append(data[field_name])
        
        # Also check for other possible image fields
        other_fields = ['photo_url', 'image_url']
        for field in other_fields:
            if field in data and data[field] and data[field] not in image_urls:
                image_urls.append(data[field])
        
        return image_urls
    
    def _get_current_timestamp(self) -> str:
        """Get current timestamp in ISO format"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def get_enrichment_stats(self, enriched_listings: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Get statistics about the enrichment process
        
        Args:
            enriched_listings: List of enriched listings
            
        Returns:
            Statistics dictionary
        """
        total_listings = len(enriched_listings)
        successful_enrichments = 0
        has_enriched_images = 0
        has_collages = 0
        has_errors = 0
        
        for listing in enriched_listings:
            if 'enrichment_error' not in listing:
                successful_enrichments += 1
            else:
                has_errors += 1
            
            if 'ai_enriched_image' in listing:
                has_enriched_images += 1
            
            if 'ai_collage_image' in listing:
                has_collages += 1
        
        return {
            'total_listings': total_listings,
            'successful_enrichments': successful_enrichments,
            'success_rate': successful_enrichments / total_listings if total_listings > 0 else 0,
            'has_enriched_images': has_enriched_images,
            'has_collages': has_collages,
            'has_errors': has_errors,
            'error_rate': has_errors / total_listings if total_listings > 0 else 0
        }

