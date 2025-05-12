import requests
import os
from dotenv import load_dotenv

load_dotenv()  # Загружаем переменные из .env
API_KEY = os.getenv("API_KEY")  # Используем API ключ, если нужно

# Функция для получения товаров с ценами
def get_wb_products(limit=1000, offset=0, filter_nm_id=None):
    url = "https://discounts-prices-api.wildberries.ru/api/v2/list/goods/filter"
    
    headers = {
        'HeaderApiKey': API_KEY  # Ваш API ключ для авторизации
    }
    
    params = {
        'limit': limit,
        'offset': offset,
        'filterNmID': filter_nm_id  # Используется, если нужно искать по артикулу
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        print(f"Ошибка: {response.status_code}")
        return None
    
    data = response.json()
    
    if not data.get('data', {}).get('products', []):
        print("Товары не найдены или достигнут конец списка.")
        return None
    
    products = data['data']['products']
    return products

# Пример использования функции
if __name__ == "__main__":
    # Параметры запроса (например, ищем товары с артикулом или без)
    limit = 1000  # Максимум товаров на одной странице
    offset = 0  # Смещение, начинаем с первого товара
    filter_nm_id = None  # Здесь можно указать артикул товара для фильтрации

    products = get_wb_products(limit=limit, offset=offset, filter_nm_id=filter_nm_id)
    
    if products:
        for product in products:
            print(f"Название: {product['name']}, Цена: {product['price']}, Скидка: {product.get('salePrice', 'Нет скидки')}")
