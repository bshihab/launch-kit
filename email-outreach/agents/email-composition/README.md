# Email Composition Agent

The Email Composition Agent is an A2A-compatible AI agent that drafts personalized outreach emails. It synthesizes data from the User Context Agent, Company Research Agent, and Connection Mapping Agent to create compelling, context-aware messages.

## Capabilities

- **Email Drafting**: Generates a complete email, including subject, body, and call to action.
- **Subject Line Generation**: Creates engaging and relevant subject lines.
- **Tone Adaptation**: Can adapt the writing style to be formal, casual, or enthusiastic.

## A2A (Agent-to-Agent) API

### Endpoint: `/compose-email`

Generates a draft email based on the provided inputs.

- **Method**: `POST`
- **Body**:
  ```json
  {
    "task_id": "compose-email-123",
    "input": {
      "user_context": { "..." },
      "company_intelligence": { "..." },
      "connection_points": [ "..." ],
      "email_tone": "formal"
    }
  }
  ```

- **Success Response (200 OK)**:
  ```json
  {
    "task_id": "compose-email-123",
    "status": "completed",
    "output": {
      "draft_email": {
        "subject": "A compelling subject line",
        "body": "The personalized email body.",
        "call_to_action": "A clear call to action."
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
    The agent will start on port 8084.
