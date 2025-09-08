"""
Connection Mapping Agent - A2A Compatible
Finds connections between a user's context and a target's profile.
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
PORT = int(os.getenv('PORT', 8083))
AGENT_VERSION = os.getenv('AGENT_VERSION', '1.0.0')

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('models/gemini-1.5-flash')
    logger.info("Gemini API configured for Connection Mapping Agent")
else:
    logger.warning("No Gemini API key found - Connection Mapping Agent will use mock data")

class ConnectionMappingAgent:
    """A2A agent to find common ground between two profiles."""
    
    def __init__(self):
        self.agent_card = {
            "name": "Connection Mapping Agent",
            "description": "Analyzes a user's context and a target's profile to find shared experiences, interests, and connections.",
            "version": AGENT_VERSION,
            "capabilities": ["common_interest_detection", "shared_experience_mapping", "relationship_analysis"],
            "input_schema": {
                "type": "object",
                "properties": {
                    "user_context": {"type": "object", "description": "Structured data about the user."},
                    "target_profile_analysis": {"type": "object", "description": "Structured data about the target."}
                },
                "required": ["user_context", "target_profile_analysis"]
            },
            "output_schema": {
                "type": "object",
                "properties": {
                    "connection_points": {"type": "array"},
                    "mapping_metadata": {"type": "object"}
                }
            }
        }
    
    def map_connections(self, user_context: Dict[str, Any], target_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Use Gemini to find connections between two profiles."""
        if not GEMINI_API_KEY:
            return self._get_mock_analysis()
        
        try:
            prompt = f"""You are a JSON-generating AI that acts as a networking assistant.
            
            User's Profile:
            {json.dumps(user_context, indent=2)}

            Target's Profile:
            {json.dumps(target_profile, indent=2)}

            Instructions:
            1. Return ONLY a valid JSON object.
            2. Analyze both profiles to find meaningful points of connection.
            3. These connections should be useful for starting a conversation.
            4. Focus on shared interests, experiences, education, or skills.
            5. Keep the exact same structure and keys as the example below.
            
            Return this exact JSON structure (with your analysis):
            {{
                "connection_points": [
                    {{
                        "type": "Shared Interest",
                        "details": "Both the user and the target are interested in AI technology."
                    }},
                    {{
                        "type": "Shared Experience",
                        "details": "Both have experience in backend development."
                    }},
                    {{
                        "type": "Shared Education",
                        "details": "Both attended universities in California."
                    }}
                ]
            }}"""
            
            response = model.generate_content(prompt)
            logger.info(f"Raw Gemini response for connection mapping: {response.text}")
            
            text = response.text.strip().replace('```json', '').replace('```', '').strip()
            ai_analysis = json.loads(text)
            logger.info("Successfully parsed Gemini response for connection mapping")
            return ai_analysis
            
        except Exception as e:
            logger.error(f"Error in AI analysis for connection mapping: {str(e)}")
            return self._get_mock_analysis(error=str(e))
    
    def _get_mock_analysis(self, error: str = None) -> Dict[str, Any]:
        analysis = {
            "connection_points": [{
                "type": "Shared Interest",
                "details": "Both are interested in mock data."
            }]
        }
        if error:
            analysis["ai_analysis_error"] = error
        return analysis

    def process_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Main A2A task processing method."""
        try:
            user_context = task_data.get('input', {}).get('user_context')
            target_profile = task_data.get('input', {}).get('target_profile_analysis')
            if not user_context or not target_profile:
                raise ValueError("user_context and target_profile_analysis are required")
            
            logger.info("Starting connection mapping")
            connections = self.map_connections(user_context, target_profile)
            
            result = {
                "task_id": task_data.get('task_id', f"conn_map_{datetime.now().timestamp()}"),
                "agent_info": self.agent_card,
                "status": "completed",
                "output": {
                    "connection_points": connections.get("connection_points", []),
                    "mapping_metadata": {"processed_at": datetime.now().isoformat()}
                },
                "next_suggested_agents": ["email_composition_agent"]
            }
            
            logger.info("Successfully completed connection mapping")
            return result
            
        except Exception as e:
            logger.error(f"Error processing connection mapping task: {str(e)}")
            return {"status": "error", "error": str(e)}

agent = ConnectionMappingAgent()

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "agent": "Connection Mapping Agent"})

@app.route('/agent-card', methods=['GET'])
def get_agent_card():
    return jsonify(agent.agent_card)

@app.route('/map-connections', methods=['POST'])
def map_connections_endpoint():
    """Main endpoint for connection mapping."""
    try:
        task_data = request.get_json()
        if not task_data:
            return jsonify({"status": "error", "error": "No task data provided"}), 400
        
        result = agent.process_task(task_data)
        status_code = 200 if result.get('status') == 'completed' else 500
        return jsonify(result), status_code
        
    except Exception as e:
        logger.error(f"Error in map-connections endpoint: {str(e)}")
        return jsonify({"status": "error", "error": str(e)}), 500

if __name__ == '__main__':
    debug_mode = FLASK_ENV == 'development'
    logger.info(f"Starting Connection Mapping Agent v{AGENT_VERSION} on port {PORT}")
    app.run(host='0.0.0.0', port=PORT, debug=debug_mode)
