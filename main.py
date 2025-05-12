import requests

def get_real_price(nmID):
    url = f'https://card.wb.ru/cards/detail?nm={nmID}'
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Ошибка при запросе: {response.status_code}")
        return

    try:
        data = response.json()
        # Проверяем, что список products не пуст
        products = data['data']['products']
        if not products:
            print("Продукты не найдены.")
            return
        
        product = products[0]
        price = product['priceU'] / 100
        sale_price = product['salePriceU'] / 100
        discount = product.get('discount', round((1 - sale_price / price) * 100))
        
        print(f"Арт: {nmID}")
        print(f"Цена без скидки: {price:.2f} ₽")
        print(f"Цена со скидкой: {sale_price:.2f} ₽")
        print(f"Итоговая скидка: {discount}%")
    except (KeyError, ValueError) as e:
        print("Ошибка в структуре данных:", e)

# Пример использования
get_real_price(260800583)
