import os
import requests
import telegram
import asyncio
import logging
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

API_KEY_WB = os.getenv("API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_IDS = os.getenv("TELEGRAM_CHAT_IDS", "").split(",")

if not API_KEY_WB:
    raise ValueError("API_KEY не задана в переменных окружения")
if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN не задан")
if not CHAT_IDS:
    raise ValueError("TELEGRAM_CHAT_IDS не заданы")

URL = "https://discounts-prices-api.wildberries.ru/api/v2/list/goods/filter"
HEADERS = {
    "Authorization": f"Bearer {API_KEY_WB}"
}

def is_even_hour():
    # Приводим UTC ко времени Стамбула (+3 часа)
    istanbul_time = datetime.utcnow() + timedelta(hours=3)
    current_hour = istanbul_time.hour

    logging.info(f"[DEBUG] Текущее стамбульское время: {istanbul_time}, Час: {current_hour}")

    return current_hour % 2 == 0

def fetch_products(limit=20, offset=0):
    params = {'limit': limit, 'offset': offset}
    logging.info(f"Запрос к API: {URL} с параметрами {params}")
    response = requests.get(URL, headers=HEADERS, params=params)
    logging.info(f"Ответ API: статус {response.status_code}")
    response.raise_for_status()
    data = response.json()
    logging.info(f"Получено товаров: {len(data.get('data', {}).get('listGoods', []))}")
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
        if sizes:
            first_size = sizes[0]
            if first_size and first_size.get('discountedPrice') is not None:
                discounted_price = first_size['discountedPrice']
        line = escape_markdown(f"{vendor_code} - {discounted_price} RUB")
        lines.append(line)
    return "\n".join(lines)

async def send_telegram_message(text):
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    try:
        async with bot:
            for chat_id in CHAT_IDS:
                await bot.send_message(chat_id=chat_id.strip(), text=text, parse_mode='MarkdownV2')
                logging.info(f"Сообщение успешно отправлено в Telegram: {chat_id.strip()}")
    except telegram.error.TelegramError as e:
        logging.error(f"Ошибка при отправке сообщения в Telegram: {e}")
        raise

async def main():
    if not is_even_hour():
        logging.info("Пропуск отправки: нечётный час")
        return

    try:
        data = fetch_products()
        goods = data.get('data', {}).get('listGoods', [])
        if not goods:
            logging.warning("Нет данных о товарах для отправки")
            return
        message = format_message(goods)
        logging.info(f"Формируем сообщение для Telegram:\n{message}")
        await send_telegram_message(message)
    except Exception as e:
        logging.error(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    asyncio.run(main())
