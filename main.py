import os
import requests
from dotenv import load_dotenv

load_dotenv()  # Загружаем переменные из .env
API_KEY = os.getenv("API_KEY")  # Получаем API ключ

def get_wb_price(nm_id):
    url = f"https://discounts-prices-api.wildberries.ru/api/v2/list/goods/filter"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "HeaderApiKey": API_KEY
    }

    params = {
        "limit": 10,
        "filterNmID": nm_id
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Поднимет исключение для ошибок HTTP
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе: {e}")
        return None
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Ошибка {response.status_code}: {response.text}")
        return None

if __name__ == "__main__":
    nm_id = 44589768676  # Пример ID товара
    result = get_wb_price(nm_id)
    if result:
        print(result)
