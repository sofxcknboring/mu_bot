import logging
from datetime import datetime, timedelta

from aiogram import Bot
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

import config
from models import Subscription

async def check_subscription(user_id: int, db: AsyncSession) -> Subscription | None:
    """
    Проверка подписки.
    :param user_id: идентификатор пользователя
    :param db: сессия базы данных
    :return: подписка или None
    """
    query = select(Subscription).filter(Subscription.user_id == user_id)
    result = await db.execute(query)
    subscription = result.scalar_one_or_none()
    if not subscription:
        logging.info(f"{user_id} отсутствует в базе данных")
    elif subscription:
        logging.info(f"Подписка пользователя {user_id} найдена")
    return subscription

async def save_subscription(user_id: str, invite_link: str, db: AsyncSession) -> None:
    """
    Сохранение подписки.
    :param user_id: идентификатор пользователя
    :param invite_link: уникальная ссылка-приглашение
    :param db: сессия базы данных
    :return: None
    """
    subscription = Subscription(
        user_id=user_id,
        expiry_date=datetime.now() + timedelta(days=30),
        invite_link=invite_link,
        status=True,
    )
    db.add(subscription)
    await db.commit()


async def update_subscription(user_id: int, db: AsyncSession, bot: Bot) -> None:
    """
    Продление подписки. Если подписка была неактивной, создаётся новая ссылка.
    """
    query = select(Subscription).filter(Subscription.user_id == user_id)
    result = await db.execute(query)
    subscription = result.scalar_one_or_none()

    if subscription:
        if subscription.status:
            subscription.expiry_date += timedelta(days=30)
            await bot.send_message(
                user_id,
                f"Подписка продлена до {subscription.expiry_date.strftime('%d.%m.%Y')}"
            )
        else:
            invite_link = await bot.create_chat_invite_link(config.channel_id, expire_date=None, member_limit=1)
            subscription.expiry_date = datetime.now() + timedelta(days=30)
            subscription.status = True
            subscription.invite_link = invite_link.invite_link

            await bot.send_message(
                user_id,
                f"""Поздравляю! Твоя подписка активирована. 
                Вступите в канал: {invite_link.invite_link}"""
            )

        await db.commit()
    else:
        logging.error(f"Подписка пользователя {user_id} не найдена")

