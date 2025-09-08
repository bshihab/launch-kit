# Company Research Agent

The Company Research Agent is an A2A-compatible AI agent that provides high-level intelligence on a given company. It's designed to quickly gather information on a company's recent news, culture, and industry trends to help with email personalization.

## Capabilities

- **Company News Summary**: Identifies and summarizes recent news and developments.
- **Culture Analysis**: Provides a brief overview of the company's work culture.
- **Industry Intelligence**: Highlights key trends affecting the company's industry.

## A2A (Agent-to-Agent) API

### Endpoint: `/research-company`

Researches a company and returns a structured intelligence report.

- **Method**: `POST`
- **Body**:
  ```json
  {
    "task_id": "company-research-123",
    "input": {
      "company_name": "ExampleCorp"
    }
  }
  ```

- **Success Response (200 OK)**:
  ```json
  {
    "task_id": "company-research-123",
    "status": "completed",
    "output": {
      "company_intelligence": {
        "company_overview": "A brief description of the company.",
        "recent_news": ["A recent news item."],
        "company_culture": "A summary of the company's culture.",
        "industry_trends": ["A relevant industry trend."]
      }
    }
  }
  ```

## Getting Started

1.  **Set up environment variables**:
    Create a `.env` file and add your `GEMINI_API_KEY`.

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the agent**:
    ```bash
    python main.py
    ```
    The agent will start on port 8082.
