
import asyncpg
import asyncio
import os
import streamlit as st
from db.manage import DBManager


st.set_page_config(page_title="GitHub Insights Dashboard", layout="wide")
DATABASE_URL = os.getenv("DB_URL")

async def get_repos():
    conn = DBManager()
    await conn.init_pool();
    res = await conn.check_connection()
    await conn.close()


def run_dashboard():
    st.title("GitHub Insights Dashboard")

    # Fetch data
    repos = asyncio.run(get_repos())

    if not repos:
        st.warning("No repositories found.")
        return


    repo_names = [repo['full_name'] for repo in repos]
    selected_repo = st.selectbox("Select Repository", repo_names)

    # Show repo info
    selected_data = next((r for r in repos if r['full_name'] == selected_repo), None)

    if selected_data:
        st.subheader(f"Repository: {selected_data['full_name']}")
        st.write({
            "Stars": selected_data["stargazers_count"],
            "Forks": selected_data["forks_count"],
            "Created at": selected_data["created_at"].strftime("%Y-%m-%d")
        })

if __name__ == "__main__":
    run_dashboard()