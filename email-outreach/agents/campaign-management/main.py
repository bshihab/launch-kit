"""
Campaign Management Agent - A2A Compatible
Manages email sending schedules and tracks interactions.
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import logging
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=os.getenv('LOG_LEVEL', 'INFO'))
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

PORT = int(os.getenv('PORT', 8087))

class CampaignManagementAgent:
    """A2A agent for managing email campaigns."""
    
    def __init__(self):
        # In a real implementation, this would connect to a database.
        self.campaigns = {}

    def schedule_campaign(self, campaign_data: Dict[str, Any]) -> Dict[str, Any]:
        """Schedules an email campaign."""
        campaign_id = f"camp_{len(self.campaigns) + 1}"
        self.campaigns[campaign_id] = campaign_data
        logger.info(f"Scheduled campaign {campaign_id}")
        return {"status": "scheduled", "campaign_id": campaign_id}

    def get_campaign_status(self, campaign_id: str) -> Dict[str, Any]:
        """Gets the status of a campaign."""
        return self.campaigns.get(campaign_id, {"status": "not_found"})

agent = CampaignManagementAgent()

@app.route('/schedule-campaign', methods=['POST'])
def schedule_campaign_endpoint():
    result = agent.schedule_campaign(request.get_json())
    return jsonify(result)

@app.route('/campaign-status/<campaign_id>', methods=['GET'])
def campaign_status_endpoint(campaign_id):
    result = agent.get_campaign_status(campaign_id)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
