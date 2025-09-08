# Quality Assurance Agent

The Quality Assurance Agent is an A2A-compatible AI agent that acts as an automated editor for the Email Composition Agent. It reviews drafts for quality, personalization, and potential issues.

## Capabilities

- **Content Review**: Checks for clarity, grammar, and tone.
- **Personalization Check**: Ensures the email effectively uses the identified connection points.
- **Spam Score Analysis**: Flags potential spam triggers.

## A2A (Agent-to-Agent) API

### Endpoint: `/review-email`

- **Method**: `POST`
- **Body**:
  ```json
  {
    "task_id": "review-email-123",
    "input": {
      "draft_email": {
        "subject": "...",
        "body": "..."
      }
    }
  }
  ```

## Getting Started

- The agent runs on port 8085.
