from typing import List, Dict, Any


class Transformer:
    def transform_commits(self, raw_commits: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [
            {
                "sha": commit.get("sha"),
                "author": commit.get("commit", {}).get("author", {}).get("name"),
                "date": commit.get("commit", {}).get("author", {}).get("date"),
                "message": commit.get("commit", {}).get("message"),
            }
            for commit in raw_commits
        ]

    def transform_repos(self, raw_repos: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [
            {
                "id": repo.get("id"),
                "name": repo.get("name"),
                "full_name": repo.get("full_name"),
                "description": repo.get("description"),
                "html_url": repo.get("html_url"),
                "language": repo.get("language"),
                "created_at": repo.get("created_at"),
                "updated_at": repo.get("updated_at"),
                "stargazers_count": repo.get("stargazers_count"),
                "forks_count": repo.get("forks_count"),
            }
            for repo in raw_repos
        ]

    def transform_repo_details(self, repo: Dict[str, Any]) -> Dict[str, Any]:

        return {
            "id": repo.get("id"),
            "name": repo.get("name"),
            "full_name": repo.get("full_name"),
            "description": repo.get("description"),
            "html_url": repo.get("html_url"),
            "language": repo.get("language"),
            "created_at": repo.get("created_at"),
            "updated_at": repo.get("updated_at"),
            "default_branch": repo.get("default_branch"),
            "open_issues_count": repo.get("open_issues_count"),
            "license": repo.get("license", {}).get("name") if repo.get("license") else None,
            "visibility": repo.get("visibility"),
        }

    def transform_contributors(self, raw_contributors):
        """
        Transforms raw contributor data into a structured format.
        """
        return [
            {
                "login": contributor.get("login"),
                "id": contributor.get("id"),
                "contributions": contributor.get("contributions"),
                "url": contributor.get("html_url"),
                "avatar_url": contributor.get("avatar_url")
            }
            for contributor in raw_contributors
        ]