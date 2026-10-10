from html import escape

def formatDeveloper(developer:dict, number:int)->str:
    name = escape(developer["name"])

    username = escape(developer["username"])

    repoName = escape(developer["repoName"])

    stars = developer["stars"]

    repoUrl = developer["repoUrl"]

    githubUrl = developer["githubUrl"]

    lines = [
        f"<b>{number}. {name}</b>",
        "",
        f"👤 @{username}",
        "",
        f"⭐ <b>{stars:,}</b> stars",
        (
            f'📦 <a href="{repoUrl}">'
            f"{repoName}</a>"
        ),
        "",
    ]

    twitter = developer[
        "social"
    ].get("twitter")

    if twitter:
        lines.append(
            f'𝕏 <a href="{twitter}">'
            f"X / Twitter</a>"
        )
        lines.append("")
    
    lines.extend(
        [
            (
                f'🔗 <a href="{githubUrl}">'
                f"Github Profile</a>"
            ),
            "",
            "────────────"
        ]
    )

    return "\n".join(lines)

def formatDevelopers(developers: list[dict])->str:
    blocks = [
        formatDeveloper(developer, index)
        for index, developer in enumerate(
            developers,
            start=1
        )
    ]

    return "\n\n".join(blocks)