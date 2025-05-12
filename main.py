import os
import requests
from dotenv import load_dotenv

load_dotenv()  # Загружаем переменные из .env
API_KEY = os.getenv("API_KEY")  # Используется, если нужен Telegram

def get_wb_price(nm_id):
    url = f"https://discounts-prices-api.wildberries.ru/api/v2/list/goods/filter?limit=10&filterNmID={nm_id}"
    headers = {'Authorization': f'ApiKey {API_KEY}'}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Ошибка: {response.status_code}")
        return None

    data = response.json()
    try:
        product = data['data']['listGoods'][0]
        base_price = product['sizes'][0]['discountedPrice']  # Цена после стандартной скидки
        wb_discount = product['clubDiscount'] / 100  # Скидка WB (в процентах, делим на 100)

        # Расчет конечной цены с учетом скидки WB
        final_price = base_price * (1 - wb_discount)

        return {
            "name": product['vendorCode'],
            "base_price": base_price,
            "wb_discount": wb_discount * 100,  # Возвращаем скидку в процентах
            "final_price_with_discount": round(final_price, 2),
            "currency": product['currencyIsoCode4217']
        }
    except (KeyError, IndexError):
        print("Ошибка в данных или товар не найден")
        return None

if __name__ == "__main__":
    nm_id = 260800583  # Примерный артикул товара
    result = get_wb_price(nm_id)
    if result:
        print(result)
