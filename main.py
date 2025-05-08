from telegram import Bot
from parser import get_price
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")  # должен быть указан в .env
bot = Bot(token=TOKEN)

# Список артикулов
articuls = ["12345678", "87654321"]  # замени на реальные

for wb_id in articuls:
    price = get_price(wb_id)
    if price:
        bot.send_message(chat_id=CHAT_ID, text=f"Цена товара {wb_id}: {price} ₽")
    else:
        bot.send_message(chat_id=CHAT_ID, text=f"Товар {wb_id} не найден.")
