import asyncio
from app.core.db.databases import async_engine
from app.models.user import Base

async def init():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tables created successfully!")

if __name__ == "__main__":
    asyncio.run(init())
