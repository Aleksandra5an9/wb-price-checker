import requests
import os
import time
from dotenv import load_dotenv

# Загрузка переменных из .env файла
load_dotenv()

# API ключ
WB_API_KEY = os.getenv("WB_API_KEY")

# URL для проверки подключения
url = "https://content-api.wildberries.ru/ping"

# Заголовки (если требуется токен или ключ)
headers = {
    "Authorization": f"Bearer {WB_API_KEY}"  # Используйте ваш реальный API ключ
}

# Отправляем запрос
response = requests.get(url, headers=headers)

# Проверка результата
if response.status_code == 200:
    print("Подключение успешно!")
else:
    print(f"Ошибка: {response.status_code}")
    try:
        error_details = response.json()
        print("Подробности ошибки:", error_details)
    except ValueError:
        print("Не удалось распарсить ответ, возможно, не в формате JSON")
        print("Ответ:", response.text)

# Далее, ваш основной код
# Например, можно продолжить выполнение скрипта для получения цен

load_dotenv()

WB_API_KEY = os.getenv("WB_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

WB_IDS = ["260800583", "260897865"]  # пример: артикулы с WB

def get_price(wb_id):
    url = f"https://card.wb.ru/cards/detail?appType=1&curr=rub&nm={wb_id}"
    r = requests.get(url)
    try:
        price = r.json()["data"]["products"][0]["priceU"] // 100
        return price
    except Exception:
        return None

def send_message(text):
    requests.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", params={
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text
    })

def main():
    message = "📦 Цены товаров на WB:\n"
    for wb_id in WB_IDS:
        price = get_price(wb_id)
        if price:
            message += f"- {wb_id}: {price} ₽\n"
        else:
            message += f"- {wb_id}: не найден\n"
    send_message(message)

if __name__ == "__main__":
    main()
