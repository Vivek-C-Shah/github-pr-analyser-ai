# GitHub PR Analyser AI

This project is a FastAPI application that analyzes GitHub pull requests using OpenAI's GPT-4 model. It provides insights into code style issues, bugs, performance improvements, and best practices.

## Live Demo

You can check out the live docs of live server demo at https://github-pr-analyser-ai-production.up.railway.app/docs. Hosted on Railway.

## Project Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Vivek-C-Shah/github-pr-analyser-ai.git
   cd github-pr-analyser-ai
   ```

2. **Set Up Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables**
   Create a `.env` file in the root directory and add the following:
   ```plaintext
   REDIS_URL=your_redis_url
   DATABASE_URL=your_database_url
   OPENAI_API_KEY=your_openai_api_key
   WEBHOOK_SECRET=your_webhook_secret
   ```

5. **Run the Application**
   ```bash
   uvicorn app.main:app --reload
   ```

6. **Start Celery Worker**
   ```bash
   celery -A celery_app worker --loglevel=info
   ```

## API Documentation

### Analyze Pull Request

- **Endpoint**: `/analyze-pr`
- **Method**: `POST`
- **cURL Request**:
  ```bash
  curl -X POST https://github-pr-analyser-ai-production.up.railway.app/analyze-pr \
  -H "Content-Type: application/json" \
  -d '{"repo_url": "https://github.com/yourrepo", "pr_number": 1, "github_token": "your_github_token"}'
  ```

### Get Task Status

- **Endpoint**: `/status/{task_id}`
- **Method**: `GET`
- **cURL Request**:
  ```bash
  curl -X GET https://github-pr-analyser-ai-production.up.railway.app/status/{task_id}
  ```

### Get Analysis Results

- **Endpoint**: `/results/{pr_number}`
- **Method**: `GET`
- **cURL Request**:
  ```bash
  curl -X GET "https://github-pr-analyser-ai-production.up.railway.app/results/{pr_number}?repo_url=https://github.com/yourrepo"
  ```

## Design Decisions

- **FastAPI**: Chosen for its speed and ease of use in building APIs.
- **Celery**: Used for background task processing to handle long-running analysis tasks asynchronously.
- **OpenAI GPT-4**: Provides advanced code analysis capabilities.
- **Rate Limiting**: Implemented using `slowapi` to prevent abuse of the API.

## Future Improvements

- **Enhanced Error Handling**: Improve error messages and handling for better user experience.
- **Scalability**: Implement horizontal scaling for handling more concurrent requests.
- **Additional Analysis Features**: Expand the analysis to include more metrics and insights.
- **User Authentication**: Add authentication to secure the API endpoints.

## Configure a Webhook in GitHub

1. Go to your repository settings → Webhooks → Add Webhook.
2. **Payload URL**: Set this to your FastAPI endpoint, e.g., `https://github-pr-analyser-ai-production.up.railway.app/webhook`.
3. **Content Type**: Select `application/json`.
4. **Secret**: Add a secret key for validation (e.g., `webhook_secret`).
5. **Events**: Choose "Pull Request" or other events as required.

## Environment Variables

Ensure the following environment variables are set in your `.env` file:

- `REDIS_URL`: URL for your Redis instance.
- `DATABASE_URL`: URL for your database.
- `OPENAI_API_KEY`: API key for OpenAI.
- `WEBHOOK_SECRET`: Secret key for validating GitHub webhooks.

## Running Tests

1. **Set Up Test Environment Variables**
   Create a `.env.test` file in the root directory and add the necessary test environment variables, including a GitHub Personal Access Token for testing.

   - `GH_PAT`: A GitHub Personal Access Token with the necessary permissions for testing.

2. **Run Tests with Pytest**
   Ensure your virtual environment is activated and run the tests using `pytest`:
   ```bash
   pytest tests/
   ```

   This will execute all test cases in the `tests` directory, ensuring your application functions as expected.