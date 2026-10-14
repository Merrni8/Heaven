import aiosqlite

DB_NAME = "heaven.db"

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                xp INTEGER DEFAULT 0,
                level INTEGER DEFAULT 1,
                money INTEGER DEFAULT 0,
                last_daily TEXT
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS giveaways (
                message_id INTEGER PRIMARY KEY,
                channel_id INTEGER,
                prize TEXT,
                end_time TEXT,
                winners INTEGER DEFAULT 1
            )
        """)
        await db.commit()

async def get_user(user_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)) as cursor:
            row = await cursor.fetchone()
            if row is None:
                await db.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))
                await db.commit()
                return {"user_id": user_id, "xp": 0, "level": 1, "money": 0, "last_daily": None}
            return {
                "user_id": row[0],
                "xp": row[1],
                "level": row[2],
                "money": row[3],
                "last_daily": row[4]
            }

async def update_user(user_id: int, **kwargs):
    async with aiosqlite.connect(DB_NAME) as db:
        for key, value in kwargs.items():
            await db.execute(f"UPDATE users SET {key} = ? WHERE user_id = ?", (value, user_id))
        await db.commit()
