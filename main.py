import os
import requests
import telegram
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

# Получаем переменные окружения
API_KEY_WB = os.getenv("API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Проверка переменных окружения
if not API_KEY_WB:
    raise ValueError("API_KEY не задана в переменных окружения")
if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN не задан")
if not CHAT_ID:
    raise ValueError("TELEGRAM_CHAT_ID не задан")

URL = "https://discounts-prices-api.wildberries.ru/api/v2/list/goods/filter"
HEADERS = {
    "Authorization": f"Bearer {API_KEY_WB}"
}

def fetch_products(limit=10, offset=0):
    params = {'limit': limit, 'offset': offset}
    logging.info(f"Запрос к API: {URL} с параметрами {params}")
    response = requests.get(URL, headers=HEADERS, params=params)
    logging.info(f"Ответ API: статус {response.status_code}")
    response.raise_for_status()
    data = response.json()
    logging.info(f"Получено товаров: {len(data.get('data', {}).get('listGoods', []))}")
    return data

def escape_markdown(text: str) -> str:
    """
    Экранирует все специальные символы для Telegram MarkdownV2.
    """
    if not text:
        return ""
    escape_chars = r'_*[]()~`>#+-=|{}.!,:'
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
        # Экранируем только vendorCode (строка) и discounted_price (число в строке) для безопасности
        line = f"{escape_markdown(str(vendor_code))} - {escape_markdown(str(discounted_price))} RUB"
        lines.append(line)
    return "\n".join(lines)

async def send_telegram_message(text):
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    try:
        async with bot:
            await bot.send_message(chat_id=CHAT_ID, text=text, parse_mode='MarkdownV2')
        logging.info("Сообщение успешно отправлено в Telegram")
    except telegram.error.TelegramError as e:
        logging.error(f"Ошибка при отправке сообщения в Telegram: {e}")
        raise

async def main():
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
