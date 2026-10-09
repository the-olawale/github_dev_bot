# GitHub Developer Discovery Bot

A Telegram bot for discovering active individual developers behind public GitHub tech projects with 1,000+ stars.

The bot focuses on finding real developers rather than organizations, filters out low-signal repositories, checks recent GitHub activity, surfaces public social links when available, and avoids repeatedly showing the same developer.

## Features

- Discover 10 developers with `/find`
- Only considers repositories with 1,000+ stars
- Only includes individually owned repositories
- Excludes organizations, forks, archived repositories, templates, awesome-lists, tutorials, datasets, boilerplates, interview-prep repositories, and other low-signal projects
- Requires the developer to have recent GitHub activity
- Requires at least one supported public social account
- Prevents duplicate developers from being shown to the same Telegram user
- Supports resetting discovery history with `/reset`
- Designed for small internal usage

## Commands

`/find`  
Discover 10 fresh developers matching the bot's criteria.

`/reset`  
Clear your previously shown developers so they can appear again.

`/profile <username>`  
Inspect a public GitHub profile. Planned for a future version.

## Developer Criteria

A developer is eligible when:

- Their repository has at least 1,000 stars
- The repository is owned directly by an individual GitHub account
- The developer has public GitHub activity within the last 30 days
- The developer has at least one supported public social account
- The developer has not already been shown to the requesting Telegram user

The qualifying repository itself does not need to have been updated recently. The activity requirement applies to the developer.

## Tech Scope

The bot is intended to discover developers working on areas such as:

- AI and machine learning
- Developer tools
- Cybersecurity
- DevOps and infrastructure
- Databases
- Web development
- Mobile development
- APIs
- Programming languages
- Blockchain
- Open-source software
- Frameworks and libraries

Repositories such as awesome-lists, learning resources, interview-prep collections, datasets, templates, boilerplates, dotfiles, and similar non-product repositories are excluded.

## Project Structure

```text
github_dev_bot/
│
├── data/
│
├── src/
│   ├── bot.py
│   ├── config.py
│   ├── database.py
│   ├── discovery.py
│   ├── filters.py
│   ├── formatter.py
│   ├── github_client.py
│   └── search_strategy.py
│
├── .gitignore
├── README.md
└── requirements.txt
```

## How It Works

The discovery process follows this general flow:

1. Search GitHub for repositories across multiple star ranges
2. Filter out repositories that do not match the project criteria
3. Confirm that the repository owner is an individual user
4. Fetch the developer's public GitHub profile
5. Check whether the developer has been active within the last 30 days
6. Check for supported public social accounts
7. Remove developers already shown to the requesting Telegram user
8. Continue until 10 valid developers are found
9. Store the returned GitHub usernames to prevent duplicates

## Setup

Clone the repository and create a virtual environment.

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```env
GITHUB_TOKEN=your_github_token
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
```

Run the bot:

```bash
python bot.py
```

## Configuration

Core settings include:

- Minimum stars: `1000`
- Activity window: `30 days`
- Developers returned per `/find`: `10`

These values can be changed in `config.py`.

## Storage

The bot uses SQLite to keep track of developers already shown to each Telegram user.

Each Telegram user has their own discovery history.

Running `/reset` removes that user's stored history.

## Planned Features

- `/profile <username>`
- Telegram social discovery
- Discord social discovery
- Better profile README parsing
- Personal website social extraction
- Improved tech-project classification
- Smarter discovery ranking
- Additional filtering controls
