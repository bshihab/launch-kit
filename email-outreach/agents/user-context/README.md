# User Context Agent

The User Context Agent is an A2A-compatible AI agent that analyzes a user's resume and LinkedIn profile to create a comprehensive professional context. This context can then be used by other agents, like the Email Composition Agent, to generate highly personalized outreach.

## Capabilities

- **Resume Parsing**: Extracts key information from resume text.
- **LinkedIn Analysis**: Considers the user's LinkedIn profile for a holistic view.
- **Goal Identification**: Infers professional goals and target industries.
- **Skill Mapping**: Identifies and lists the user's key skills.

## A2A (Agent-to-Agent) API

### Endpoint: `/analyze-user`

Analyzes the user's profile and returns a structured context.

- **Method**: `POST`
- **Body**:
  ```json
  {
    "task_id": "user-context-123",
    "input": {
      "user_linkedin_url": "https://www.linkedin.com/in/user-profile",
      "user_resume_text": "Text content of the user's resume..."
    }
  }
  ```

- **Success Response (200 OK)**:
  ```json
  {
    "task_id": "user-context-123",
    "status": "completed",
    "output": {
      "user_context": {
        "summary": "A brief professional summary...",
        "key_skills": ["Skill 1", "Skill 2"],
        "professional_goals": "Seeking a role in...",
        "target_industries": ["Industry 1"],
        "unique_selling_points": ["Point 1"]
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
    The agent will start on port 8081.
