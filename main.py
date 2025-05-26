import requests

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # Задай в Railway как переменную окружения
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID") 

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
    }
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        print("Ошибка Telegram:", response.status_code, response.text)
        return False
    return True

if __name__ == "__main__":
    if send_telegram_message("Привет! Это тестовое сообщение."):
        print("Сообщение успешно отправлено!")
    else:
        print("Ошибка отправки.")
