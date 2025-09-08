# Connection Mapping Agent

The Connection Mapping Agent is an A2A-compatible AI agent that specializes in finding the "common ground" between two professional profiles. It takes a user's context and a target's profile analysis as input and identifies shared experiences, interests, and other potential conversation starters.

## Capabilities

- **Common Interest Detection**: Finds shared interests, hobbies, or skills.
- **Shared Experience Mapping**: Identifies common employers, schools, or volunteer organizations.
- **Relationship Analysis**: Suggests the most promising angles for building rapport.

## A2A (Agent-to-Agent) API

### Endpoint: `/map-connections`

Analyzes two profiles and returns a list of connection points.

- **Method**: `POST`
- **Body**:
  ```json
  {
    "task_id": "map-connections-123",
    "input": {
      "user_context": {
        "summary": "User's professional summary...",
        "key_skills": ["Python", "Data Analysis"]
      },
      "target_profile_analysis": {
        "interests": ["Data Analysis", "Machine Learning"],
        "experience": [{
            "company": "Tech Company"
        }]
      }
    }
  }
  ```

- **Success Response (200 OK)**:
  ```json
  {
    "task_id": "map-connections-123",
    "status": "completed",
    "output": {
      "connection_points": [
        {
          "type": "Shared Interest",
          "details": "Both profiles mention an interest in Data Analysis."
        }
      ]
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
    The agent will start on port 8083.
