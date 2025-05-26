import requests

# --- Настройки ---
TOKEN = "API_KEY"
TELEGRAM_BOT_TOKEN = "TELEGRAM_BOT_TOKEN"
CHAT_ID = "TELEGRAM_CHAT_ID"  

product_ids = [
    "260800583",
    "260897865",
    "293878560",
    "332051245",
    # добавь остальные ID сюда
]

# --- Функция для получения цен с WB API ---
def get_wb_prices(product_ids):
    url = "https://discounts-prices-api.wildberries.ru/api/v2/list/goods/filter"
    params = {
        "ids": ",".join(product_ids),
        "dest": "123"  # можно менять, если нужно
    }
    headers = {
        "Authorization": TOKEN
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code != 200:
        print(f"Ошибка при запросе к WB API: {response.status_code}")
        print(response.text)
        return None

    data = response.json()
    return data.get("data", {}).get("products", [])

# --- Функция для отправки сообщения в Telegram ---
def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    response = requests.post(url, data=payload)
    if response.status_code != 200:
        print(f"Ошибка отправки сообщения в Telegram: {response.status_code}")
        print(response.text)

# --- Основной код ---
def main():
    products = get_wb_prices(product_ids)
    if not products:
        send_telegram_message("Не удалось получить данные по товарам.")
        return

    messages = []
    for product in products:
        name = product.get("name", "Без названия")
        price = product.get("priceU", 0) / 100  # Цена в копейках, переводим в рубли
        messages.append(f"{name}: {price} ₽")

    message_text = "\n".join(messages)
    send_telegram_message(message_text)

if __name__ == "__main__":
    main()
