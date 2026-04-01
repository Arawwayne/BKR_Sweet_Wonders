from api_client import APIClient
from config import SERVER_HOST, SERVER_PORT

import json
import requests

client  = APIClient(f"http://{SERVER_HOST}:{SERVER_PORT}")

def get_products(): 
    return client.get("/admin/products")

def post_product(data):
    return client.post("/admin/products/add", data=data)

def put_product(data):
    return client.put(f"/admin/products/update", data=data)


def save_response_to_json(response: requests.Response, filename: str = None):
    if filename is None:
        filename = f"response.json"
    
    try:
        # Получаем JSON данные из response
        data = response
        
        # Записываем в файл с форматированием
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        print(f"Response сохранен в файл: {filename}")
        return filename
    
    except json.JSONDecodeError:
        print("Response не содержит JSON данных")
        return None

