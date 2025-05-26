import requests

# === ТВОИ ДАННЫЕ ===
WB_TOKEN = "ТВОЙ_WB_TOKEN"
TELEGRAM_BOT_TOKEN = "ТВОЙ_TELEGRAM_BOT_TOKEN"
TELEGRAM_CHAT_ID = "ТВОЙ_CHAT_ID"

# Артикулы WB
nm_ids = [
    260800583, 260897865, 293878560, 332051245, 332082880,
    332084081, 332084082, 332084083, 375740835, 375742309,
    375744765, 375744766
]

# Запрос к Wildberries Discounts API
def get_prices(nm_ids):
    url = "https://discounts-prices-api.wildberries.ru/api/v2/list/goods/filter"
    headers = {
        "Authorization": WB_TOKEN,
        "Content-Type": "application/json"
    }
    payload = {"nm": nm_ids}

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json().get("data", [])
    else:
        print("Ошибка при запросе к WB API:", response.status_code)
        return []

# Отправка в Telegram
def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    requests.post(url, data=payload)

# Основная логика
def main():
    products = get_prices(nm_ids)
    if not products:
        send_to_telegram("❗️Не удалось получить данные от Wildberries.")
        return

    messages = []
    for item in products:
        name = item.get("name") or "Без названия"
        sale_price = item.get("salePrice", 0) / 100  # Цена в копейках
        messages.append(f"{name} ({item.get('brand', '')}): {sale_price:.2f} ₽")

    full_message = "\n\n".join(messages)
    send_to_telegram(full_message)

# Запуск
if __name__ == "__main__":
    main()
