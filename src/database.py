import sqlite3
from pathlib import Path 

dbPath = Path("data/bot.db")

class Database:
    def __init__(self, dbPath:Path=dbPath) -> None:
        self.dbPath = dbPath

        self.dbPath.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._create_tables()

    def _connect(self):
        return sqlite3.connect(self.dbPath)

    def _create_tables(self):
        with self._connect() as conn:
            conn.execute(
                '''
                CREATE TABLE IF NOT EXISTS seenDevelopers(
                    telegramUserId INTEGER NOT NULL,
                    githubUsername TEXT NOT NULL,
                    shownAt DATETIME DEFAULT CURRENT_TIMESTAMP,

                    PRIMARY KEY(
                            telegramUserId,
                            githubUsername
                        )
                    )
                '''
            )
            conn.commit()

    def getSeenUsernames(self, telegramUserId:int)->set[str]:
        with self._connect() as conn:
            cursor = conn.execute(
                """
                SELECT githubUsername
                FROM seenDevelopers
                WHERE telegramUserId = ?
                """,
                (telegramUserId,),
            )

            return {row[0].lower() for row in cursor.fetchall()}

    def markSeen(self, telegramUserId:int, usernames:list[str]):
        with self._connect() as conn:
            conn.executemany(
                """
                INSERT OR IGNORE INTO seenDevelopers(
                    telegramUserId,
                    githubUsername
                )
                """,
                [
                    (
                        telegramUserId,
                        username.lower
                    )
                    for username in usernames
                ]
            )

            conn.commit()

    def resetUser(self, telegramUserId:int,):
        with self._connect() as conn:
            conn.execute(
                """
                DELETE FROM seenDevelopers
                WHERE telegramUserId = ?
                """,
                (telegramUserId,),
            )

            conn.commit() 

    def countSeen(self, telegramUserId:int):
        with self._connect() as conn:
            cursor = conn.execute(
                """
                SELECT COUNT(*)
                FROM seenDevelopers
                WHERE telegramUserId = ?
                """,
                (telegramUserId,),
            )

            return cursor.fetchone()[0]

