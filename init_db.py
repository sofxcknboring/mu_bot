import asyncio
from database import engine, Base
from models import Subscription

async def init_db():
    """ Функция создаёт таблицы в БД """
    async with engine.begin() as conn:
        # Создание всех таблиц, если они не существуют
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(init_db())
