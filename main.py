import requests
import os
from dotenv import load_dotenv

# Загрузка переменных из .env файла
load_dotenv()

# API ключ
WB_API_KEY = os.getenv("WB_API_KEY")

# Список артикулов товаров
WB_IDS = ["260800583", "260897865"]

def get_price(wb_id):
    url = f"https://card.wb.ru/cards/detail?appType=1&curr=rub&nm={wb_id}"
    r = requests.get(url)
    
    # Логируем ответ от API
    print(f"Статус ответа для {wb_id}: {r.status_code}")
    print(f"Ответ от API для {wb_id}: {r.text}")  # Печатаем полный ответ от API для отладки

    try:
        response_data = r.json()
        # Логируем структуру данных, чтобы понять, как искать цену
        print(f"Данные от API для {wb_id}: {response_data}")
        
        # Пытаемся извлечь цену
        price = response_data["data"]["products"][0]["priceU"] // 100
        return price
    except Exception as e:
        print(f"Ошибка при обработке данных для {wb_id}: {e}")
        return None

def main():
    for wb_id in WB_IDS:
        price = get_price(wb_id)
        if price:
            print(f"Цена для товара {wb_id}: {price} ₽")
        else:
            print(f"Товар {wb_id}: не найден")

if __name__ == "__main__":
    main()
