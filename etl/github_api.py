import requests
import os
from typing import Any, Dict, Optional, List
import  logging

class GithubAPI:
    def __init__(self, token:str=None ):
        self.base_url = "https://api.github.com"
        self.token = token or os.getenv('GITHUB_TOKEN')
        self.headers = {
        }

        if not self.token:
            raise ConnectionRefusedError("Token Not Found !")

        self.headers["Authorization"] = f"Bearer {self.token}"


    def ping_valid(self) -> bool:
        """
        Checks whether API Connection is Working
        :return True if status 200
        """
        url = f"{self.base_url.strip()}/rate_limit"
        try:
            response = requests.get(url, headers=self.headers)
            print("Status Code:", response.status_code)
            response.raise_for_status()
            return True
        except requests.RequestException as e:
            print("Connection failed:", e)
            return False

    def get_repos(self, username: str) -> List[Dict[str, Any]]:
        """
        Fetches public repositories of a GitHub user.
        """
        url = f"{self.base_url}/users/{username}/repos"

        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()

        except requests.HTTPError as http_err:
            print(f"HTTP error occurred while fetching repos for '{username}': {http_err}")
            raise

        except requests.RequestException as req_err:
            print(f"Request error occurred: {req_err}")
            raise

    def get_repo_meta(self, owner:str, entity:str="users"):

        url = f"{self.base_url}/${entity}/${owner}/repos"
        try:
            response = requests.get(url, self.headers)
            # print(response)

        except requests.exceptions.HTTPError as http_err:
            logging.error(
                f"[HTTPError] Failed to fetch repos")


    def get_contributors(self, owner:str, repo:str ,per_page: int=10 ) -> Optional[Dict[str, Any]]:

        url = f"{self.base_url}/repos/{owner}/{repo}/contributors"
        params = {
            "per_page": per_page
        }

        response = requests.get(url, params=params, headers=self.headers)

        response.raise_for_status()
        return response.json()

    def get_commits(self, owner: str, repo: str, branch: str = "main") -> Optional[List[Dict[str, Any]]]:
        """
        Fetch all commits from a specific repository and branch.
        """
        url = f"{self.base_url}/repos/{owner}/{repo}/commits"
        params = {"sha": branch, "per_page": 100, "page": 1}
        commits = []

        try:
            while True:
                response = requests.get(url, headers=self.headers, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()
                if not data:
                    break

                commits.extend(data)

                if len(data) < 100:
                    break

                params["page"] += 1

            return commits

        except requests.exceptions.HTTPError as http_err:
            logging.error(f"[HTTPError] Could not fetch commits for '{owner}/{repo}': {http_err}")
        except requests.exceptions.ConnectionError as conn_err:
            logging.error(f"[ConnectionError] Network issue while fetching commits for '{owner}/{repo}': {conn_err}")
        except requests.exceptions.Timeout as timeout_err:
            logging.error(f"[Timeout] Request timed out for '{owner}/{repo}': {timeout_err}")
        except requests.exceptions.RequestException as req_err:
            logging.error(f"[RequestException] Unexpected error for '{owner}/{repo}': {req_err}")

        return None














