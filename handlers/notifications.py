import asyncio
import logging
from datetime import datetime, timedelta

from aiogram import Bot
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models import Subscription
import config


async def check_subscriptions(bot: Bot, db: AsyncSession):
    now = datetime.now()
    warning_date = now + timedelta(days=2)

    query = select(Subscription)
    result = await db.execute(query)
    subscriptions = result.scalars().all()

    for sub in subscriptions:
        user_id = sub.user_id

        if sub.expiry_date.date() == warning_date.date():
            try:
                await bot.send_message(user_id, "⚠️ Ваша подписка истекает через 2 дня! "
                                                "Вы можете продлить её прямо сейчас. Напишите /start")
                logging.info(f"Отправлено уведомление пользователю {user_id} о скором истечении подписки")
            except Exception as e:
                logging.error(f"Ошибка отправки уведомления {user_id}: {e}")

        if sub.expiry_date <= now and sub.status:
            try:
                await bot.ban_chat_member(config.channel_id, user_id, revoke_messages=True)
                await bot.unban_chat_member(config.channel_id, user_id, only_if_banned=True)
                sub.status = False
                await db.commit()  # Здесь коммитим изменения
                logging.info(f"Пользователь {user_id} удален из канала.")

                if sub.invite_link:
                    await bot.revoke_chat_invite_link(config.channel_id, sub.invite_link)
                    logging.info(f"Ссылка {sub.invite_link} отозвана")
                    sub.invite_link = None
                    await db.commit()

            except Exception as e:
                logging.error(f"Ошибка удаления пользователя {user_id}: {e}")

# Основная функция для запуска проверок подписок
async def schedule_subscription_check(bot: Bot):
    while True:
        async for db in get_db():
            await check_subscriptions(bot, db)
        await asyncio.sleep(86400)  # Проверка раз в 24 часа