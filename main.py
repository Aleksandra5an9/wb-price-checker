import requests

def get_product_info(nm_id):
    url = f"https://card.wb.ru/cards/v2/detail?appType=1&curr=rub&dest=-1255987&spp=30&ab_testing=false&nm={nm_id}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        print(data)  # Здесь вы можете обработать данные по вашему усмотрению
    else:
        print(f"Ошибка: {response.status_code}")

# Пример использования
get_product_info(314337853)
