# parser.py
import requests

def get_price(wb_id):
    url = f"https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=0&nm={wb_id}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        try:
            return data['data']['products'][0]['priceU'] // 100  # Цена в рублях
        except (IndexError, KeyError):
            return None
    else:
        return None
