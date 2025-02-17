from aiogram import Router
from aiogram.types import Message

from database import get_db
from keyboards import training_keyboard, renew_keyboard
from config import start_message
from services.subscription_service import check_subscription

router = Router()

@router.message(lambda message: message.text == "/start")
async def start_command(message: Message):
    user_first_name = message.from_user.first_name

    user_id = message.from_user.id
    subscription = None

    async for db in get_db():
        subscription = await check_subscription(user_id, db)

    if subscription:
        await message.answer(
            f"✨ Привет, дорогая {user_first_name}!✨Ты можешь продлить подписку, или просто её возобновить",
            reply_markup=renew_keyboard,
            parse_mode='HTML'
        )
    else:
        await message.answer(
            f"✨ Привет, дорогая {user_first_name}!✨\n{start_message}",
            reply_markup=training_keyboard,
            parse_mode='HTML'
        )