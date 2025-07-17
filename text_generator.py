import openai
import os
from typing import Dict, Any, List, Optional
import json
import re

class TextGenerator:
    def __init__(self):
        # OpenAI client is already configured via environment variables
        self.client = openai.OpenAI()
        
    def generate_instagram_caption(self, 
                                 property_data: Dict[str, Any], 
                                 style: str = "engaging") -> str:
        """
        Generate Instagram caption for property listing
        
        Args:
            property_data: Dictionary containing property information
            style: Caption style ("engaging", "professional", "casual")
            
        Returns:
            Generated Instagram caption
        """
        try:
            # Extract key information
            title = property_data.get('title', 'Property Listing')
            price = property_data.get('price', 'N/A')
            development = property_data.get('development', '')
            area = property_data.get('saleable_area', property_data.get('usable_area', 'N/A'))
            rooms = property_data.get('rooms', 'N/A')
            address = property_data.get('address', 'N/A')
            floor = property_data.get('floor', 'N/A')
            
            # Create prompt based on style
            if style == "engaging":
                prompt = self._create_engaging_prompt(title, price, development, area, rooms, address, floor)
            elif style == "professional":
                prompt = self._create_professional_prompt(title, price, development, area, rooms, address, floor)
            else:  # casual
                prompt = self._create_casual_prompt(title, price, development, area, rooms, address, floor)
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a professional property marketing expert who creates engaging Instagram captions for Hong Kong rental properties. Always write in Traditional Chinese and include relevant hashtags."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            caption = response.choices[0].message.content.strip()
            
            # Add call-to-action and contact info
            caption += "\n\n💬 有興趣？立即DM查詢詳情！"
            caption += "\n📱 WhatsApp聯絡我們"
            
            return caption
            
        except Exception as e:
            print(f"Error generating caption: {e}")
            return self._create_fallback_caption(property_data)
    
    def _create_engaging_prompt(self, title, price, development, area, rooms, address, floor):
        return f"""
        Create an engaging Instagram caption for this Hong Kong rental property:
        
        Property: {title}
        Development: {development}
        Price: {price}
        Area: {area}
        Rooms: {rooms}
        Floor: {floor}
        Location: {address}
        
        Requirements:
        - Write in Traditional Chinese
        - Use emojis to make it visually appealing
        - Highlight the best features
        - Create excitement and urgency
        - Include relevant hashtags (#租屋 #香港租屋 #物業 etc.)
        - Keep it under 200 characters
        - Make it sound attractive to potential tenants
        """
    
    def _create_professional_prompt(self, title, price, development, area, rooms, address, floor):
        return f"""
        Create a professional Instagram caption for this Hong Kong rental property:
        
        Property: {title}
        Development: {development}
        Price: {price}
        Area: {area}
        Rooms: {rooms}
        Floor: {floor}
        Location: {address}
        
        Requirements:
        - Write in Traditional Chinese
        - Professional and informative tone
        - Focus on facts and features
        - Include relevant hashtags
        - Suitable for serious property seekers
        - Clear and concise
        """
    
    def _create_casual_prompt(self, title, price, development, area, rooms, address, floor):
        return f"""
        Create a casual, friendly Instagram caption for this Hong Kong rental property:
        
        Property: {title}
        Development: {development}
        Price: {price}
        Area: {area}
        Rooms: {rooms}
        Floor: {floor}
        Location: {address}
        
        Requirements:
        - Write in Traditional Chinese
        - Casual and friendly tone
        - Use everyday language
        - Include relevant hashtags
        - Make it feel personal and approachable
        """
    
    def _create_fallback_caption(self, property_data: Dict[str, Any]) -> str:
        """Create a simple fallback caption if AI generation fails"""
        title = property_data.get('title', '物業出租')
        price = property_data.get('price', '')
        
        caption = f"🏠 {title}\n"
        if price:
            caption += f"💰 租金: ${price}\n"
        caption += "\n📍 優質物業，歡迎查詢！\n"
        caption += "💬 DM了解更多詳情\n\n"
        caption += "#租屋 #香港租屋 #物業出租 #apartment #rental #hongkong"
        
        return caption
    
    def generate_property_summary(self, property_data: Dict[str, Any]) -> str:
        """
        Generate a concise property summary for overlays
        
        Args:
            property_data: Dictionary containing property information
            
        Returns:
            Concise property summary
        """
        try:
            title = property_data.get('title', 'Property')
            price = property_data.get('price', 'N/A')
            area = property_data.get('saleable_area', property_data.get('usable_area', 'N/A'))
            rooms = property_data.get('rooms', 'N/A')
            
            prompt = f"""
            Create a very concise property summary (max 3 lines) for image overlay:
            
            Property: {title}
            Price: {price}
            Area: {area}
            Rooms: {rooms}
            
            Requirements:
            - Traditional Chinese
            - Maximum 3 lines
            - Each line max 20 characters
            - Include key selling points
            - No hashtags
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You create very concise property summaries for image overlays in Traditional Chinese."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100,
                temperature=0.5
            )
            
            summary = response.choices[0].message.content.strip()
            
            # Ensure it's not too long
            lines = summary.split('\n')
            if len(lines) > 3:
                lines = lines[:3]
            
            return '\n'.join(lines)
            
        except Exception as e:
            print(f"Error generating summary: {e}")
            return self._create_fallback_summary(property_data)
    
    def _create_fallback_summary(self, property_data: Dict[str, Any]) -> str:
        """Create a simple fallback summary"""
        development = property_data.get('development', property_data.get('title', '物業'))
        price = property_data.get('price', '')
        area = property_data.get('saleable_area', property_data.get('usable_area', ''))
        
        lines = []
        if development:
            lines.append(development[:15])
        if price:
            lines.append(f"${price}")
        if area:
            lines.append(f"面積: {area}")
        
        return '\n'.join(lines[:3])
    
    def generate_hashtags(self, property_data: Dict[str, Any]) -> List[str]:
        """
        Generate relevant hashtags for the property
        
        Args:
            property_data: Dictionary containing property information
            
        Returns:
            List of relevant hashtags
        """
        try:
            address = property_data.get('address', '')
            development = property_data.get('development', '')
            rooms = property_data.get('rooms', '')
            
            prompt = f"""
            Generate relevant Instagram hashtags for this Hong Kong rental property:
            
            Location: {address}
            Development: {development}
            Rooms: {rooms}
            
            Requirements:
            - Mix of Traditional Chinese and English hashtags
            - Include location-based hashtags
            - Include property type hashtags
            - Maximum 15 hashtags
            - Popular and searchable hashtags
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You generate relevant hashtags for Hong Kong property listings."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.6
            )
            
            hashtags_text = response.choices[0].message.content.strip()
            
            # Extract hashtags
            hashtags = re.findall(r'#\w+', hashtags_text)
            
            # Add default hashtags if not enough
            default_hashtags = [
                "#租屋", "#香港租屋", "#物業出租", "#apartment", "#rental", 
                "#hongkong", "#hkproperty", "#hkrental", "#property"
            ]
            
            for tag in default_hashtags:
                if tag not in hashtags and len(hashtags) < 15:
                    hashtags.append(tag)
            
            return hashtags[:15]
            
        except Exception as e:
            print(f"Error generating hashtags: {e}")
            return [
                "#租屋", "#香港租屋", "#物業出租", "#apartment", "#rental", 
                "#hongkong", "#hkproperty", "#hkrental", "#property"
            ]
    
    def generate_news_summary(self, news_data: Dict[str, Any]) -> str:
        """
        Generate engaging summary for property news
        
        Args:
            news_data: Dictionary containing news information
            
        Returns:
            Generated news summary for social media
        """
        try:
            title = news_data.get('title', '')
            summary = news_data.get('summary', '')
            
            prompt = f"""
            Create an engaging Instagram caption for this Hong Kong property news:
            
            Title: {title}
            Summary: {summary}
            
            Requirements:
            - Traditional Chinese
            - Engaging and informative
            - Highlight key insights for property investors/renters
            - Include relevant hashtags
            - Add call-to-action for engagement
            - Maximum 250 characters
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You create engaging social media content for Hong Kong property news."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            caption = response.choices[0].message.content.strip()
            
            # Add engagement prompt
            caption += "\n\n💭 你點睇？留言分享你嘅意見！"
            
            return caption
            
        except Exception as e:
            print(f"Error generating news summary: {e}")
            return f"📰 {title}\n\n{summary[:100]}...\n\n#香港樓市 #地產新聞 #property #hongkong"

