import requests
from Todo_list.settings import bot_token, bot_chatID
import logging

logger = logging.getLogger(__name__)


def telegram_bot_sendtext(bot_message):
    send_text = (
        "https://api.telegram.org/bot"
        + bot_token
        + "/sendMessage?chat_id="
        + bot_chatID
        + "&text="
        + bot_message
    )
    response = requests.get(send_text)
    if response.json()["ok"]:
        logger.info("Message is sent to Telegram")
    else:
        logger.warning(
            "Telegram is not working, description: '%s'", response.json()["description"]
        )

    return response.json()
