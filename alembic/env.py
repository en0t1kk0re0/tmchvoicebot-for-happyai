import asyncio
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.orm import sessionmaker
from alembic import context

# Подключение к базе данных с использованием асинхронного движка
DATABASE_URL = "postgresql+asyncpg://postgres:sudo@localhost/voicebot"
engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=True)

def run_migrations_online():
    # Создаём подключение в асинхронном контексте
    asyncio.run(run_migrations())

async def run_migrations():
    # Создаём сессию и начинаем миграции
    async with engine.begin() as connection:
        context.configure(connection=connection)
        await context.run_migrations()

if __name__ == "__main__":
    run_migrations_online()
