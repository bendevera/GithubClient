import json
import os
from typing import Dict, List

import requests
from dotenv import load_dotenv

load_dotenv()


class GithubClient:

    def __init__(self, token: str, owner: str, repo: str):
        self.headers = self.__get_headers(token)
        self.owner = owner
        self.repo = repo

    def __get_headers(self, token: str) -> Dict:
        return {'Authorization': 'token %s' % token}

    def list_pull_requests(self, params: Dict = {"state": "open"}) -> List:
        url = "https://api.github.com/repos/%s/%s/pulls" % (
            self.owner, self.repo)
        response = requests.get(url, headers=self.headers, params=params)
        return response.json()

    def get_pull_commits(self, number: int) -> List:
        url = "https://api.github.com/repos/%s/%s/pulls/%s/commits" % (
            self.owner, self.repo, number)
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_pull_files(self, number: int) -> List:
        url = "https://api.github.com/repos/%s/%s/pulls/%s/files" % (
            self.owner, self.repo, number)
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_pull_comments(self, number: int) -> List:
        url = "https://api.github.com/repos/%s/%s/pulls/%s/comments" % (
            self.owner, self.repo, number)
        response = requests.get(url, headers=self.headers)
        return response.json()


def main(token: str, owner: str, repo: str):
    client = GithubClient(token, owner, repo)
    pull_requests = client.list_pull_requests()
    data = []
    for pull in pull_requests:
        commits = client.get_pull_commits(pull["number"])
        files = client.get_pull_files(pull["number"])
        comments = client.get_pull_comments(pull["number"])
        data.append((pull["number"], commits, files, comments))
        print(json.dumps(comments, indent=2))


if __name__ == "__main__":
    TEST_OWNER = "brendajin"
    TEST_REPO = "bendevera"
    GITHUB_TOKEN = str(os.getenv("GITHUB_TOKEN"))
    main(GITHUB_TOKEN, TEST_OWNER, TEST_REPO)
