import requests
import os



class GithubAPI:
    def __init__(self, token:str=None):
        self.base_url = "https://api.github.com"
        self.token = token or os.getenv('GITHUB_TOKEN')
        self.headers = {
        }

        if not self.token:
            raise ConnectionRefusedError("Token Not Found !")

        self.headers["Authorization"] = f"Bearer {self.token}"


    def ping_valid(self) -> bool:
        """
        Checks whether API Connection is Working
        :return True if status 200
        """
        url = f"{self.base_url.strip()}/rate_limit"
        try:
            response = requests.get(url, headers=self.headers)
            print("Status Code:", response.status_code)
            response.raise_for_status()
            return True
        except requests.RequestException as e:
            print("Connection failed:", e)
            return False

















