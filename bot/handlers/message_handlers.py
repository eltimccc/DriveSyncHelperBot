import requests
from telegram import Update
from telegram.ext import ContextTypes
from bot.keyboard import get_back_keyboard, get_booking_keyboard
from bot.utils.flask_client import get_bookings_today, login_to_flask, login_with_telegram_id


async def handle_credentials(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обрабатывает ввод пользователя после запроса на логин."""
    if context.user_data.get('awaiting_credentials'):
        credentials = update.message.text.split(":")
        if len(credentials) != 2:
            await update.message.reply_text("Неверный формат. Введите данные в формате 'username:password'.")
            return

        username, password = credentials
        try:
            token = login_to_flask(username, password)
            context.user_data['token'] = token
            await update.message.delete()

            context.user_data['awaiting_credentials'] = False

            await update.message.reply_text(f"Добро пожаловать {username}!\nВыберите действие:", reply_markup=get_booking_keyboard())
        except ValueError as e:
            await update.message.reply_text(str(e))


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обрабатывает нажатие на кнопки."""
    query = update.callback_query
    await query.answer()

    if query.data == "login":
        await query.edit_message_text(text="Введите имя пользователя и пароль в формате 'username:password'.")
        context.user_data['awaiting_credentials'] = True

    elif query.data == "get_bookings":
        token = context.user_data.get('token')
        if token:
            bookings_info = get_bookings_today(token) 
            await query.edit_message_text(text=bookings_info, reply_markup=get_back_keyboard())
        else:
            await query.edit_message_text(text="Ошибка: отсутствует токен.", reply_markup=get_back_keyboard())

    elif query.data == "back":
        await query.edit_message_text(text="Выберите действие:", reply_markup=get_booking_keyboard())
