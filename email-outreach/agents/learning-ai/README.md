# Learning AI Agent

The Learning AI Agent is an A2A-compatible AI agent that analyzes the performance of email campaigns to provide optimization insights.

## Capabilities

- **Performance Analysis**: Identifies trends in open rates, reply rates, etc.
- **Pattern Recognition**: Finds common threads in successful (and unsuccessful) emails.
- **Success Prediction**: Helps predict the potential success of future campaigns.

## A2A (Agent-to-Agent) API

### Endpoint: `/analyze-performance`

- **Method**: `POST`
- **Body**:
  ```json
  {
    "task_id": "analyze-perf-123",
    "input": {
      "interaction_data": [
        { "email_id": 1, "opened": true, "replied": false },
        { "email_id": 2, "opened": true, "replied": true }
      ]
    }
  }
  ```

## Getting Started

- The agent runs on port 8086.
