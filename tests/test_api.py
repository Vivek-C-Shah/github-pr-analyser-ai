import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env.test")

def test_analyze_pr(test_client):
    response = test_client.post(
        "/analyze-pr",
        json={
            "repo_url": "https://github.com/yourrepo",
            "pr_number": 1,
            "github_token": os.getenv("GH_PAT")
        }
    )
    assert response.status_code == 200
    assert "task_id" in response.json()

def test_get_status(test_client):
    # Assuming a task_id is known for testing
    task_id = "some_task_id"
    response = test_client.get(f"/status/{task_id}")
    assert response.status_code == 200
    assert "status" in response.json()

def test_get_results(test_client):
    response = test_client.get(
        "/results/1",
        params={"repo_url": "https://github.com/yourrepo"}
    )
    assert response.status_code in [200, 404]  # Depending on whether results exist