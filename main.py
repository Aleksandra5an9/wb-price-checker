import os
import requests

API_KEY_WB = os.getenv("API_KEY")  # Убедись, что в Railway переменная API_KEY установлена
HEADERS = {
    "Authorization": f"Bearer {API_KEY_WB}"
}
URL = "https://discounts-prices-api.wildberries.ru/api/v2/list/goods/filter"

def test_get_products(limit=10, offset=0):
    params = {
        "limit": limit,
        "offset": offset
    }
    print(f"Отправляем запрос с params: {params}")
    response = requests.get(URL, headers=HEADERS, params=params)

    print(f"Статус ответа: {response.status_code}")

    try:
        data = response.json()
        print("Ответ API:")
        print(data)
    except Exception as e:
        print("Не удалось распарсить JSON:", e)
        print("Текст ответа:")
        print(response.text)
        return

    if response.status_code != 200:
        print(f"Ошибка запроса: {response.status_code}")
        return

    if "data" in data and "products" in data["data"]:
        products = data["data"]["products"]
        if not products:
            print("Товары не найдены.")
        else:
            print(f"Найдено товаров: {len(products)}")
            for p in products:
                nm_id = p.get("nmId", "No nmId")
                name = p.get("name", "Нет названия")
                price = p.get("price") or p.get("salePriceU") or "Цена не найдена"
                if isinstance(price, int):
                    price = price / 100
                print(f"NM ID: {nm_id}, Название: {name}, Цена: {price} ₽")
    else:
        print("В ответе нет ключа 'data' или 'products'.")

if __name__ == "__main__":
    test_get_products()
