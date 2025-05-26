import os
import requests
from time import sleep

API_KEY_WB = os.getenv("API_KEY")  # Укажи в Railway как переменную окружения
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

GET https://discounts-prices-api.wildberries.ru/ping
Headers:
Authorization: Bearer <API_KEY_WB>
