import os

from dotenv import load_dotenv
from etl.etl_pipeline import GithubETL, GithubAPI
load_dotenv()

if __name__ == "__main__":

    etl = GithubETL(token=os.getenv('GITHUB_TOKEN'))

    etl.run_for_user("saphalpantha")
    etl.run_for_repo(owner="saphalpantha", repo="saphalpantha")
    print("END")

