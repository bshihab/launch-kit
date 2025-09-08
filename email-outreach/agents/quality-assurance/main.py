"""
Quality Assurance Agent - A2A Compatible
Reviews and scores draft emails for quality and personalization.
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
PORT = int(os.getenv('PORT', 8085))
AGENT_VERSION = os.getenv('AGENT_VERSION', '1.0.0')

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('models/gemini-1.5-flash')
    logger.info("Gemini API configured for Quality Assurance Agent")
else:
    logger.warning("No Gemini API key found - Quality Assurance Agent will use mock data")

class QualityAssuranceAgent:
    """A2A agent for reviewing email drafts."""
    
    def __init__(self):
        self.agent_card = {
            "name": "Quality Assurance Agent",
            "description": "Reviews draft emails for personalization, tone, clarity, and potential spam triggers.",
            "version": AGENT_VERSION,
            "capabilities": ["content_review", "personalization_check", "spam_score_analysis"],
            "input_schema": {
                "type": "object",
                "properties": {"draft_email": {"type": "object"}},
                "required": ["draft_email"]
            },
            "output_schema": {
                "type": "object",
                "properties": {
                    "quality_score": {"type": "number"},
                    "suggestions": {"type": "array"},
                    "review_metadata": {"type": "object"}
                }
            }
        }
    
    def review_email(self, draft_email: Dict[str, Any]) -> Dict[str, Any]:
        """Use Gemini to review an email draft."""
        if not GEMINI_API_KEY:
            return self._get_mock_review()
        
        try:
            prompt = f"""You are a JSON-generating AI that acts as an expert email editor.
            
            Email Draft to Review:
            {json.dumps(draft_email, indent=2)}

            Instructions:
            1. Return ONLY a valid JSON object.
            2. Rate the email on a scale of 1-100 for overall quality.
            3. Provide specific, actionable suggestions for improvement.
            4. Check for personalization, clarity, and tone.
            5. Keep the exact same structure and keys as the example below.
            
            Return this exact JSON structure (with your review):
            {{
                "quality_score": 85,
                "suggestions": [
                    "Make the subject line more concise.",
                    "Strengthen the call to action by proposing a specific time."
                ],
                "spam_trigger_warning": false
            }}"""
            
            response = model.generate_content(prompt)
            text = response.text.strip().replace('```json', '').replace('```', '').strip()
            return json.loads(text)
            
        except Exception as e:
            logger.error(f"Error in AI analysis for QA: {str(e)}")
            return self._get_mock_review(error=str(e))
    
    def _get_mock_review(self, error: str = None) -> Dict[str, Any]:
        review = {"quality_score": 75, "suggestions": ["This is a mock suggestion."], "spam_trigger_warning": False}
        if error:
            review["ai_analysis_error"] = error
        return review

    def process_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Main A2A task processing method."""
        try:
            draft_email = task_data['input']['draft_email']
            review = self.review_email(draft_email)
            
            result = {
                "task_id": task_data.get('task_id', f"qa_{datetime.now().timestamp()}"),
                "status": "completed",
                "output": {**review, "review_metadata": {"processed_at": datetime.now().isoformat()}}
            }
            return result
            
        except Exception as e:
            return {"status": "error", "error": str(e)}

agent = QualityAssuranceAgent()

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "agent": "Quality Assurance Agent"})

@app.route('/agent-card', methods=['GET'])
def get_agent_card():
    return jsonify(agent.agent_card)

@app.route('/review-email', methods=['POST'])
def review_email_endpoint():
    """Main endpoint for email review."""
    task_data = request.get_json()
    result = agent.process_task(task_data)
    status_code = 200 if result.get('status') == 'completed' else 500
    return jsonify(result), status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=(FLASK_ENV == 'development'))
