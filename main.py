import requests
import time

from dotenv import load_dotenv
import os

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
