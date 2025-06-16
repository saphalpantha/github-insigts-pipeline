import os
from dotenv import load_dotenv
import requests
from etl.github_api import GithubAPI
class Extractor:
    def __init__(self):
        self.client = GithubAPI()


    def fetch_commits(self, owner :str, repo:str, branch:str="main"):
        return self.client.get_commits(owner, repo,branch)

    def fetch_repos(self,owner:str):
        return self.client.get_repos(owner)

    def fetch_contributors(self, owner:str, repo:str ,per_page: int=10 ):
        return self.fetch_contributors(owner, repo, per_page)

    def fetch_repo_meta(self, owner:str, entity:str="users"):
        return self.fetch_repo_meta(owner, entity)
