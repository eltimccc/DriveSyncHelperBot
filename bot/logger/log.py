import logging


def setup_logging():
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
        handlers=[logging.FileHandler("bot.log"), logging.StreamHandler()],
    )

    httpx_logger = logging.getLogger("httpx")
    httpx_logger.setLevel(logging.WARNING)
