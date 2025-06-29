# Profile Analysis Agent 🔍

A2A-compatible AI agent that analyzes LinkedIn profiles and extracts structured data for email personalization.

## Features

- **LinkedIn Profile Extraction**: Extracts key profile information
- **AI-Powered Analysis**: Uses GPT-4 to analyze personality traits and interests
- **A2A Protocol Compatible**: Follows Google's Agent-to-Agent communication standard
- **Personalization Insights**: Generates actionable insights for email outreach
- **Cloud-Ready**: Containerized and ready for Google Cloud Run deployment

## API Endpoints

### Health Check
```bash
GET /health
```
Returns agent health status and basic information.

### Agent Discovery
```bash
GET /agent-card
```
Returns A2A agent card with capabilities and schemas.

### Profile Analysis
```bash
POST /analyze
Content-Type: application/json

{
  "task_id": "unique_task_id",
  "input": {
    "linkedin_url": "https://linkedin.com/in/profile",
    "analysis_depth": "basic"
  }
}
```

### Test Endpoint
```bash
GET /test
```
Returns sample analysis for testing purposes.

## Response Format

```json
{
  "task_id": "profile_analysis_123",
  "agent_info": {
    "name": "Profile Analysis Agent",
    "version": "1.0.0"
  },
  "status": "completed",
  "output": {
    "profile_data": {
      "url": "https://linkedin.com/in/profile",
      "profile": {
        "name": "John Doe",
        "headline": "Software Engineer at Tech Corp",
        "skills": ["Python", "AI", "Cloud"],
        "experience": [...],
        "education": [...]
      }
    },
    "ai_analysis": {
      "personality_traits": ["analytical", "innovative"],
      "communication_style": "professional",
      "interests": ["technology", "startups"],
      "networking_potential": "high",
      "personalization_hooks": ["shared_university", "similar_role"]
    }
  }
}
```

## Local Development

### Prerequisites
- Python 3.11+ (or Conda)
- OpenAI API key (optional, will use mock data without it)

### Setup with Conda (Recommended)
```bash
# Create conda environment
conda env create -f environment.yml

# Activate environment
conda activate profile-analysis-agent

# Create environment file
cat > .env << 'EOF'
# OpenAI API Configuration
# Get your API key from: https://platform.openai.com/api-keys
OPENAI_API_KEY=your_openai_api_key_here

# LinkedIn API Configuration (for future production use)
LINKEDIN_CLIENT_ID=your_linkedin_client_id
LINKEDIN_CLIENT_SECRET=your_linkedin_client_secret

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
PORT=8080

# Logging Configuration
LOG_LEVEL=INFO

# Agent Configuration
AGENT_VERSION=1.0.0
ANALYSIS_DEPTH=basic

# Rate Limiting (for production)
MAX_REQUESTS_PER_MINUTE=60
MAX_PROFILES_PER_HOUR=100

# Cache Configuration (for future Redis integration)
CACHE_TTL_HOURS=24
ENABLE_CACHING=False
EOF

# Add your actual OpenAI API key
# Replace 'your_openai_api_key_here' with your actual key
nano .env

# Run the agent
python main.py
```

### Alternative Setup with pip
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (same as above)
# Run the agent
python main.py
```

The agent will be available at `http://localhost:8080`

### Testing

```bash
# Health check
curl http://localhost:8080/health

# Test analysis
curl http://localhost:8080/test

# Custom analysis
curl -X POST http://localhost:8080/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "task_id": "test_123",
    "input": {
      "linkedin_url": "https://linkedin.com/in/sample",
      "analysis_depth": "basic"
    }
  }'
```

## Deployment

### Google Cloud Run
```bash
# Build and deploy
gcloud run deploy profile-analysis-agent \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars OPENAI_API_KEY=your_key
```

### Docker
```bash
# Build image
docker build -t profile-analysis-agent .

# Run container
docker run -p 8080:8080 \
  -e OPENAI_API_KEY=your_key \
  profile-analysis-agent
```

## Configuration

### Environment Variables
- `OPENAI_API_KEY`: OpenAI API key for AI analysis
- `LINKEDIN_CLIENT_ID`: LinkedIn API client ID (future)
- `LINKEDIN_CLIENT_SECRET`: LinkedIn API secret (future)
- `PORT`: Server port (default: 8080)
- `LOG_LEVEL`: Logging level (default: INFO)

## A2A Integration

This agent follows the Google A2A protocol and can be easily integrated with:
- n8n workflows
- Other A2A agents
- Custom orchestration systems

### Agent Card
The agent exposes its capabilities via the `/agent-card` endpoint, allowing for automatic discovery and integration.

### Next Agents
After processing, this agent suggests calling:
- `company_research_agent`: To research the person's company
- `connection_mapping_agent`: To find commonalities with the user

## Production Notes

- **LinkedIn Scraping**: Currently uses simulated data. In production, integrate with LinkedIn API or specialized scraping services
- **Rate Limiting**: Implement rate limiting for production use
- **Caching**: Add Redis caching for frequently analyzed profiles
- **Monitoring**: Add application monitoring and alerting
- **Security**: Implement authentication and input validation

## License

MIT License - see LICENSE file for details. 