import os
import requests
from time import sleep

API_KEY_WB = os.getenv("API_KEY")  # Укажи в Railway как переменную окружения
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

PRODUCT_IDS = [
    260800583,
    260897865,
    293878560,
    332051245,
    332082880,
    332084081,
    332084082,
    332084083,
    375740835,
    375742309,
    375744765,
    375744766,
]

def get_prices(product_ids):
    url = "https://discounts-prices-api.wildberries.ru/api/v2/list/goods/filter"
    headers = {
        "X-API-KEY": API_KEY_WB
    }
    prices_info = []

    for nm_id in product_ids:
        params = {"filterNmID": nm_id, "limit": 1}
        try:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                data = response.json()
                product_list = data.get("data", {}).get("products", [])
                if product_list:
                    product = product_list[0]
                    name = product.get("name", "Нет названия")
                    price = product.get("salePriceU") or product.get("priceU") or 0
                    price = price / 100  # цены в копейках
                    prices_info.append(f"{name}: {price} ₽")
                else:
                    prices_info.append(f"Артикул {nm_id}: данные не найдены")
            else:
                prices_info.append(f"Артикул {nm_id}: ошибка запроса {response.status_code}")
        except Exception as e:
            prices_info.append(f"Артикул {nm_id}: ошибка {str(e)}")
        sleep(0.5)  # защита от лимитов API

    return prices_info

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text
    }
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        print("Ошибка Telegram:", response.status_code, response.text)
        return False
    return True

def main():
    prices = get_prices(PRODUCT_IDS)
    message = "\n".join(prices)
    if send_telegram_message(message):
        print("✅ Цены успешно отправлены в Telegram")
    else:
        print("❌ Ошибка при отправке сообщения в Telegram")

if __name__ == "__main__":
    main()
