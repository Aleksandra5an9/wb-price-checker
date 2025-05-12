import os
import requests
from dotenv import load_dotenv

load_dotenv()  # Загружаем переменные из .env
API_KEY = os.getenv("API_KEY")  # Получаем API ключ

def get_wb_price(nm_id):
    url = f"https://discounts-prices-api.wildberries.ru/api/v2/list/goods/filter"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",  # используем только этот заголовок
    }

    params = {
        "limit": 10,
        "filterNmID": nm_id  # Артикул товара, который нужно проверить
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Поднимет исключение для ошибок HTTP
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе: {e}")
        return None
    
    if response.status_code == 200:
        data = response.json()
        
        # Выведем информацию о товаре
        if "data" in data and "listGoods" in data["data"]:
            product = data["data"]["listGoods"][0]
            print(f"Артикул: {product['nmID']}")
            print(f"Код товара: {product['vendorCode']}")
            print(f"Размеры: {', '.join([size['techSizeName'] for size in product['sizes']])}")
            
            for size in product["sizes"]:
                print(f"Размер: {size['techSizeName']}")
                print(f"Цена: {size['price'] / 100} ₽")
                print(f"Цена со скидкой: {size['discountedPrice'] / 100} ₽")
                print(f"Цена для WB Клуба: {size['clubDiscountedPrice'] / 100} ₽")
                print("-" * 50)
            
            # Печать дополнительной информации о скидке
            print(f"Общая скидка: {product['discount']}%")
            print(f"Скидка для WB Клуба: {product['clubDiscount']}%")
        
        return data
    else:
        print(f"Ошибка {response.status_code}: {response.text}")
        return None

if __name__ == "__main__":
    nm_id = 260800583  # Пример ID товара
    result = get_wb_price(nm_id)
    if result:
        print(result)
