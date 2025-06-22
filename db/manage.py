from typing import List, Dict
import asyncpg
import os


class DBManager:
    def __init__(self):
        self.pool = None

    async def init_pool(self):
        connection_string = os.getenv('DB_URL')
        self.pool = await asyncpg.create_pool(connection_string)
        print("Connection pool created")

    async def check_connection(self):
        async with self.pool.acquire() as conn:
            time = await conn.fetchval('SELECT NOW();')
            version = await conn.fetchval('SELECT version();')
            print(' Current time:', time)
            print(' PostgreSQL version:', version)

    async def insert_commits(self, data: List[Dict]):
        query = """
        INSERT INTO commits (sha, author, date, message)
        VALUES ($1, $2, $3, $4)
        ON CONFLICT (sha) DO NOTHING;
        """
        async with self.pool.acquire() as conn:
            await conn.executemany(query, [
                (item['sha'], item['author'], item['date'], item['message']) for item in data
            ])

    async def insert_contributors(self, data: List[Dict]):
        # Example - adjust field names as needed
        query = """
        INSERT INTO contributors (login, contributions)
        VALUES ($1, $2)
        ON CONFLICT (login) DO NOTHING;
        """
        async with self.pool.acquire() as conn:
            await conn.executemany(query, [
                (item['login'], item['contributions'] ,item["id"], item["url"] , item["avatar_id"]) for item in data
            ])

    async def insert_repo_meta(self, data: Dict):
        query = """
        INSERT INTO repos (id, name, full_name, description)
        VALUES ($1, $2, $3, $4)
        ON CONFLICT (id) DO UPDATE SET description = EXCLUDED.description;
        """
        async with self.pool.acquire() as conn:
            await conn.execute(query, data['id'], data['name'], data['full_name'], data.get('description'))

    async def close(self):
        if self.pool:
            await self.pool.close()
            print("Connection pool closed")


    async  def get_repos(self):
        query = """
        SELECT id, name, full_name, stargazers_count, forks_count, created_at FROM repos
        """
        async with self.pool.acquire() as conn:
            result = await conn.execute(query)
            return result

