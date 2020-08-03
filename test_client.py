import os

from client import GithubClient


def test_client() -> None:
    TEST_OWNER = "bendevera"
    TEST_REPO = "test-repo"
    GITHUB_TOKEN = str(os.getenv("GITHUB_TOKEN"))
    client = GithubClient(GITHUB_TOKEN, TEST_OWNER, TEST_REPO)
    pull_requests = client.list_pull_requests()
    assert len(pull_requests) == 0

    success, pull_request = client.create_pull(
        "Test Pull",
        "test-branch-1",
        "master")
    assert success

    is_merged = client.is_merged(pull_request["number"])
    assert not is_merged

    success, _ = client.merge_pull(pull_request["number"])
    assert success
