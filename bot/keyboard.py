from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def login_keyboard():
    """Возвращает клавиатуру с кнопкой для входа."""
    keyboard = [[InlineKeyboardButton("Войти", callback_data="login")]]
    return InlineKeyboardMarkup(keyboard)


def get_booking_keyboard():
    """Возвращает клавиатуру с кнопкой для сегодняшних бронирований."""
    keyboard = [
        [InlineKeyboardButton("❇️ Запросить бронирования", callback_data="get_bookings")]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_back_keyboard() -> InlineKeyboardMarkup:
    keyboard = [[InlineKeyboardButton("⏎ Назад", callback_data="back")]]
    return InlineKeyboardMarkup(keyboard)
