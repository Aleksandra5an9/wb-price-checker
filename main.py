import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")

url = "https://discounts-prices-api.wildberries.ru/api/v2/list/goods/filter"
headers = {
    "Authorization": f"Bearer {API_KEY}"
}
params = {
    "filterNmID": 260800583,
    "limit": 1
}

response = requests.get(url, headers=headers, params=params)

print(f"Status code: {response.status_code}")
print("Response:", response.json())
