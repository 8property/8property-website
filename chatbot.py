from flask import Blueprint, request, jsonify
import json
import re
from datetime import datetime

chatbot_bp = Blueprint('chatbot', __name__)

# Simple chatbot responses and logic
class PropertyChatbot:
    def __init__(self):
        self.context = {}
        
    def process_message(self, message, user_id="default"):
        """Process user message and return appropriate response"""
        message = message.lower().strip()
        
        # Initialize user context if not exists
        if user_id not in self.context:
            self.context[user_id] = {
                'stage': 'greeting',
                'preferences': {},
                'last_search': None
            }
        
        user_context = self.context[user_id]
        
        # Greeting responses
        if any(word in message for word in ['hello', 'hi', 'hey', '你好', 'hola']):
            user_context['stage'] = 'greeting'
            return {
                'message': "Hello! 👋 I'm your property assistant. I can help you find the perfect rental property in Hong Kong. What type of property are you looking for?",
                'suggestions': [
                    "Show me 1-bedroom apartments",
                    "I need a 2-bedroom place",
                    "What's available under $20,000?",
                    "Properties in Central area"
                ]
            }
        
        # Price inquiries
        price_match = re.search(r'(\d+,?\d*)', message)
        if any(word in message for word in ['price', 'cost', 'budget', 'under', 'below', '$']):
            if price_match:
                budget = price_match.group(1).replace(',', '')
                user_context['preferences']['budget'] = int(budget)
                return {
                    'message': f"Great! I'll help you find properties under ${budget:,}. What area are you interested in?",
                    'suggestions': [
                        "Central/Admiralty",
                        "Causeway Bay",
                        "Tsim Sha Tsui",
                        "Wan Chai",
                        "Any area is fine"
                    ]
                }
            else:
                return {
                    'message': "What's your budget range? Please let me know your maximum monthly rent.",
                    'suggestions': [
                        "Under $15,000",
                        "$15,000 - $25,000", 
                        "$25,000 - $40,000",
                        "Above $40,000"
                    ]
                }
        
        # Room/bedroom inquiries
        if any(word in message for word in ['room', 'bedroom', 'bed']):
            room_match = re.search(r'(\d+)', message)
            if room_match:
                rooms = room_match.group(1)
                user_context['preferences']['rooms'] = rooms
                return {
                    'message': f"Perfect! Looking for {rooms}-bedroom properties. What's your budget range?",
                    'suggestions': [
                        "Under $20,000",
                        "$20,000 - $30,000",
                        "$30,000 - $50,000",
                        "Budget is flexible"
                    ]
                }
            else:
                return {
                    'message': "How many bedrooms do you need?",
                    'suggestions': [
                        "Studio/1 bedroom",
                        "2 bedrooms", 
                        "3 bedrooms",
                        "4+ bedrooms"
                    ]
                }
        
        # Area/location inquiries
        if any(word in message for word in ['area', 'location', 'district', 'where', 'central', 'causeway', 'tsim', 'wan chai', 'admiralty']):
            areas = []
            if 'central' in message or 'admiralty' in message:
                areas.append('Central/Admiralty')
            if 'causeway' in message:
                areas.append('Causeway Bay')
            if 'tsim' in message:
                areas.append('Tsim Sha Tsui')
            if 'wan chai' in message:
                areas.append('Wan Chai')
                
            if areas:
                user_context['preferences']['area'] = areas[0]
                return {
                    'message': f"Excellent choice! {areas[0]} is a great area. Let me search for available properties that match your criteria.",
                    'suggestions': [
                        "Search now",
                        "Add more preferences",
                        "Show me all options",
                        "Contact an agent"
                    ]
                }
            else:
                return {
                    'message': "Which area interests you most?",
                    'suggestions': [
                        "Hong Kong Island",
                        "Kowloon",
                        "New Territories", 
                        "No preference"
                    ]
                }
        
        # Search requests
        if any(word in message for word in ['search', 'find', 'show', 'available', 'properties']):
            preferences = user_context['preferences']
            search_params = []
            
            if 'budget' in preferences:
                search_params.append(f"Budget: Under ${preferences['budget']:,}")
            if 'rooms' in preferences:
                search_params.append(f"Bedrooms: {preferences['rooms']}")
            if 'area' in preferences:
                search_params.append(f"Area: {preferences['area']}")
                
            if search_params:
                criteria = ", ".join(search_params)
                return {
                    'message': f"🔍 Searching for properties with your criteria: {criteria}\n\nI found several matching properties! You can view them in the listings above. Would you like me to connect you with an agent for more details?",
                    'suggestions': [
                        "Contact an agent",
                        "Refine my search",
                        "Save these results",
                        "Start over"
                    ]
                }
            else:
                return {
                    'message': "I'd be happy to search for properties! Please tell me your preferences first - budget, number of bedrooms, and preferred area.",
                    'suggestions': [
                        "I need a 2-bedroom under $25,000",
                        "Show me 1-bedroom in Central",
                        "Budget under $20,000",
                        "Any 3-bedroom apartment"
                    ]
                }
        
        # Agent contact requests
        if any(word in message for word in ['agent', 'contact', 'call', 'speak', 'talk', 'meet']):
            return {
                'message': "I'll connect you with one of our experienced property agents! 👨‍💼\n\nOur agents can:\n• Arrange property viewings\n• Provide detailed property information\n• Assist with rental applications\n• Answer specific questions\n\nPlease provide your contact details and preferred contact method.",
                'suggestions': [
                    "WhatsApp contact",
                    "Phone call",
                    "Email contact",
                    "Schedule viewing"
                ]
            }
        
        # Help requests
        if any(word in message for word in ['help', 'what can you do', 'options']):
            return {
                'message': "I'm here to help you find the perfect rental property! 🏠\n\nI can help you with:\n• Finding properties by budget, size, and location\n• Providing property details and photos\n• Connecting you with our agents\n• Scheduling property viewings\n• Answering questions about rentals\n\nWhat would you like to do?",
                'suggestions': [
                    "Find properties",
                    "Contact an agent", 
                    "Learn about areas",
                    "Rental process info"
                ]
            }
        
        # Default response
        return {
            'message': "I understand you're looking for property information. Could you please be more specific about what you need? For example, your budget, preferred number of bedrooms, or area of interest?",
            'suggestions': [
                "I need help finding a property",
                "What's my budget options?",
                "Show me available areas",
                "Contact an agent"
            ]
        }

# Initialize chatbot instance
chatbot = PropertyChatbot()

@chatbot_bp.route('/api/chatbot/message', methods=['POST'])
def chat_message():
    """Handle chatbot message from user"""
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({
                'success': False,
                'error': 'Message is required'
            }), 400
        
        user_message = data['message']
        user_id = data.get('user_id', 'default')
        
        # Process message through chatbot
        response = chatbot.process_message(user_message, user_id)
        
        return jsonify({
            'success': True,
            'response': response,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@chatbot_bp.route('/api/chatbot/reset', methods=['POST'])
def reset_chat():
    """Reset chat context for user"""
    try:
        data = request.get_json()
        user_id = data.get('user_id', 'default') if data else 'default'
        
        # Reset user context
        if user_id in chatbot.context:
            del chatbot.context[user_id]
        
        return jsonify({
            'success': True,
            'message': 'Chat context reset successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@chatbot_bp.route('/api/chatbot/health', methods=['GET'])
def chatbot_health():
    """Health check for chatbot service"""
    return jsonify({
        'success': True,
        'message': 'Chatbot service is running',
        'active_users': len(chatbot.context)
    })

