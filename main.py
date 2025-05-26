import os
import requests
import telegram

API_KEY_WB = os.getenv("API_KEY")  # Твой токен для авторизации
URL = "https://discounts-prices-api.wildberries.ru/api/v2/list/goods/filter"
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

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

def format_message(products):
    lines = []
    for product in products:
        vendor_code = product.get('vendorCode', 'N/A')
        sizes = product.get('sizes', [])
        if sizes:
            discounted_price = sizes[0].get('discountedPrice', 'N/A')
            lines.append(f"VendorCode: {vendor_code}, DiscountedPrice: {discounted_price} RUB")
        else:
            lines.append(f"VendorCode: {vendor_code}, DiscountedPrice: N/A")
    return "\n".join(lines)

def send_telegram_message(text):
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
        print(f"Формируем сообщение для Telegram:\n{message}")
        send_telegram_message(message)
        print("Сообщение отправлено")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()
