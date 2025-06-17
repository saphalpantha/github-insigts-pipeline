import os

from dotenv import load_dotenv
from etl.etl_pipeline import GithubETL, GithubAPI
from db.manage import  DBManager
load_dotenv()
import asyncio

async def main():

    etl = GithubETL(token=os.getenv('GITHUB_TOKEN'))

    # etl.run_for_user("saphalpantha")
    # etl.run_for_repo(owner="saphalpantha", repo="saphalpantha")
    db = DBManager()
    await  db.init_pool()
    res = await db.check_connection()


    print("END")



if(__name__ == "__main__"):

    asyncio.run(main())

