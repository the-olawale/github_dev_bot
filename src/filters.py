from datetime import datetime, timedelta, timezone

ExcludedTerms = {
    "awesome",
    "awesome-list",
    "awesome-lists",
    "interview",
    "interview-prep",
    "roadmap",
    "tutorial",
    "tutorials",
    "course",
    "courses",
    "learning",
    "learn",
    "resources",
    "resource-list",
    "cheatsheet",
    "cheat-sheet",
    "dotfiles",
    "boilerplate",
    "starter-template",
    "starter-kit",
    "template",
    "dataset",
    "datasets",
}

def isValidRepo(repo: dict)->bool:
    if repo.get("fork"):
        return False
    
    if repo.get("archived"):
        return False
    
    if repo. get("is_templated"):
        return False

    if repo.get("stargazers_count", 0)<1000:
        return False
    
    owner = repo.get("owner", {})

    if owner.get("type") != "User":
        return False
    
    textParts = [
        repo.get("name", ""),
        repo.get("description", ""),
        " ".join(repo.get("topic", [])),
    ]

    haystack = " ".join(textParts).lower()

    for term in ExcludedTerms:
        if term in haystack:
            return False

    return True

def hasRecentActivity(events:list, day:int=30)->bool:
    cutoff = datetime.now(timezone.utc)-timedelta(days=day)

    meaningfulEvents = {
        "PushEvent",
        "PullRequestsEvent",
        "CreateEvent",
        "ReleaseEvent",
    }
    
    for event in events:
        if event.get("type") not in meaningfulEvents:
            continue
        
        createdAt = event.get("created_at")

        if not createdAt:
            continue
        
        eventTime = datetime.fromisoformat(
            createdAt.replace("Z", "+00:00")
        )

        if eventTime >= cutoff:
            return True

    return False

def getSocials(user: dict)->dict:
    socials={}

    twitter = user.get("twitter_username")

    if twitter:
        socials["twitter"] = f"https://x.com/{twitter}"

    return socials