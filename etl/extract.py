import os
from dotenv import load_dotenv
import requests

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN_C");

HEADERS= {
    "Authorization" : f"token ${GITHUB_TOKEN}"
}


