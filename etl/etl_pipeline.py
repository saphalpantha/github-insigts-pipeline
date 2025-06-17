from etl.github_api import GithubAPI
from etl.transform import Transformer
import json
from dotenv import load_dotenv
from pathlib import Path


class GithubETL:
    def __init__(self, token):
        self.api = GithubAPI(token)
        self.transformer = Transformer()

    def run_for_user(self, username:str):
        print(f"🔍 Running ETL for {username}")
        raw_repos = self.api.get_repos(username)
        transformed_repos = self.transformer.transform_repos(raw_repos)

        output_path = Path(f"data/{username}/repos.json")
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w") as f:
            json.dump(transformed_repos, f,indent=2)

        print(f"[✓] Saved {len(transformed_repos)} repos to {output_path}")

    def run_for_repo(self, owner: str, repo: str):
        print(f"🔍 Running ETL for {owner}/{repo}")

        # 1. Extract
        repo_details = self.api.get_repo_meta(owner, repo )
        contributors = self.api.get_contributors(owner, repo)
        commits = self.api.get_commits(owner, repo)

        # 2. Transform
        transformed_details = self.transformer.transform_repo_details(repo_details)
        transformed_contributors = self.transformer.transform_contributors(contributors)
        transformed_commits = self.transformer.transform_commits(commits)

        # 3. Load (Save to disk as JSON)
        base_path = Path(f"data/{owner}/{repo}")
        base_path.mkdir(parents=True, exist_ok=True)

        with open(base_path / "repo_details.json", "w") as f:
            json.dump(transformed_details, f, indent=2)

        with open(base_path / "contributors.json", "w") as f:
            json.dump(transformed_contributors, f, indent=2)

        with open(base_path / "commits.json", "w") as f:
            json.dump(transformed_commits, f, indent=2)

        print(f"[✓] ETL for {owner}/{repo} completed and saved to {base_path}")

