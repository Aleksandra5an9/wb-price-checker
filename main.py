import requests

WB_IDS = ["260800583", "260897865"]

def get_price(wb_id):
    url = f"https://search.wb.ru/exactmatch/ru/common/v4/search?query={wb_id}&resultset=catalog"
    response = requests.get(url)
    print(f"\nОтвет от поиска для {wb_id}: {response.status_code}")

    try:
        data = response.json()
        products = data.get("data", {}).get("products", [])
        if not products:
            print(f"Товар {wb_id} не найден.")
            return None
        product = products[0]
        name = product.get("name")
        price = product.get("salePriceU", 0) // 100
        print(f"Найдено: {name}, цена: {price} ₽")
        return price
    except Exception as e:
        print(f"Ошибка при обработке данных для {wb_id}: {e}")
        return None

for wb_id in WB_IDS:
    get_price(wb_id)
