from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

training_button = InlineKeyboardButton(text="Хочу на обучение", callback_data="training")
training_keyboard = InlineKeyboardMarkup(inline_keyboard=[[training_button]])

renew_button = InlineKeyboardButton(text="Продлить подписку", callback_data="renew_subscription")
renew_keyboard = InlineKeyboardMarkup(inline_keyboard=[[renew_button]])



