"""
Learning AI Agent - A2A Compatible
Analyzes email campaign performance to provide optimization insights.
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
PORT = int(os.getenv('PORT', 8086))

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('models/gemini-1.5-flash')

class LearningAiAgent:
    """A2A agent for analyzing campaign performance."""
    
    def __init__(self):
        self.agent_card = {
            "name": "Learning AI Agent",
            "description": "Analyzes email interaction data to find patterns and suggest optimizations.",
            "capabilities": ["performance_analysis", "pattern_recognition", "success_prediction"],
            "input_schema": {
                "type": "object",
                "properties": {"interaction_data": {"type": "array"}},
                "required": ["interaction_data"]
            },
            "output_schema": {"type": "object"}
        }
    
    def analyze_performance(self, interaction_data: list) -> Dict[str, Any]:
        """Use Gemini to analyze email performance data."""
        if not GEMINI_API_KEY:
            return {"insights": ["Enable Gemini API for analysis."]}
        
        try:
            prompt = f"""You are a JSON-generating AI that analyzes email campaign data.
            
            Data:
            {json.dumps(interaction_data, indent=2)}

            Instructions:
            1. Return ONLY a valid JSON object.
            2. Identify patterns in successful emails (high open/reply rates).
            3. Provide actionable suggestions for improving future campaigns.
            
            Return this exact JSON structure:
            {{
                "key_findings": [
                    "Emails with personalized subject lines have a 20% higher open rate."
                ],
                "optimization_suggestions": [
                    "Focus on mentioning shared interests in the first paragraph."
                ]
            }}"""
            
            response = model.generate_content(prompt)
            return json.loads(response.text.strip().replace('```json', '').replace('```', '').strip())
            
        except Exception as e:
            return {"error": str(e)}

    def process_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Main A2A task processing method."""
        try:
            interactions = task_data['input']['interaction_data']
            analysis = self.analyze_performance(interactions)
            return {"status": "completed", "output": analysis}
        except Exception as e:
            return {"status": "error", "error": str(e)}

agent = LearningAiAgent()

@app.route('/analyze-performance', methods=['POST'])
def analyze_performance_endpoint():
    result = agent.process_task(request.get_json())
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
