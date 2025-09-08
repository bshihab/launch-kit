"""
Company Research Agent - A2A Compatible
Gathers and analyzes information about a company for personalization.
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
PORT = int(os.getenv('PORT', 8082)) # Different port
AGENT_VERSION = os.getenv('AGENT_VERSION', '1.0.0')

# Configure Gemini
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('models/gemini-1.5-flash')
    logger.info("Gemini API configured successfully for Company Research Agent")
else:
    logger.warning("No Gemini API key found - Company Research Agent will use mock data")

class CompanyResearchAgent:
    """A2A-compatible agent for company intelligence"""
    
    def __init__(self):
        self.agent_card = {
            "name": "Company Research Agent",
            "description": "Gathers intelligence on a company, including recent news, culture, and industry trends.",
            "version": AGENT_VERSION,
            "capabilities": [
                "company_news_summary",
                "culture_analysis",
                "industry_intelligence"
            ],
            "input_schema": {
                "type": "object",
                "properties": {
                    "company_name": {"type": "string", "description": "The name of the company to research"}
                },
                "required": ["company_name"]
            },
            "output_schema": {
                "type": "object",
                "properties": {
                    "company_intelligence": {"type": "object"},
                    "research_metadata": {"type": "object"}
                }
            }
        }
    
    def research_company(self, company_name: str) -> Dict[str, Any]:
        """Use Gemini to research and analyze a company."""
        
        if not GEMINI_API_KEY:
            return self._get_mock_analysis()
        
        try:
            # In a real scenario, this would also involve web scraping or news API calls.
            # For this version, we rely on the LLM's knowledge and simulated search.
            prompt = f"""You are a JSON-generating AI that acts as a business analyst.
            
            Company to research: {company_name}

            Instructions:
            1. Return ONLY a valid JSON object.
            2. Provide a brief analysis of the company's recent activities, culture, and industry positioning.
            3. Your information should be concise and useful for someone preparing for an interview or outreach.
            4. Keep the exact same structure and keys as the example below.
            
            Return this exact JSON structure (with your analysis):
            {{
                "company_overview": "A brief, one-sentence description of the company.",
                "recent_news": [
                    "A recent news item or development.",
                    "Another recent event or announcement."
                ],
                "company_culture": "A summary of the company's culture (e.g., fast-paced, collaborative, innovative).",
                "industry_trends": [
                    "A relevant trend in the company's industry.",
                    "Another key trend affecting the company."
                ]
            }}"""
            
            response = model.generate_content(prompt)
            logger.info(f"Raw Gemini response for company research: {response.text}")
            
            text = response.text.strip().replace('```json', '').replace('```', '').strip()
            ai_analysis = json.loads(text)
            logger.info("Successfully parsed Gemini response for company research as JSON")
            return ai_analysis
            
        except Exception as e:
            logger.error(f"Error in AI analysis for company research: {str(e)}")
            return self._get_mock_analysis(error=str(e))
    
    def _get_mock_analysis(self, error: str = None) -> Dict[str, Any]:
        """Return mock analysis data for a company."""
        analysis = {
            "company_overview": "A leading technology company specializing in AI.",
            "recent_news": ["Launched a new AI-powered analytics platform.", "Announced record quarterly earnings."],
            "company_culture": "Known for its innovative and fast-paced work environment.",
            "industry_trends": ["Growing adoption of AI in business.", "Increased focus on data privacy."]
        }
        if error:
            analysis["ai_analysis_error"] = error
        return analysis

    def process_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Main A2A task processing method."""
        try:
            company_name = task_data.get('input', {}).get('company_name')
            if not company_name:
                raise ValueError("company_name is required")
            
            logger.info(f"Starting company research for: {company_name}")
            company_intelligence = self.research_company(company_name)
            
            result = {
                "task_id": task_data.get('task_id', f"company_research_{datetime.now().timestamp()}"),
                "agent_info": self.agent_card,
                "status": "completed",
                "output": {
                    "company_intelligence": company_intelligence,
                    "research_metadata": {
                        "processed_at": datetime.now().isoformat(),
                        "data_sources": ["simulated_llm_knowledge"]
                    }
                },
                "next_suggested_agents": ["connection_mapping_agent", "email_composition_agent"]
            }
            
            logger.info(f"Successfully completed company research for: {company_name}")
            return result
            
        except Exception as e:
            logger.error(f"Error processing company research task: {str(e)}")
            return {"status": "error", "error": str(e)}

# Initialize agent
agent = CompanyResearchAgent()

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "agent": "Company Research Agent"})

@app.route('/agent-card', methods=['GET'])
def get_agent_card():
    return jsonify(agent.agent_card)

@app.route('/research-company', methods=['POST'])
def research_company_endpoint():
    """Main endpoint for company research."""
    try:
        task_data = request.get_json()
        if not task_data:
            return jsonify({"status": "error", "error": "No task data provided"}), 400
        
        result = agent.process_task(task_data)
        status_code = 200 if result.get('status') == 'completed' else 500
        return jsonify(result), status_code
        
    except Exception as e:
        logger.error(f"Error in research-company endpoint: {str(e)}")
        return jsonify({"status": "error", "error": str(e)}), 500

if __name__ == '__main__':
    debug_mode = FLASK_ENV == 'development'
    logger.info(f"Starting Company Research Agent v{AGENT_VERSION} on port {PORT}")
    app.run(host='0.0.0.0', port=PORT, debug=debug_mode)
