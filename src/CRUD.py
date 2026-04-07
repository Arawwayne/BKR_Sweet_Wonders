from api_client import APIClient
from config import SERVER_HOST, SERVER_PORT

import json
import requests

client  = APIClient(f"http://{SERVER_HOST}:{SERVER_PORT}")

#ТОВАРЫ
def get_products(): 
    return client.get("/admin/products")

def get_product(products, id):
    return next((p for p in products if p[0] == id), None)

def post_product(data):
    return client.post_data("/admin/products/add", data=data)

def put_product(data):
    return client.put_data("/admin/products/update", data=data)


#КАТЕГОРИИ
def get_categories(): 
    return client.get("/admin/categories")

def get_category(categories, id):
    return next((c for c in categories if c[-1] == id), None)

def post_category(data):
    return client.post_json("/admin/categories/add", data=data)

def put_category(data):
    return client.put_json(f"/admin/categories/update", data=data)


#ЗАКАЗЫ (Получить все заказы, доступные сотруднику)
def get_emp_orders(employee_id):
    return client.get(f"/admin/orders/{employee_id}")

#Изменить статус заказа
def put_order_update(data):
    return client.put_json("/admin/orders/update", data=data)






def save_response_to_json(response: requests.Response, filename: str = None):
    if filename is None:
        filename = f"response1.json"
    
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
