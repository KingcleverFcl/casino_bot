import asyncpg
import os

DB = None

async def create_db():
    global DB
    DB = await asyncpg.create_pool(
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DB_NAME"],
        host=os.environ["DB_HOST"],
        port=os.environ["DB_PORT"]
    )
    async with DB.acquire() as conn:
        await conn.execute(open("dealer_bot/models.sql").read())