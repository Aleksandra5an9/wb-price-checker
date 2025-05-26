import os
import requests
import telegram

API_URL = os.getenv("API_KEY")  # Твой реальный URL API
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def fetch_products():
    params = {'limit': 10, 'offset': 0}
    print(f"Запрос к API: {API_URL} с параметрами {params}")
    response = requests.get(API_URL, params=params)
    print(f"Ответ API: статус {response.status_code}")
    response.raise_for_status()
    data = response.json()
    print(f"Полученные данные: {data}")
    return data

def format_message(products):
    lines = []
    for product in products:
        vendor_code = product.get('vendorCode', 'N/A')
        sizes = product.get('sizes', [])
        if sizes:
            discounted_price = sizes[0].get('discountedPrice', 'N/A')
            line = f"VendorCode: {vendor_code}, DiscountedPrice: {discounted_price} RUB"
            print(f"Формируем строку: {line}")
            lines.append(line)
        else:
            print(f"Товар {vendor_code} без размеров или цен")
    if not lines:
        print("Нет товаров с ценами для отправки")
    return "\n".join(lines)

def send_telegram_message(text):
    print(f"Отправляем сообщение в Telegram:\n{text}")
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    bot.send_message(chat_id=CHAT_ID, text=text)

def main():
    try:
        data = fetch_products()
        goods = data.get('data', {}).get('listGoods', [])
        if not goods:
            print("Нет данных о товарах")
            return
        message = format_message(goods)
        if message:
            send_telegram_message(message)
            print("Сообщение отправлено")
        else:
            print("Сообщение пустое, отправка не требуется")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()

