from etl.github_api import GithubAPI
from etl.transform import Transformer
import json

from pathlib import Path


class GithubETL:
    def __init__(self, token):
        self.api = GithubAPI(token)
        self.transformer = Transformer()

    def run_for_user(self, username:str, output:str):
        raw_repos = self.api.get_repos(username)
        transformed_repos = self.transformer.transform_repos(raw_repos)

        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w") as f:
            json.dump(transformed_repos, f,indent=2)

        print(f"[✓] Saved {len(transformed_repos)} repos to {output_path}")




