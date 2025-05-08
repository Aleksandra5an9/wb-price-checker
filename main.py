import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from parser import get_price  # твоя функция парсинга

load_dotenv()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Привет! Введи артикул WB.')

async def check_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Укажи артикул Wildberries.")
        return

    wb_id = context.args[0]
    price = get_price(wb_id)

    if price:
        await update.message.reply_text(f"Цена товара {wb_id}: {price} ₽")
    else:
        await update.message.reply_text(f"Товар {wb_id} не найден.")

def main():
    token = os.getenv("TELEGRAM_TOKEN")
    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("check", check_price))

    application.run_polling()

if __name__ == '__main__':
    main()
