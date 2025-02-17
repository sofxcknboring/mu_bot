from aiogram import Router
from aiogram.types import Message
from keyboards import training_keyboard
from config import start_message

router = Router()

@router.message(lambda message: message.text == "/start")
async def start_command(message: Message):
    user_first_name = message.from_user.first_name
    await message.answer(
        f"✨ Привет, дорогая {user_first_name}!✨\n{start_message}",
        reply_markup=training_keyboard,
        parse_mode='HTML'
    )