import requests
import os
from dotenv import load_dotenv

# Загрузка переменных из .env
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Артикулы товаров
WB_IDS = ["260800583", "260897865"]  # Можно добавить свои

def get_price_via_search(wb_id):
    url = f"https://search.wb.ru/exactmatch/ru/common/v4/search?query={wb_id}&resultset=catalog"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    print(f"Ответ от поиска для {wb_id}: {response.status_code}")
    try:
        data = response.json()
        product = data["data"]["products"][0]
        price = product["salePriceU"] // 100  # Цена со скидкой
        name = product["name"]
        print(f"Найдено: {name}, цена: {price} ₽")
        return f"{name}: {price} ₽"
    except (KeyError, IndexError) as e:
        print(f"Не удалось получить цену для {wb_id}: {e}")
        return f"{wb_id}: не найден"

def send_message(text):
    requests.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", params={
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text
    })

def main():
    message = "📦 Цены товаров на WB:\n"
    for wb_id in WB_IDS:
        result = get_price_via_search(wb_id)
        message += f"- {result}\n"
    send_message(message)

if __name__ == "__main__":
    main()
