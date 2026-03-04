from discord.ext import commands
import sqlite3
import json


# F:\amadeus_memories\memories.db
# I was going to use PostgreSQL- But this was simpler (I'll later migrate it)

class MemoryCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conn = sqlite3.connect(r'F:\amadeus_memories\memories.db')
        self.cursor = self.conn.cursor()
        self._setup_db()

    def _setup_db(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user TEXT,
                channel_id INTEGER,
                text TEXT,
                embedding TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()

    '''
    async def add_memory(self, user: str, text: str, channel_id: int, embedding=None):
        if embedding is None:
            embedding = [0.0] * 10  # jut placeholder embedding

        self.cursor.execute(
            "INSERT INTO memories (user, channel_id, text, embedding) VALUES (?, ?, ?, ?)",
            (
                user,
                channel_id,
                text,
                json.dumps(embedding)
            )
        )

        self.conn.commit()
    '''

    async def recall_memories(self, limit: int = 5):
        self.cursor.execute(
            "SELECT user, channel_id, text, timestamp FROM memories ORDER BY id DESC LIMIT ?",
            (limit,)
        )

        return self.cursor.fetchall()

    # Imma add the commands below, to keep this file 'organised'

    async def saveMemories(
                           self,
                           user: str,
                           channel_id: int,
                           question: str,
                           answer: str,
                           embbeding=None
                           ):

        if embbeding is None:
            embbeding = [0.0] * 10

        text_to_store = f"Q: {question}\nA: {answer}"

        self.cursor.execute(
            "INSERT INTO memories (user, channel_id, text, embedding) VALUES (?, ?, ?, ?)",
            (
                user,
                channel_id,
                text_to_store, json.dumps(embbeding)
            )
        )
        self.conn.commit()


def setup(bot):
    memSec = MemoryCog(bot)
    bot.add_cog(memSec)
