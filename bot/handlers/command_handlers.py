from telegram import Update
from telegram.ext import ContextTypes

from bot.keyboard import get_booking_keyboard, login_keyboard
from bot.utils.flask_client import login_with_telegram_id


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Попытка автоматической авторизации по Telegram ID и отправка приветственного сообщения."""
    telegram_id = str(update.message.from_user.id)
    
    try:
        token = login_with_telegram_id(telegram_id)
        context.user_data['token'] = token

        await update.message.reply_text(
            "Добро пожаловать, суперпользователь!\nВыберите действие:",
            reply_markup=get_booking_keyboard()
        )
    except ValueError:
        context.user_data['awaiting_credentials'] = True
        await update.message.reply_text(
            "Ваш Telegram ID не авторизован.\nПожалуйста, введите логин и пароль в формате 'username:password'."
        )
