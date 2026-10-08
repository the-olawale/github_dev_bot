import httpx

from config import gitHubToken

class GitHubClient:
    baseURL = "https://api.github.com"

    def __init__(self):
        self.client = httpx.AsyncClient(
            timeout=20,
            headers={
                "Authorization": f"Bearer{gitHubToken}",
                "Accept": "application/vnd.github+json",
                "User-Agent": "github-developer-discovery-bot"
            },
        )
    
    async def searchRepo(self, query:str, page:int=1, perPage:int=100, sort:str="stars", order:str="desc"):
        params = {
            "q": query,
            "sort": sort,
            "order": order,
            "page": page,
            "per_page": perPage,
        }
        response = await self.client.get(
            f"{self.baseURL}/search/repositories",
            params=params,
        )
        response.raise_for_status()
        return response.json()["items"]
    
    async def get_user(self, username:str):
        response = await self.client.get(
            f"{self.baseURL}/users/{username}",
        )
        response.raise_for_status()
        response.json()

    async def get_user_events(self, username:str):
        response = await self.client.get(
            f"{self.baseURL}/users/{username}/events/public",
            params={"per_page":100}
        )
        response.raise_for_status()
        response.json()

    async def close(self):
        await self.client.aclose()