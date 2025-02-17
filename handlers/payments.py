from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, LabeledPrice, PreCheckoutQuery, Message
import config
from database import get_db
from services.payment_service import get_final_price_for_user
from services.subscription_service import check_subscription, save_subscription, update_subscription
import logging

router = Router()

@router.message(F.text == "Купить подписку")
async def buy_subscription(callback_query: CallbackQuery) -> None:
    """
    Покупка подписки.
    :param callback_query: колбэк запрос
    :return: None
    """

    user_id = callback_query.from_user.id
    subscription = None

    async for db in get_db():
        subscription = await check_subscription(user_id, db)

    final_price_for_user = get_final_price_for_user(subscription)

    if subscription:
        await callback_query.message.answer("Круто, видим вы уже ранее покупали подписку, для вас есть скидка!")

    prices = [LabeledPrice(label="Обучение", amount=final_price_for_user)]
    await callback_query.message.bot.send_invoice(
        callback_query.message.chat.id,
        title=config.product_title,
        description=config.product_description,
        provider_token=config.PROVIDER_TOKEN,
        currency="RUB",
        photo_url=config.product_photo,
        photo_width=416 * 2,
        photo_height=416 * 2,
        photo_size=416 * 2,
        is_flexible=False,
        prices=prices,
        start_parameter=config.product_start_parameter,
        payload=config.product_payload
    )

@router.callback_query(F.data == "training")
async def training_button_click(callback_query: CallbackQuery) -> None:
    """
    Обработчик кнопки "Хочу на обучение".
    :param callback_query: колбэк запрос
    :return: None
    """
    await callback_query.answer(callback_query.id)
    await buy_subscription(callback_query)

@router.pre_checkout_query()
async def pre_checkout_handler(pre_checkout_query: PreCheckoutQuery) -> None:
    """
    Обработчик предварительного запроса на оплату.
    :param pre_checkout_query: колбэк запрос
    :return: None
    """
    await pre_checkout_query.bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@router.message(F.content_type == "successful_payment")
async def successful_payment_handler(message: Message, bot: Bot) -> None:
    """
    Обработчик успешной оплаты.
    :param message: сообщение
    :param bot: экземпляр бота
    :return: None
    """
    user_id = str(message.from_user.id)

    async for db in get_db():
        user = await check_subscription(user_id, db)
        if user:
            await update_subscription(user_id, db, bot)
        else:
            try:
                invite_link = await bot.create_chat_invite_link(config.channel_id, expire_date=None, member_limit=1)
                await bot.send_message(user_id,
                                       f"""Поздравляю! Твоя подписка активирована. 
                                       Вступайте в канал: {invite_link.invite_link}
                                       """)
                await save_subscription(user_id, invite_link.invite_link, db)

            except Exception as e:
                logging.error(f"Ошибка при добавлении в канал {user_id}: {e}")
                await message.answer("Что-то пошло не так. Свяжитесь с поддержкой.")
                return

    await message.answer("Спасибо за покупку! Платеж обработан.")