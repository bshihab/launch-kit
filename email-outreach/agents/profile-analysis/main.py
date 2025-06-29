"""
Profile Analysis Agent - A2A Compatible
Analyzes LinkedIn profiles and extracts structured data for email personalization
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime
import logging
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
log_level = os.getenv('LOG_LEVEL', 'INFO')
logging.basicConfig(level=getattr(logging, log_level))
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
FLASK_ENV = os.getenv('FLASK_ENV', 'development')
PORT = int(os.getenv('PORT', 8080))
AGENT_VERSION = os.getenv('AGENT_VERSION', '1.0.0')
ANALYSIS_DEPTH = os.getenv('ANALYSIS_DEPTH', 'basic')

if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY
    logger.info("OpenAI API key loaded successfully")
else:
    logger.warning("No OpenAI API key found - using mock data")

class ProfileAnalysisAgent:
    """A2A-compatible agent for LinkedIn profile analysis"""
    
    def __init__(self):
        self.agent_card = {
            "name": "Profile Analysis Agent",
            "description": "Extracts and analyzes LinkedIn profile data for email personalization",
            "version": AGENT_VERSION,
            "capabilities": [
                "linkedin_profile_extraction",
                "skill_analysis", 
                "experience_parsing",
                "activity_monitoring"
            ],
            "input_schema": {
                "type": "object",
                "properties": {
                    "linkedin_url": {"type": "string", "description": "LinkedIn profile URL"},
                    "analysis_depth": {"type": "string", "enum": ["basic", "detailed"], "default": "basic"}
                },
                "required": ["linkedin_url"]
            },
            "output_schema": {
                "type": "object",
                "properties": {
                    "profile_data": {"type": "object"},
                    "analysis": {"type": "object"},
                    "extraction_metadata": {"type": "object"}
                }
            }
        }
    
    def extract_linkedin_profile(self, linkedin_url: str) -> Dict[str, Any]:
        """
        Extract profile data from LinkedIn URL
        Note: In production, this would use LinkedIn API or specialized scraping tools
        For now, we'll simulate the extraction and use AI to generate realistic data
        """
        try:
            # Simulate profile extraction (in production, use proper LinkedIn API)
            # For demo purposes, we'll generate realistic profile data
            profile_data = {
                "url": linkedin_url,
                "extraction_method": "simulated",  # In production: "linkedin_api" or "scraping"
                "extracted_at": datetime.now().isoformat(),
                "profile": {
                    "name": "Sample Profile",
                    "headline": "Software Engineer at Tech Company", 
                    "location": "San Francisco, CA",
                    "connections": "500+",
                    "about": "Passionate software engineer with 5+ years of experience...",
                    "experience": [
                        {
                            "title": "Senior Software Engineer",
                            "company": "Tech Company",
                            "duration": "2022 - Present",
                            "description": "Leading backend development for AI-powered applications"
                        }
                    ],
                    "education": [
                        {
                            "school": "University of California, Berkeley",
                            "degree": "Bachelor of Science in Computer Science", 
                            "years": "2017 - 2021"
                        }
                    ],
                    "skills": ["Python", "Machine Learning", "AWS", "React"],
                    "recent_activity": [
                        {
                            "type": "post",
                            "content": "Excited about the latest developments in AI...",
                            "date": "2024-06-20"
                        }
                    ]
                }
            }
            
            logger.info(f"Successfully extracted profile data for: {linkedin_url}")
            return profile_data
            
        except Exception as e:
            logger.error(f"Error extracting profile from {linkedin_url}: {str(e)}")
            raise
    
    def analyze_profile_with_ai(self, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """Use AI to analyze the profile and extract insights for personalization"""
        
        if not OPENAI_API_KEY:
            # Return mock analysis if no API key
            return {
                "personality_traits": ["analytical", "innovative", "collaborative"],
                "communication_style": "professional",
                "interests": ["technology", "artificial intelligence", "startups"],
                "networking_potential": "high",
                "personalization_hooks": [
                    "shared_university",
                    "similar_role", 
                    "common_interests"
                ],
                "ai_analysis": "Mock analysis - configure OpenAI API key for real analysis"
            }
        
        try:
            # Prepare profile summary for AI analysis
            profile_summary = f"""
Name: {profile_data['profile'].get('name', 'Unknown')}
Headline: {profile_data['profile'].get('headline', 'No headline')}
About: {profile_data['profile'].get('about', 'No about section')}
Experience: {json.dumps(profile_data['profile'].get('experience', []))}
Education: {json.dumps(profile_data['profile'].get('education', []))}
Skills: {', '.join(profile_data['profile'].get('skills', []))}
Recent Activity: {json.dumps(profile_data['profile'].get('recent_activity', []))}
"""
            
            # AI prompt for profile analysis
            prompt = f"""
Analyze this LinkedIn profile and provide insights for email personalization:

{profile_summary}

Please provide a JSON response with:
1. personality_traits: Array of 3-5 key personality traits
2. communication_style: Professional communication style (formal/casual/technical)
3. interests: Array of main professional/personal interests  
4. networking_potential: Assessment (low/medium/high)
5. personalization_hooks: Array of potential conversation starters
6. key_achievements: Notable accomplishments to reference
7. connection_opportunities: Ways to build rapport

Focus on actionable insights for crafting personalized outreach emails.
"""
            
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert at analyzing professional profiles for networking and outreach purposes. Provide structured, actionable insights."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1000
            )
            
            # Parse AI response
            ai_analysis = json.loads(response.choices[0].message.content)
            
            logger.info("Successfully completed AI analysis of profile")
            return ai_analysis
            
        except Exception as e:
            logger.error(f"Error in AI analysis: {str(e)}")
            # Return fallback analysis
            return {
                "personality_traits": ["professional"],
                "communication_style": "formal",
                "interests": ["career_development"],
                "networking_potential": "medium", 
                "personalization_hooks": ["professional_background"],
                "ai_analysis_error": str(e)
            }
    
    def process_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Main A2A task processing method"""
        try:
            # Extract input parameters
            linkedin_url = task_data.get('input', {}).get('linkedin_url')
            analysis_depth = task_data.get('input', {}).get('analysis_depth', 'basic')
            
            if not linkedin_url:
                raise ValueError("linkedin_url is required")
            
            # Step 1: Extract profile data
            logger.info(f"Starting profile extraction for: {linkedin_url}")
            profile_data = self.extract_linkedin_profile(linkedin_url)
            
            # Step 2: AI analysis
            logger.info("Starting AI analysis of profile")
            ai_analysis = self.analyze_profile_with_ai(profile_data)
            
            # Step 3: Prepare A2A response
            result = {
                "task_id": task_data.get('task_id', f"profile_analysis_{datetime.now().timestamp()}"),
                "agent_info": self.agent_card,
                "status": "completed",
                "output": {
                    "profile_data": profile_data,
                    "ai_analysis": ai_analysis,
                    "extraction_metadata": {
                        "processed_at": datetime.now().isoformat(),
                        "analysis_depth": analysis_depth,
                        "data_quality": "high" if profile_data['profile']['name'] != "Sample Profile" else "simulated"
                    }
                },
                "next_suggested_agents": [
                    "company_research_agent",
                    "connection_mapping_agent"
                ]
            }
            
            logger.info(f"Successfully completed profile analysis for: {linkedin_url}")
            return result
            
        except Exception as e:
            logger.error(f"Error processing task: {str(e)}")
            return {
                "task_id": task_data.get('task_id', "error"),
                "agent_info": self.agent_card,
                "status": "error",
                "error": {
                    "message": str(e),
                    "type": type(e).__name__,
                    "timestamp": datetime.now().isoformat()
                }
            }

# Initialize agent
agent = ProfileAnalysisAgent()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "agent": agent.agent_card["name"],
        "version": agent.agent_card["version"],
        "timestamp": datetime.now().isoformat()
    })

@app.route('/agent-card', methods=['GET'])
def get_agent_card():
    """Return A2A agent card for capability discovery"""
    return jsonify(agent.agent_card)

@app.route('/analyze', methods=['POST'])
def analyze_profile():
    """Main endpoint for profile analysis - A2A compatible"""
    try:
        task_data = request.get_json()
        
        if not task_data:
            return jsonify({
                "status": "error", 
                "error": "No task data provided"
            }), 400
        
        # Process the task
        result = agent.process_task(task_data)
        
        # Return appropriate status code
        status_code = 200 if result.get('status') == 'completed' else 500
        return jsonify(result), status_code
        
    except Exception as e:
        logger.error(f"Error in analyze endpoint: {str(e)}")
        return jsonify({
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@app.route('/test', methods=['GET'])
def test_endpoint():
    """Test endpoint with sample data"""
    sample_task = {
        "task_id": "test_001",
        "input": {
            "linkedin_url": "https://linkedin.com/in/sample-profile",
            "analysis_depth": "basic"
        }
    }
    
    result = agent.process_task(sample_task)
    return jsonify(result)

if __name__ == '__main__':
    debug_mode = FLASK_ENV == 'development'
    logger.info(f"Starting Profile Analysis Agent v{AGENT_VERSION}")
    logger.info(f"Environment: {FLASK_ENV}")
    logger.info(f"Port: {PORT}")
    logger.info(f"Debug mode: {debug_mode}")
    
    app.run(host='0.0.0.0', port=PORT, debug=debug_mode) 