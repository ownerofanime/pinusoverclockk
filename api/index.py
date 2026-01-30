"""
ArtSpace AI Room Analyzer - Vercel Serverless Function
"""

from http.server import BaseHTTPRequestHandler
import json
import os
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

SYSTEM_PROMPT = """You are an expert interior designer and art consultant. Analyze the room photo and recommend artworks.

Your response MUST be valid JSON with this exact structure:
{
    "analysis": {
        "description": "2-3 sentences describing the room's style, colors, and atmosphere",
        "dominantColors": ["color1", "color2", "color3"],
        "style": "modern/traditional/minimalist/eclectic/etc",
        "mood": "calm/energetic/cozy/sophisticated/etc",
        "lighting": "bright/dim/natural/warm/cool"
    },
    "recommendations": [
        {
            "artworkId": 101,
            "matchScore": 95,
            "reason": "Why this artwork fits the room"
        }
    ]
}

Available artwork IDs and their characteristics:
- 101: Starry Night (blue, dramatic, expressive)
- 102: Water Lilies (green, calm, natural)
- 103: Café Terrace (yellow, warm, cozy)
- 104: Mona Lisa (brown, classic, elegant)
- 105: Kandinsky (colorful, energetic, bold)
- 106: Abstract Blue (blue, calm, modern)
- 107: Colorful Abstract (vibrant, playful, fun)
- 108: Golden Abstract (gold, luxurious, warm)
- 109: Botanical Study (green, fresh, natural)
- 110: Classic Portrait (brown, traditional, dignified)
- 111: Great Wave (blue, dramatic, powerful)
- 112: Minimalist Lines (black/white, clean, simple)
- 113: Geometric Patterns (colorful, structured, modern)
- 114: Neon Dreams (neon, futuristic, edgy)
- 115: Traditional Landscape (green, peaceful, scenic)

Recommend 3-5 artworks that best match the room. Consider color harmony, style compatibility, and mood."""


def get_default_recommendations():
    """Return default recommendations as fallback"""
    return {
        "analysis": {
            "description": "This appears to be a well-lit room with a contemporary feel. The space has potential for various art styles depending on your preference.",
            "dominantColors": ["neutral", "white", "gray"],
            "style": "contemporary",
            "mood": "versatile",
            "lighting": "natural"
        },
        "recommendations": [
            {"artworkId": 106, "matchScore": 90, "reason": "Abstract Blue would add a calming focal point to your space"},
            {"artworkId": 112, "matchScore": 85, "reason": "Minimalist Lines would complement a clean, modern aesthetic"},
            {"artworkId": 108, "matchScore": 82, "reason": "Golden Abstract adds warmth and sophistication"},
            {"artworkId": 102, "matchScore": 78, "reason": "Water Lilies brings natural tranquility to any room"}
        ]
    }


class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_POST(self):
        """Handle POST requests for room analysis"""
        # CORS headers
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        try:
            # Read request body
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            data = json.loads(body)
            
            if 'image' not in data:
                self.wfile.write(json.dumps({'error': 'No image provided'}).encode())
                return
            
            image_data = data['image']
            
            # Handle data URL format
            if image_data.startswith('data:'):
                image_data = image_data.split(',')[1] if ',' in image_data else image_data
            
            # Call OpenAI Vision API
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Analyze this room and recommend artworks from the available collection."
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_data}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=1000
            )
            
            # Parse the response
            content = response.choices[0].message.content
            
            # Try to extract JSON
            try:
                if '{' in content and '}' in content:
                    start = content.find('{')
                    end = content.rfind('}') + 1
                    result = json.loads(content[start:end])
                else:
                    result = get_default_recommendations()
            except json.JSONDecodeError:
                result = get_default_recommendations()
            
            self.wfile.write(json.dumps(result).encode())
            
        except Exception as e:
            print(f"Error: {str(e)}")
            self.wfile.write(json.dumps(get_default_recommendations()).encode())
    
    def do_GET(self):
        """Health check endpoint"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({
            'status': 'ok',
            'service': 'ArtSpace AI Room Analyzer'
        }).encode())
