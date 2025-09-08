"""
Email Composition Agent - A2A Compatible
Drafts personalized outreach emails based on collected intelligence.
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

load_dotenv()
logging.basicConfig(level=os.getenv('LOG_LEVEL', 'INFO'))
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
FLASK_ENV = os.getenv('FLASK_ENV', 'development')
PORT = int(os.getenv('PORT', 8084))
AGENT_VERSION = os.getenv('AGENT_VERSION', '1.0.0')

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('models/gemini-1.5-flash')
    logger.info("Gemini API configured for Email Composition Agent")
else:
    logger.warning("No Gemini API key found - Email Composition Agent will use mock data")

class EmailCompositionAgent:
    """A2A agent for drafting personalized emails."""
    
    def __init__(self):
        self.agent_card = {
            "name": "Email Composition Agent",
            "description": "Drafts personalized outreach emails using user context, company research, and connection points.",
            "version": AGENT_VERSION,
            "capabilities": ["email_drafting", "subject_line_generation", "tone_adaptation"],
            "input_schema": {
                "type": "object",
                "properties": {
                    "user_context": {"type": "object"},
                    "company_intelligence": {"type": "object"},
                    "connection_points": {"type": "array"},
                    "email_tone": {"type": "string", "enum": ["formal", "casual", "enthusiastic"], "default": "formal"}
                },
                "required": ["user_context", "company_intelligence", "connection_points"]
            },
            "output_schema": {
                "type": "object",
                "properties": {
                    "draft_email": {"type": "object"},
                    "composition_metadata": {"type": "object"}
                }
            }
        }
    
    def compose_email(self, user_context: Dict[str, Any], company_intel: Dict[str, Any], connections: list, tone: str) -> Dict[str, Any]:
        """Use Gemini to draft a personalized email."""
        if not GEMINI_API_KEY:
            return self._get_mock_draft()
        
        try:
            prompt = f"""You are a JSON-generating AI that writes compelling outreach emails.
            
            User's Profile:
            {json.dumps(user_context, indent=2)}

            Target Company's Profile:
            {json.dumps(company_intel, indent=2)}

            Key Connection Points:
            {json.dumps(connections, indent=2)}

            Desired Tone: {tone}

            Instructions:
            1. Return ONLY a valid JSON object.
            2. Write a concise and professional email from the user to someone at the target company.
            3. The email should be personalized based on the connection points.
            4. Create a compelling subject line and a clear call to action.
            5. Keep the exact same structure and keys as the example below.
            
            Return this exact JSON structure (with your composed email):
            {{
                "subject": "Catchy and relevant subject line",
                "body": "A well-written, personalized email body. Use paragraphs for readability.",
                "call_to_action": "e.g., 'Would you be open to a brief chat next week?'"
            }}"""
            
            response = model.generate_content(prompt)
            logger.info(f"Raw Gemini response for email composition: {response.text}")
            
            text = response.text.strip().replace('```json', '').replace('```', '').strip()
            ai_draft = json.loads(text)
            logger.info("Successfully parsed Gemini response for email composition")
            return ai_draft
            
        except Exception as e:
            logger.error(f"Error in AI analysis for email composition: {str(e)}")
            return self._get_mock_draft(error=str(e))
    
    def _get_mock_draft(self, error: str = None) -> Dict[str, Any]:
        draft = {
            "subject": "Mock Subject",
            "body": "This is a mock email body.",
            "call_to_action": "Let's connect."
        }
        if error:
            draft["ai_analysis_error"] = error
        return draft

    def process_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Main A2A task processing method."""
        try:
            user_context = task_data['input']['user_context']
            company_intel = task_data['input']['company_intelligence']
            connections = task_data['input']['connection_points']
            tone = task_data['input'].get('email_tone', 'formal')
            
            logger.info("Starting email composition")
            draft = self.compose_email(user_context, company_intel, connections, tone)
            
            result = {
                "task_id": task_data.get('task_id', f"email_comp_{datetime.now().timestamp()}"),
                "agent_info": self.agent_card,
                "status": "completed",
                "output": {
                    "draft_email": draft,
                    "composition_metadata": {"processed_at": datetime.now().isoformat(), "tone": tone}
                },
                "next_suggested_agents": ["quality_assurance_agent"]
            }
            
            logger.info("Successfully completed email composition")
            return result
            
        except Exception as e:
            logger.error(f"Error processing email composition task: {str(e)}")
            return {"status": "error", "error": str(e)}

agent = EmailCompositionAgent()

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "agent": "Email Composition Agent"})

@app.route('/agent-card', methods=['GET'])
def get_agent_card():
    return jsonify(agent.agent_card)

@app.route('/compose-email', methods=['POST'])
def compose_email_endpoint():
    """Main endpoint for email composition."""
    try:
        task_data = request.get_json()
        if not task_data:
            return jsonify({"status": "error", "error": "No task data provided"}), 400
        
        result = agent.process_task(task_data)
        status_code = 200 if result.get('status') == 'completed' else 500
        return jsonify(result), status_code
        
    except Exception as e:
        logger.error(f"Error in compose-email endpoint: {str(e)}")
        return jsonify({"status": "error", "error": str(e)}), 500

if __name__ == '__main__':
    debug_mode = FLASK_ENV == 'development'
    logger.info(f"Starting Email Composition Agent v{AGENT_VERSION} on port {PORT}")
    app.run(host='0.0.0.0', port=PORT, debug=debug_mode)
