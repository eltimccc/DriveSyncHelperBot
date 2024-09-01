from datetime import datetime
import logging
from telegram import Update
from telegram.ext import ContextTypes
from bot.config import FLASK_BOOKING_TODAY_URL
from bot.keyboard import get_back_keyboard, get_booking_keyboard
from bot.utils.flask_client import (
    get_bookings,
    login_to_flask,
    login_with_telegram_id,
)


logger = logging.getLogger(__name__)


async def handle_credentials(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Обрабатывает ввод пользователя после запроса на логин."""

    user = update.effective_user
    username = user.username if user.username else "Без имени"

    if context.user_data.get("awaiting_credentials"):
        credentials = update.message.text.split(":")

        logger.info(f"Получены учетные данные от пользователя {username}.")

        if len(credentials) != 2:
            logger.warning("Неверный формат учетных данных.")
            await update.message.reply_text(
                "Неверный формат. Введите данные в формате 'username:password'."
            )
            return

        username, password = credentials
        try:
            token = login_to_flask(username, password)
            context.user_data["token"] = token

            logger.info(f"Пользователь {username} успешно вошел в систему.")

            context.user_data["awaiting_credentials"] = False
            await update.message.delete()

            await update.message.reply_text(
                f"Добро пожаловать {username}!\nВыберите действие:",
                reply_markup=get_booking_keyboard(),
            )
        except ValueError as e:
            logger.error(f"Ошибка авторизации для пользователя {username}: {e}")
            await update.message.reply_text(str(e))


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обрабатывает нажатие на кнопки."""
    query = update.callback_query
    await query.answer()

    user = update.effective_user
    username = user.username if user.username else "Без имени"

    logger.info(f"Пользователь {username} нажал кнопку с данными: {query.data}")

    token = context.user_data.get("token")

    if query.data == "login":
        logger.info(f"Пользователь {username} выбрал вход.")
        await query.edit_message_text(
            text="Введите имя пользователя и пароль в формате 'username:password'."
        )
        context.user_data["awaiting_credentials"] = True

    elif query.data == "get_bookings":
        if token:
            bookings_info = get_bookings(token)
            logger.info(
                f"Пользователь {username} получил бронирования для текущего дня."
            )
            await query.edit_message_text(
                text=bookings_info, reply_markup=get_back_keyboard()
            )
        else:
            logger.warning("Ошибка: отсутствует токен.")
            await query.edit_message_text(
                text="Ошибка: отсутствует токен.", reply_markup=get_back_keyboard()
            )

    elif query.data == "back":
        logger.info(f"Пользователь {username} вернулся к главному меню.")
        await query.edit_message_text(
            text="Выберите действие:", reply_markup=get_booking_keyboard()
        )

    elif query.data.startswith("get_bookings_date_"):
        date_str = query.data.split("_", 3)[-1]
        try:
            selected_date = datetime.strptime(date_str, "%d.%m.%Y").strftime("%d.%m.%Y")
        except ValueError:
            message = "Некорректный формат даты."
            await query.edit_message_text(text=message)
            return

        if token:
            bookings_info = get_bookings(token, selected_date)  # с указанием даты
            await query.edit_message_text(
                text=bookings_info, reply_markup=get_back_keyboard()
            )
        else:
            logger.warning("Ошибка: отсутствует токен.")
            await query.edit_message_text(
                text="Ошибка: отсутствует токен.", reply_markup=get_back_keyboard()
            )
