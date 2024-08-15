import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from bot.config import TELEGRAM_TOKEN
from bot.handlers.command_handlers import start
from bot.handlers.message_handlers import handle_credentials
from bot.handlers.message_handlers import button_handler, handle_credentials

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def main() -> None:
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_credentials)
    )

    application.run_polling()


if __name__ == "__main__":
    main()
