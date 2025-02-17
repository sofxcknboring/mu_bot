from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

training_button = InlineKeyboardButton(text="Хочу на обучение", callback_data="training")
training_keyboard = InlineKeyboardMarkup(inline_keyboard=[[training_button]])
