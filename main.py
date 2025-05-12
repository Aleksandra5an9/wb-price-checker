import requests

def get_real_price(nmID):
    # Правильный URL
    url = f'https://card.wb.ru/cards/detail?nm={nmID}'
    
    # Заголовки для имитации запроса с браузера
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
    }

    # Выполнение запроса с дополнительными заголовками
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Ошибка при запросе: {response.status_code}")
        return

    try:
        # Пытаемся распарсить ответ
        data = response.json()
        products = data.get('data', {}).get('products', [])

        if not products:
            print(f"Товар с nmID {nmID} не найден на сайте.")
            return

        # Извлечение данных товара
        product = products[0]
        price = product['priceU'] / 100
        sale_price = product['salePriceU'] / 100
        discount = product.get('discount', round((1 - sale_price / price) * 100))

        # Выводим информацию о товаре
        print(f"Арт: {nmID}")
        print(f"Цена без скидки: {price:.2f} ₽")
        print(f"Цена со скидкой: {sale_price:.2f} ₽")
        print(f"Итоговая скидка: {discount}%")
    except Exception as e:
        print("Ошибка обработки данных:", e)

# Пример использования
get_real_price(260800583)
