import json
import os
from typing import Dict, List, Tuple

import requests
from dotenv import load_dotenv

load_dotenv()


class GithubClient:
    """ GitHub client to get pull request data. """

    base_url = "https://api.github.com"

    def __init__(self, token: str, owner: str, repo: str):
        self.headers = self.__get_headers(token)
        self.owner = owner
        self.repo = repo

    def __get_headers(self, token: str) -> Dict:
        return {'Authorization': 'token %s' % token}

    def list_pull_requests(self, params: Dict = {"state": "open"}) -> List:
        url = "%s/repos/%s/%s/pulls" % (
            self.base_url, self.owner, self.repo)
        response = requests.get(url, headers=self.headers, params=params)
        return response.json()

    def get_pull_commits(self, number: int) -> List:
        url = "%s/repos/%s/%s/pulls/%s/commits" % (
            self.base_url, self.owner, self.repo, number)
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_pull_files(self, number: int) -> List:
        url = "%s/repos/%s/%s/pulls/%s/files" % (
            self.base_url, self.owner, self.repo, number)
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_pull_comments(self, number: int) -> List:
        url = "%s/repos/%s/%s/pulls/%s/comments" % (
            self.base_url, self.owner, self.repo, number)
        response = requests.get(url, headers=self.headers)
        return response.json()

    def create_pull(
            self,
            title: str,
            head: str,
            base: str,
            body: str = "",
            maintainer_can_modify: bool = True,
            draft: bool = False) -> Tuple[bool, Dict]:
        params = {
            "title": title,
            "head": self.owner + ":" + head,
            "base": base,
            "body": body,
            "maintainer_can_modify": maintainer_can_modify,
            "draft": draft
        }
        url = "%s/repos/%s/%s/pulls" % (
            self.base_url, self.owner, self.repo)
        response = requests.post(url, headers=self.headers, json=params)
        return response.status_code == 201, response.json()

    def update_pull(self, number: int, params: Dict) -> Tuple[bool, Dict]:
        url = "%s/repos/%s/%s/pulls/%s" % (
            self.base_url, self.owner, self.repo, number)
        response = requests.patch(url, headers=self.headers, json=params)
        return response.status_code == 200, response.json()

    def is_merged(self, number: int) -> bool:
        url = "%s/repos/%s/%s/pulls/%s/merge" % (
            self.base_url, self.owner, self.repo, number)
        response = requests.get(url, headers=self.headers)
        return response.status_code == 204

    def merge_pull(self, number: int, params: Dict = {}) -> Tuple[bool, str]:
        if params == {}:
            params = {"commit_title": "merging pull id %s" % (number)}
        url = "%s/repos/%s/%s/pulls/%s/merge" % (
            self.base_url, self.owner, self.repo, number)
        response = requests.put(url, headers=self.headers, params=params)
        return response.status_code == 200, response.json()["message"]


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
