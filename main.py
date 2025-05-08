import requests
import os
from dotenv import load_dotenv

# Загрузка переменных из .env файла
load_dotenv()

# Получаем API ключи и токены из .env
WB_API_KEY = os.getenv("WB_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Проверка подключения к API Wildberries
def check_api_connection():
    url = "https://content-api.wildberries.ru/ping"
    headers = {
        "Authorization": f"Bearer {WB_API_KEY}"  # Используйте ваш реальный API ключ
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("Подключение успешно!")
        return True
    else:
        print(f"Ошибка подключения: {response.status_code}")
        try:
            error_details = response.json()
            print("Подробности ошибки:", error_details)
        except ValueError:
            print("Не удалось распарсить ответ, возможно, не в формате JSON")
            print("Ответ:", response.text)
        return False

# Функция для получения цены товара
def get_price(wb_id):
    url = f"https://card.wb.ru/cards/detail?appType=1&curr=rub&nm={wb_id}"
    r = requests.get(url)
    try:
        price = r.json()["data"]["products"][0]["priceU"] // 100
        return price
    except Exception:
        return None

# Функция для отправки сообщения в Telegram
def send_message(text):
    requests.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", params={
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text
    })

# Основной код
def main():
    if not check_api_connection():
        print("Не удается подключиться к API Wildberries. Завершаем выполнение.")
        return

    message = "📦 Цены товаров на WB:\n"
    WB_IDS = ["260800583", "260897865"]  # Пример артикулов с WB
    for wb_id in WB_IDS:
        price = get_price(wb_id)
        if price:
            message += f"- {wb_id}: {price} ₽\n"
        else:
            message += f"- {wb_id}: не найден\n"
    
    send_message(message)

if __name__ == "__main__":
    main()
