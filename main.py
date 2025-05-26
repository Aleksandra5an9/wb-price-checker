import os
import requests
from time import sleep

API_KEY_WB = os.getenv("API_KEY")  # Укажи в Railway переменную окружения с API ключом Wildberries
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # Токен Telegram бота
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")      # ID чата или канала Telegram

PRODUCT_IDS = [
    260800583,
    260897865,
    293878560,
    # Добавь нужные артикула
]

def get_prices(product_ids):
    url = "https://discounts-prices-api.wildberries.ru/api/v2/list/goods/filter"
    headers = {
        "Authorization": f"Bearer {API_KEY_WB}"
    }
    prices_info = []
    for nm_id in product_ids:
        params = {"filterNmID": nm_id, "limit": 1}
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            products = data.get("data", {}).get("products", [])
            if products:
                product = products[0]
                name = product.get("name", "Нет названия")
                price = product.get("salePriceU") or product.get("price") or None
                if price:
                    price = price / 100  # Цена в копейках, переводим в рубли
                    prices_info.append(f"{name}: {price} ₽")
                else:
                    prices_info.append(f"{name}: цена не найдена")
            else:
                prices_info.append(f"Артикул {nm_id}: данные не найдены")
        elif response.status_code == 401:
            prices_info.append(f"Артикул {nm_id}: ошибка 401 - неавторизован")
            break  # если 401 — прекращаем, ключ неверный
        else:
            prices_info.append(f"Артикул {nm_id}: ошибка запроса {response.status_code}")
        sleep(0.3)  # чтобы не превысить лимит запросов
    return prices_info

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        print("Ошибка Telegram:", response.status_code, response.text)
        return False
    return True

def main():
    prices = get_prices(PRODUCT_IDS)
    message = "\n".join(prices)
    success = send_telegram_message(message)
    if success:
        print("Сообщение отправлено в Telegram")
    else:
        print("Ошибка отправки сообщения в Telegram")

if __name__ == "__main__":
    main()
