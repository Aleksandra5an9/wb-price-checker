import requests

# Конфиги — замени на свои значения
API_KEY_WB = "API_KEY"
TELEGRAM_BOT_TOKEN = "TELEGRAM_BOT_TOKEN"
TELEGRAM_CHAT_ID = "TELEGRAM_CHAT_ID"

# Список артикулов Wildberries
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
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            if data and data.get("data") and data["data"].get("products"):
                product = data["data"]["products"][0]
                name = product.get("name", "Нет названия")
                # Цена может быть в поле price или priceU, зависит от API
                price = product.get("price") or product.get("salePriceU") or "Цена не найдена"
                if isinstance(price, int):
                    price = price / 100  # если цена в копейках
                prices_info.append(f"{name}: {price} ₽")
            else:
                prices_info.append(f"Артикул {nm_id}: данные не найдены")
        else:
            prices_info.append(f"Артикул {nm_id}: ошибка запроса {response.status_code}")
    return prices_info

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    response = requests.post(url, data=payload)
    return response.status_code == 200

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
