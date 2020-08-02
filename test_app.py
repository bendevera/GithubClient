import os

from app import GithubClient


def test_db() -> None:
    TEST_OWNER = "brendajin"
    TEST_REPO = "bendevera"
    GITHUB_TOKEN = str(os.getenv("GITHUB_TOKEN"))
    client = GithubClient(GITHUB_TOKEN, TEST_OWNER, TEST_REPO)
    pull_requests = client.list_pull_requests()
    assert len(pull_requests) == 1
