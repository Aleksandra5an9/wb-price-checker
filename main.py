from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
import asyncio
import os
import telegram
import requests
import logging

# Настройка логов
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

app = Flask(__name__)

# Переменные окружения
API_KEY_WB = os.getenv("API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_IDS = os.getenv("TELEGRAM_CHAT_IDS", "").split(",")

# Проверка переменных
if not API_KEY_WB or not TELEGRAM_TOKEN or not CHAT_IDS:
    raise ValueError("Не заданы необходимые переменные окружения")

# Заголовки запроса к WB
HEADERS = {"Authorization": f"Bearer {API_KEY_WB}"}
URL = "https://discounts-prices-api.wildberries.ru/api/v2/list/goods/filter"

# Функции
def fetch_products(limit=20, offset=0):
    params = {'limit': limit, 'offset': offset}
    response = requests.get(URL, headers=HEADERS, params=params)
    response.raise_for_status()
    data = response.json()
    return data

def escape_markdown(text: str) -> str:
    if not text:
        return ""
    escape_chars = r'\_*[]()~`>#+-=|{}.!,:'
    return ''.join(f'\\{c}' if c in escape_chars else c for c in text)

def format_message(products):
    lines = []
    for product in products:
        vendor_code = product.get('vendorCode', 'N/A')
        sizes = product.get('sizes', [])
        discounted_price = "N/A"
        if sizes and sizes[0].get('discountedPrice'):
            discounted_price = sizes[0]['discountedPrice']
        line = escape_markdown(f"{vendor_code} - {discounted_price} RUB")
        lines.append(line)
    return "\n".join(lines)

async def send_telegram_message(text):
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    async with bot:
        for chat_id in CHAT_IDS:
            await bot.send_message(chat_id=chat_id.strip(), text=text, parse_mode='MarkdownV2')

def run_async_task():
    logging.info("Запуск фоновой задачи...")
    asyncio.run(task())

async def task():
    try:
        data = fetch_products()
        goods = data.get('data', {}).get('listGoods', [])
        if not goods:
            logging.warning("Нет товаров")
            return
        message = format_message(goods)
        logging.info(f"Отправка сообщения:\n{message}")
        await send_telegram_message(message)
    except Exception as e:
        logging.error(f"Ошибка в задаче: {e}")

# Запуск планировщика
scheduler = BackgroundScheduler()
scheduler.add_job(run_async_task, 'interval', hours=4)
scheduler.start()

# Flask эндпоинт (для Render ping)
@app.route("/")
def home():
    return "Бот работает"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
