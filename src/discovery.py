import random
import traceback

from filters import getSocials, hasRecentActivity, isValidRepo
from github_client import GitHubClient
from search_strategy import buildSearchQueries

class DeveloperDiscovery:
    def __init__(self):
        self.github = GitHubClient()

    async def find(self, seenUsernames:set[str], limit:int=10)->list[dict]:
        candidates = {}

        queries = buildSearchQueries()

        for query in queries:
            pages = [1, 2, 3, 4, 5]
            random.shuffle(pages)

            for page in pages[:2]:
                repos = await self.github.searchRepo(
                    query=query,
                    page=page,
                )

                random.shuffle(repos)

                for repo in repos:
                    if not isValidRepo(repo):
                        continue

                    username = repo["owner"]["login"].lower()

                    if username in seenUsernames:
                        continue
                    
                    existing = candidates.get(username)

                    if (
                        existing is None
                        or repo["stargazers_count"]
                        >existing["stargazers_count"]
                    ):
                        candidates[username] = repo
            
            if len(candidates) >= 60:
                break

        candidateItems = list(candidates.items())
        random.shuffle(candidateItems)

        results = []

        for username, repo in candidateItems:
            if len(results) >= limit:
                break

            username = repo["owner"]["login"]

            try:
                user = await self.github.getUser(username)

                if user.get("type") != "User":
                    continue

                socials = getSocials(user)
                if not socials:
                    continue

                events = await self.github.getUserEvents(username)
                if not hasRecentActivity(events):
                    continue

                results.append(
                    {
                        "name": user.get("name") or username,
                        "username": username,
                        "stars": repo["stargazers_count"],
                        "repoName": repo["name"],
                        "repoUrl": repo["html_url"],
                        "githubUrl": user["html_url"],
                        "social": socials,
                    }
                )

            except Exception:
                traceback.print_exc()
                continue
        
        return results

    async def close(self):
        await self.github.close()