import asyncpg
from config import DB_HOST, DB_PORT, DB_USER, DB_PASS, DB_NAME

pool = None

async def connect():
    global pool
    pool = await asyncpg.create_pool(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME
    )

async def create_tables():
    async with pool.acquire() as conn:
        await conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id BIGINT,
            chat_id BIGINT,
            correct INTEGER DEFAULT 0,
            explained INTEGER DEFAULT 0,
            bonus INTEGER DEFAULT 0,
            PRIMARY KEY (user_id, chat_id)
        );
        """)