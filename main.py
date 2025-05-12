import os
import requests
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()
API_KEY = os.getenv("API_KEY")

def get_product_details(nm_id):
    url = f"https://discounts-prices-api.wildberries.ru/api/v2/list/goods/detail"
    
    headers = {
        "HeaderApiKey": API_KEY,  # Указываем ваш API ключ в заголовке
    }

    params = {
        "filterNmID": nm_id,  # Указываем ID товара для получения его данных
    }

    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if data.get('data'):
            return data['data']
        else:
            print("Нет данных о товаре.")
    else:
        print(f"Ошибка при запросе: {response.status_code}")
    return None

if __name__ == "__main__":
    nm_id = 260800583  # Замените на нужный ID товара
    product_data = get_product_details(nm_id)

    if product_data:
        print("Данные карточки товара:")
        print(product_data)  # Выводим все данные карточки товара
