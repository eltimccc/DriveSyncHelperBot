from datetime import datetime, timedelta

from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def login_keyboard():
    """Возвращает клавиатуру с кнопкой для входа."""
    keyboard = [[InlineKeyboardButton("Войти", callback_data="login")]]
    return InlineKeyboardMarkup(keyboard)


def get_booking_keyboard():
    today = datetime.now()
    tomorrow = today + timedelta(days=1)
    day_after_tomorrow = today + timedelta(days=2)

    keyboard = [
        [InlineKeyboardButton("❇️ Бронирования сегодня", callback_data="get_bookings")],
        [
            InlineKeyboardButton(
                f"📅 Завтра",
                callback_data=f"get_bookings_date_{tomorrow.strftime('%d.%m.%Y')}",
            ),
            InlineKeyboardButton(
                f"📅 Послезавтра",
                callback_data=f"get_bookings_date_{day_after_tomorrow.strftime('%d.%m.%Y')}",
            ),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_back_keyboard() -> InlineKeyboardMarkup:
    keyboard = [[InlineKeyboardButton("⏎ Назад", callback_data="back")]]
    return InlineKeyboardMarkup(keyboard)
