import os
import requests
from time import sleep

API_KEY_WB = os.getenv("API_KEY")  # Укажи в Railway как переменную окружения
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Проверка работоспособности API Wildberries
def ping_wb_api():
    url = "https://discounts-prices-api.wildberries.ru/ping"
    headers = {
        "Authorization": f"Bearer {API_KEY_WB}"
    }
    response = requests.get(url, headers=headers)
    return response.status_code, response.text

# Отправка сообщения в Telegram
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

# Основной блок
if __name__ == "__main__":
    status, message = ping_wb_api()
    text = f"Wildberries API статус: {status}\nОтвет: {message}"
    if send_telegram_message(text):
        print("Сообщение отправлено.")
    else:
        print("Ошибка отправки.")
