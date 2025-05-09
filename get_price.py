import requests

def get_wb_price(nm_id):
    url = f"https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&nm={nm_id}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Ошибка: {response.status_code}")
        return None

    data = response.json()
    try:
        product = data['data']['products'][0]
        price = product['priceU'] / 100
        sale_price = product['salePriceU'] / 100
        return {
            "name": product['name'],
            "brand": product['brand'],
            "price": price,
            "sale_price": sale_price
        }
    except (KeyError, IndexError):
        print("Товар не найден или структура изменилась")
        return None

if __name__ == "__main__":
    nm_id = 14922440
    result = get_wb_price(nm_id)
    print(result)
