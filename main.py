import os
import requests
import telegram

API_KEY_WB = os.getenv("API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

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

def fetch_products():
    params = {'limit': 10, 'offset': 0}
    print(f"Запрос к API: {URL} с параметрами {params}")
    response = requests.get(URL, headers=HEADERS, params=params)
    print(f"Ответ API: статус {response.status_code}")
    response.raise_for_status()
    data = response.json()
    print(f"Полученные данные: {data}")
    return data

def escape_markdown(text: str) -> str:
    """
    Экранирует специальные символы для Telegram MarkdownV2
    """
    escape_chars = r'\_*[]()~`>#+-=|{}.!'
    return ''.join(f'\\{c}' if c in escape_chars else c for c in text)

def format_message(products):
    lines = []
    for product in products:
        vendor_code = product.get('vendorCode', 'N/A')
        sizes = product.get('sizes', [])
        if sizes and sizes[0].get('discountedPrice') is not None:
            discounted_price = sizes[0]['discountedPrice']
            line = f"*VendorCode:* `{escape_markdown(vendor_code)}`, *DiscountedPrice:* {discounted_price} RUB"
        else:
            line = f"*VendorCode:* `{escape_markdown(vendor_code)}`, *DiscountedPrice:* N/A"
        lines.append(line)
    return "\n".join(lines)

def send_telegram_message(text):
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    bot.send_message(chat_id=CHAT_ID, text=text, parse_mode='MarkdownV2')

def main():
    try:
        data = fetch_products()
        goods = data.get('data', {}).get('listGoods', [])
        if not goods:
            print("Нет данных о товарах")
            return
        message = format_message(goods)
        print(f"Формируем сообщение для Telegram:\n{message}")
        send_telegram_message(message)
        print("Сообщение отправлено")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()
