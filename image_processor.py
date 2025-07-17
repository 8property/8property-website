from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import requests
import cloudinary
import cloudinary.uploader
import os
from typing import Optional, Dict, Any

class ImageProcessor:
    def __init__(self):
        # Configure Cloudinary (you'll need to set these environment variables)
        cloudinary.config(
            cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME', 'dfg1cai07'),
            api_key=os.environ.get('CLOUDINARY_API_KEY', '475588673538526'),
            api_secret=os.environ.get('CLOUDINARY_API_SECRET', 'YgY9UqhPTxuRdBi7PcFvYnfH4V0')
        )
        
        # Try to load a font, fallback to default if not available
        self.font_path = self._get_font_path()
        
    def _get_font_path(self) -> str:
        """Get available font path"""
        possible_fonts = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            "/System/Library/Fonts/Arial.ttf",  # macOS
            "arial.ttf"  # Windows
        ]
        
        for font_path in possible_fonts:
            if os.path.exists(font_path):
                return font_path
        
        return None  # Will use default font
    
    def create_property_overlay(self, 
                              image_url: str, 
                              property_data: Dict[str, Any],
                              overlay_style: str = "modern") -> Optional[str]:
        """
        Create an image with property information overlay
        
        Args:
            image_url: URL of the property image
            property_data: Dictionary containing property information
            overlay_style: Style of overlay ("modern", "classic", "minimal")
            
        Returns:
            Cloudinary URL of the processed image or None if failed
        """
        try:
            # Download the original image
            response = requests.get(image_url.strip(), timeout=10)
            if response.status_code != 200:
                return None
                
            original_image = Image.open(BytesIO(response.content)).convert("RGB")
            
            # Resize to standard Instagram size (1080x1080)
            size = 1080
            original_image = original_image.resize((size, size), Image.Resampling.LANCZOS)
            
            # Create overlay based on style
            if overlay_style == "modern":
                processed_image = self._create_modern_overlay(original_image, property_data)
            elif overlay_style == "classic":
                processed_image = self._create_classic_overlay(original_image, property_data)
            else:  # minimal
                processed_image = self._create_minimal_overlay(original_image, property_data)
            
            # Upload to Cloudinary
            image_bytes = BytesIO()
            processed_image.save(image_bytes, format='PNG', quality=95)
            image_bytes.seek(0)
            
            # Generate unique public_id
            property_id = property_data.get('listing_url', '').split('/')[-1] or 'property'
            public_id = f"enriched_{property_id}_{overlay_style}"
            
            upload_response = cloudinary.uploader.upload(
                image_bytes,
                public_id=public_id,
                overwrite=True,
                format="png"
            )
            
            return upload_response["secure_url"]
            
        except Exception as e:
            print(f"Error processing image: {e}")
            return None
    
    def _create_modern_overlay(self, image: Image.Image, data: Dict[str, Any]) -> Image.Image:
        """Create modern style overlay with gradient background"""
        draw = ImageDraw.Draw(image)
        width, height = image.size
        
        # Create gradient overlay at bottom
        overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        
        # Gradient from transparent to semi-transparent black
        gradient_height = height // 3
        for y in range(gradient_height):
            alpha = int(120 * (y / gradient_height))
            overlay_draw.rectangle(
                [(0, height - gradient_height + y), (width, height - gradient_height + y + 1)],
                fill=(0, 0, 0, alpha)
            )
        
        # Composite the overlay
        image = Image.alpha_composite(image.convert("RGBA"), overlay)
        draw = ImageDraw.Draw(image)
        
        # Prepare text
        price = data.get('price', 'N/A')
        title = data.get('title', 'Property Listing')
        area = data.get('saleable_area', data.get('usable_area', 'N/A'))
        rooms = data.get('rooms', 'N/A')
        
        # Font sizes
        try:
            if self.font_path:
                title_font = ImageFont.truetype(self.font_path, 36)
                price_font = ImageFont.truetype(self.font_path, 48)
                detail_font = ImageFont.truetype(self.font_path, 24)
            else:
                title_font = ImageFont.load_default()
                price_font = ImageFont.load_default()
                detail_font = ImageFont.load_default()
        except:
            title_font = ImageFont.load_default()
            price_font = ImageFont.load_default()
            detail_font = ImageFont.load_default()
        
        # Draw text
        y_offset = height - 180
        
        # Price (prominent)
        if price != 'N/A':
            price_text = f"${price}" if not price.startswith('$') else price
            draw.text((30, y_offset), price_text, font=price_font, fill=(255, 255, 255))
            y_offset += 60
        
        # Property details
        details = []
        if area != 'N/A':
            details.append(f"面積: {area}")
        if rooms != 'N/A':
            details.append(f"{rooms}")
        
        if details:
            detail_text = " | ".join(details)
            draw.text((30, y_offset), detail_text, font=detail_font, fill=(255, 255, 255))
            y_offset += 35
        
        # Title (truncated if too long)
        if len(title) > 40:
            title = title[:37] + "..."
        draw.text((30, y_offset), title, font=title_font, fill=(255, 255, 255))
        
        # Add branding
        brand_text = "🏠 PropertyBot"
        draw.text((width - 200, 30), brand_text, font=detail_font, fill=(255, 255, 255))
        
        return image.convert("RGB")
    
    def _create_classic_overlay(self, image: Image.Image, data: Dict[str, Any]) -> Image.Image:
        """Create classic style overlay with solid background"""
        draw = ImageDraw.Draw(image)
        width, height = image.size
        
        # Create solid overlay at bottom
        overlay_height = 150
        overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        overlay_draw.rectangle(
            [(0, height - overlay_height), (width, height)],
            fill=(0, 0, 0, 180)
        )
        
        # Composite the overlay
        image = Image.alpha_composite(image.convert("RGBA"), overlay)
        draw = ImageDraw.Draw(image)
        
        # Prepare text
        price = data.get('price', 'N/A')
        development = data.get('development', data.get('title', 'Property'))
        area = data.get('saleable_area', data.get('usable_area', 'N/A'))
        
        # Font
        try:
            if self.font_path:
                font = ImageFont.truetype(self.font_path, 28)
                small_font = ImageFont.truetype(self.font_path, 20)
            else:
                font = ImageFont.load_default()
                small_font = ImageFont.load_default()
        except:
            font = ImageFont.load_default()
            small_font = ImageFont.load_default()
        
        # Draw text
        y_start = height - 130
        
        # Development name
        if len(development) > 35:
            development = development[:32] + "..."
        draw.text((20, y_start), development, font=font, fill=(255, 255, 255))
        
        # Price and area
        details = []
        if price != 'N/A':
            price_text = f"租金: ${price}" if not price.startswith('$') else f"租金: {price}"
            details.append(price_text)
        if area != 'N/A':
            details.append(f"面積: {area}")
        
        if details:
            detail_text = " | ".join(details)
            draw.text((20, y_start + 35), detail_text, font=small_font, fill=(255, 255, 255))
        
        return image.convert("RGB")
    
    def _create_minimal_overlay(self, image: Image.Image, data: Dict[str, Any]) -> Image.Image:
        """Create minimal style overlay with just price"""
        draw = ImageDraw.Draw(image)
        width, height = image.size
        
        price = data.get('price', 'N/A')
        if price == 'N/A':
            return image
        
        # Create small overlay for price
        try:
            if self.font_path:
                font = ImageFont.truetype(self.font_path, 32)
            else:
                font = ImageFont.load_default()
        except:
            font = ImageFont.load_default()
        
        # Price badge in top-right corner
        price_text = f"${price}" if not price.startswith('$') else price
        
        # Calculate text size
        bbox = draw.textbbox((0, 0), price_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Create badge background
        badge_padding = 15
        badge_x = width - text_width - badge_padding * 2 - 20
        badge_y = 20
        badge_width = text_width + badge_padding * 2
        badge_height = text_height + badge_padding * 2
        
        # Draw badge background
        draw.rounded_rectangle(
            [(badge_x, badge_y), (badge_x + badge_width, badge_y + badge_height)],
            radius=10,
            fill=(0, 0, 0, 200)
        )
        
        # Draw price text
        draw.text(
            (badge_x + badge_padding, badge_y + badge_padding),
            price_text,
            font=font,
            fill=(255, 255, 255)
        )
        
        return image
    
    def create_collage(self, image_urls: list, property_data: Dict[str, Any]) -> Optional[str]:
        """
        Create a collage from multiple property images
        
        Args:
            image_urls: List of image URLs
            property_data: Property information
            
        Returns:
            Cloudinary URL of the collage or None if failed
        """
        try:
            if not image_urls or len(image_urls) < 2:
                return None
            
            # Download images
            images = []
            for url in image_urls[:4]:  # Max 4 images
                try:
                    response = requests.get(url.strip(), timeout=10)
                    if response.status_code == 200:
                        img = Image.open(BytesIO(response.content)).convert("RGB")
                        images.append(img)
                except:
                    continue
            
            if len(images) < 2:
                return None
            
            # Create collage layout
            if len(images) == 2:
                collage = self._create_2_image_collage(images)
            elif len(images) == 3:
                collage = self._create_3_image_collage(images)
            else:
                collage = self._create_4_image_collage(images)
            
            # Add property info overlay
            collage = self._create_minimal_overlay(collage, property_data)
            
            # Upload to Cloudinary
            image_bytes = BytesIO()
            collage.save(image_bytes, format='PNG', quality=95)
            image_bytes.seek(0)
            
            property_id = property_data.get('listing_url', '').split('/')[-1] or 'property'
            public_id = f"collage_{property_id}"
            
            upload_response = cloudinary.uploader.upload(
                image_bytes,
                public_id=public_id,
                overwrite=True,
                format="png"
            )
            
            return upload_response["secure_url"]
            
        except Exception as e:
            print(f"Error creating collage: {e}")
            return None
    
    def _create_2_image_collage(self, images: list) -> Image.Image:
        """Create side-by-side collage"""
        size = 1080
        collage = Image.new("RGB", (size, size), (255, 255, 255))
        
        # Resize images
        img1 = images[0].resize((size // 2, size), Image.Resampling.LANCZOS)
        img2 = images[1].resize((size // 2, size), Image.Resampling.LANCZOS)
        
        # Paste images
        collage.paste(img1, (0, 0))
        collage.paste(img2, (size // 2, 0))
        
        return collage
    
    def _create_3_image_collage(self, images: list) -> Image.Image:
        """Create 3-image collage"""
        size = 1080
        collage = Image.new("RGB", (size, size), (255, 255, 255))
        
        # Main image on left, two smaller on right
        main_img = images[0].resize((size // 2, size), Image.Resampling.LANCZOS)
        img2 = images[1].resize((size // 2, size // 2), Image.Resampling.LANCZOS)
        img3 = images[2].resize((size // 2, size // 2), Image.Resampling.LANCZOS)
        
        collage.paste(main_img, (0, 0))
        collage.paste(img2, (size // 2, 0))
        collage.paste(img3, (size // 2, size // 2))
        
        return collage
    
    def _create_4_image_collage(self, images: list) -> Image.Image:
        """Create 2x2 grid collage"""
        size = 1080
        collage = Image.new("RGB", (size, size), (255, 255, 255))
        
        # 2x2 grid
        half_size = size // 2
        positions = [(0, 0), (half_size, 0), (0, half_size), (half_size, half_size)]
        
        for i, img in enumerate(images[:4]):
            resized_img = img.resize((half_size, half_size), Image.Resampling.LANCZOS)
            collage.paste(resized_img, positions[i])
        
        return collage

