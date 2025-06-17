import asyncio
import os
from dotenv import load_dotenv
import asyncpg
load_dotenv()

async def setup():
    pool = await asyncpg.create_pool(os.getenv("DB_URL"))
    async with pool.acquire() as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS commits (
                sha TEXT PRIMARY KEY,
                author TEXT,
                date TIMESTAMP,
                message TEXT
            );
        """)
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS contributors (
                login TEXT PRIMARY KEY,
                id INT,
                contributions INT,
                url TEXT,
                avatar_url TEXT
            );
        """)
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS repos (
                id BIGINT PRIMARY KEY,
                name TEXT,
                full_name TEXT,
                description TEXT,
                html_url TEXT,
                language TEXT,
                created_at TIMESTAMP,
                updated_at TIMESTAMP,
                stargazers_count INT,
                forks_count INT
            );
        """)
    await pool.close()

if __name__ == "__main__":
    asyncio.run(setup())
