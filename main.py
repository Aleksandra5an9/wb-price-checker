import requests
import os

# 🔧 Настройки
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # Задай в Railway как переменную окружения
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")      # ID чата (можно свой user_id)

product_ids = [
    260800583, 260897865, 293878560, 332051245, 332082880,
    332084081, 332084082, 332084083, 375740835, 375742309,
    375744765, 375744766
]

def get_product_info(nm_id):
    url = f"https://card.wb.ru/cards/v2/detail?appType=1&curr=rub&dest=-1255987&spp=30&ab_testing=false&nm={nm_id}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        try:
            product = data['data']['products'][0]
            name = product['name']
            brand = product.get('brand', 'Не указано')
            price = product.get('priceU', 0) // 100
            sale_price = product.get('salePriceU', 0) // 100

            if sale_price:
                return f"{name} ({brand}): {sale_price} ₽ (скидка, было {price} ₽)"
            else:
                return f"{name} ({brand}): {price} ₽"
        except (IndexError, KeyError):
            return f"{nm_id}: ❌ Товар не найден или ошибка структуры"
    else:
        return f"{nm_id}: ⚠️ Ошибка запроса ({response.status_code})"

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    requests.post(url, data=payload)

def main():
    messages = [get_product_info(pid) for pid in product_ids]
    full_message = "\n\n".join(messages)
    send_telegram_message(full_message)
    print("✅ Сообщение отправлено!")

if __name__ == "__main__":
    main()
