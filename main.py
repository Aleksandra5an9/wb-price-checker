from telegram.ext import Updater, CommandHandler
from dotenv import load_dotenv
import os

from parser import get_price  # импортируй свою функцию

load_dotenv()

def start(update, context):
    update.message.reply_text('Привет! Введи артикул WB.')

def check_price(update, context):
    if not context.args:
        update.message.reply_text("Укажи артикул Wildberries.")
        return
    wb_id = context.args[0]
    price = get_price(wb_id)
    if price:
        update.message.reply_text(f"Цена товара {wb_id}: {price} ₽")
    else:
        update.message.reply_text(f"Товар {wb_id} не найден.")

def main():
    token = os.getenv("TELEGRAM_TOKEN")
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("check", check_price))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
