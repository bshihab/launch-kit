"""
User Context Agent - A2A Compatible
Analyzes the user's resume and LinkedIn profile to understand their background and goals
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import json
import os
from datetime import datetime
import logging
from typing import Dict, Any
from dotenv import load_dotenv
import fitz  # PyMuPDF

# Load environment variables
load_dotenv()

# Configure logging
log_level = os.getenv('LOG_LEVEL', 'INFO')
logging.basicConfig(level=getattr(logging, log_level))
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Configuration
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
FLASK_ENV = os.getenv('FLASK_ENV', 'development')
PORT = int(os.getenv('PORT', 8081)) # Different port from profile-analysis
AGENT_VERSION = os.getenv('AGENT_VERSION', '1.0.0')

# Configure Gemini
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('models/gemini-1.5-flash')
    logger.info("Gemini API configured successfully for User Context Agent")
else:
    logger.warning("No Gemini API key found - User Context Agent will use mock data")

class UserContextAgent:
    """A2A-compatible agent for user profile and resume analysis"""
    
    def __init__(self):
        self.agent_card = {
            "name": "User Context Agent",
            "description": "Analyzes a user's resume and LinkedIn profile to create a comprehensive user context.",
            "version": AGENT_VERSION,
            "capabilities": [
                "resume_parsing",
                "linkedin_profile_analysis",
                "goal_identification",
                "skill_mapping"
            ],
            "input_schema": {
                "type": "object",
                "properties": {
                    "user_linkedin_url": {"type": "string", "description": "URL of the user's LinkedIn profile"},
                    "user_resume_file_path": {"type": "string", "description": "Local file path to the user's PDF resume"}
                },
                "required": ["user_linkedin_url", "user_resume_file_path"]
            },
            "output_schema": {
                "type": "object",
                "properties": {
                    "user_context": {"type": "object"},
                    "analysis_metadata": {"type": "object"}
                }
            }
        }
    
    def _extract_text_from_pdf(self, file_path: str) -> str:
        """Extracts text content from a PDF file."""
        try:
            doc = fitz.open(file_path)
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()
            logger.info(f"Successfully extracted text from {file_path}")
            return text
        except Exception as e:
            logger.error(f"Error reading or parsing PDF at {file_path}: {str(e)}")
            raise

    def analyze_user_context(self, linkedin_url: str, resume_text: str) -> Dict[str, Any]:
        """Use Gemini to analyze the user's data and create a context profile."""
        
        if not GEMINI_API_KEY:
            return self._get_mock_analysis()
        
        try:
            # AI prompt for user context analysis
            prompt = f"""You are a JSON-generating AI that creates a professional profile from a resume and LinkedIn URL.
            
            Resume Text:
            {resume_text}

            LinkedIn URL: {linkedin_url}

            Instructions:
            1. Return ONLY a valid JSON object.
            2. Analyze the provided resume and LinkedIn information.
            3. Synthesize the information to create a detailed professional profile.
            4. Keep the exact same structure and keys as the example below.
            
            Return this exact JSON structure (with your analysis):
            {{
                "summary": "A brief professional summary of the user.",
                "key_skills": ["Skill 1", "Skill 2", "Skill 3"],
                "professional_goals": "Inferred professional goals, like 'seeking a role in product management'.",
                "target_industries": ["Industry 1", "Industry 2"],
                "unique_selling_points": [
                    "What makes the user stand out, e.g., 'Bilingual in English and Spanish'",
                    "Specific achievement, e.g., 'Increased user engagement by 15%'"
                ]
            }}"""
            
            response = model.generate_content(prompt)
            logger.info(f"Raw Gemini response for user context: {response.text}")
            
            # Clean and parse the response
            text = response.text.strip().replace('```json', '').replace('```', '').strip()
            ai_analysis = json.loads(text)
            logger.info("Successfully parsed Gemini response for user context as JSON")
            return ai_analysis
            
        except Exception as e:
            logger.error(f"Error in AI analysis for user context: {str(e)}")
            return self._get_mock_analysis(error=str(e))
    
    def _get_mock_analysis(self, error: str = None) -> Dict[str, Any]:
        """Return mock analysis data for user context."""
        analysis = {
            "summary": "A mock professional summary for the user.",
            "key_skills": ["Project Management", "Data Analysis", "Public Speaking"],
            "professional_goals": "Seeking an entry-level role in marketing.",
            "target_industries": ["Technology", "Marketing & Advertising"],
            "unique_selling_points": ["Experience with social media campaigns", "Certified in Google Analytics"]
        }
        if error:
            analysis["ai_analysis_error"] = error
        return analysis

    def process_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Main A2A task processing method for user context."""
        try:
            linkedin_url = task_data.get('input', {}).get('user_linkedin_url')
            resume_path = task_data.get('input', {}).get('user_resume_file_path')
            
            if not linkedin_url or not resume_path:
                raise ValueError("user_linkedin_url and user_resume_file_path are required")

            # Extract text from the PDF resume
            resume_text = self._extract_text_from_pdf(resume_path)
            
            logger.info(f"Starting user context analysis for: {linkedin_url}")
            user_context = self.analyze_user_context(linkedin_url, resume_text)
            
            result = {
                "task_id": task_data.get('task_id', f"user_context_{datetime.now().timestamp()}"),
                "agent_info": self.agent_card,
                "status": "completed",
                "output": {
                    "user_context": user_context,
                    "analysis_metadata": {
                        "processed_at": datetime.now().isoformat()
                    }
                },
                "next_suggested_agents": ["connection_mapping_agent"]
            }
            
            logger.info(f"Successfully completed user context analysis for: {linkedin_url}")
            return result
            
        except Exception as e:
            logger.error(f"Error processing user context task: {str(e)}")
            return {
                "task_id": task_data.get('task_id', "error"),
                "agent_info": self.agent_card,
                "status": "error",
                "error": {"message": str(e), "type": type(e).__name__}
            }

# Initialize agent
agent = UserContextAgent()

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "agent": agent.agent_card["name"],
        "version": agent.agent_card["version"],
        "timestamp": datetime.now().isoformat()
    })

@app.route('/agent-card', methods=['GET'])
def get_agent_card():
    return jsonify(agent.agent_card)

@app.route('/analyze-user', methods=['POST'])
def analyze_user():
    """Main endpoint for user context analysis."""
    try:
        task_data = request.get_json()
        if not task_data:
            return jsonify({"status": "error", "error": "No task data provided"}), 400
        
        result = agent.process_task(task_data)
        status_code = 200 if result.get('status') == 'completed' else 500
        return jsonify(result), status_code
        
    except Exception as e:
        logger.error(f"Error in analyze-user endpoint: {str(e)}")
        return jsonify({"status": "error", "error": str(e)}), 500

if __name__ == '__main__':
    debug_mode = FLASK_ENV == 'development'
    logger.info(f"Starting User Context Agent v{AGENT_VERSION} on port {PORT}")
    app.run(host='0.0.0.0', port=PORT, debug=debug_mode)
