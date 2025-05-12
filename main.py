import requests

def get_real_price(nmID):
    url = f'https://card.wb.ru/cards/detail?nm={nmID}'
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Ошибка при запросе: {response.status_code}")
        return

    try:
        data = response.json()
        products = data.get('data', {}).get('products', [])
        if not products:
            print(f"Товар с nmID {nmID} не найден на сайте.")
            return

        product = products[0]
        price = product['priceU'] / 100
        sale_price = product['salePriceU'] / 100
        discount = product.get('discount', round((1 - sale_price / price) * 100))

        print(f"Арт: {nmID}")
        print(f"Цена без скидки: {price:.2f} ₽")
        print(f"Цена со скидкой: {sale_price:.2f} ₽")
        print(f"Итоговая скидка: {discount}%")
    except Exception as e:
        print("Ошибка обработки данных:", e)

# Пример
get_real_price(260800583)
