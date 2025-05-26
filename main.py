import os
import requests
import telegram

API_URL = os.getenv("API_KEY")  # замени на реальный URL
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def fetch_products():
    params = {'limit': 10, 'offset': 0}
    response = requests.get(API_URL, params=params)
    response.raise_for_status()
    return response.json()

def format_message(products):
    lines = []
    for product in products:
        vendor_code = product.get('vendorCode', 'N/A')
        sizes = product.get('sizes', [])
        if sizes:
            discounted_price = sizes[0].get('discountedPrice', 'N/A')
            lines.append(f"VendorCode: {vendor_code}, DiscountedPrice: {discounted_price} RUB")
    return "\n".join(lines)

def send_telegram_message(text):
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    bot.send_message(chat_id=CHAT_ID, text=text)

def main():
    data = fetch_products()
    goods = data.get('data', {}).get('listGoods', [])
    if not goods:
        print("Нет данных о товарах")
        return
    message = format_message(goods)
    send_telegram_message(message)
    print("Сообщение отправлено")

if __name__ == "__main__":
    main()
