from api_client import APIClient
from config import SERVER_HOST, SERVER_PORT

client  = APIClient(f"http://{SERVER_HOST}:{SERVER_PORT}")

# ТОВАРЫ
def get_products(): 
    return client.get("/admin/products")

def get_product(products, id):
    return next((p for p in products if p['id'] == id), None)

def post_product(data):
    return client.post_data("/admin/products/add", data=data)

def put_product(data):
    return client.put_data("/admin/products/update", data=data)


# КАТЕГОРИИ
def get_categories(): 
    return client.get("/admin/categories")

def get_category(categories, id):
    return next((c for c in categories if c['id'] == id), None)

def post_category(data):
    return client.post_json("/admin/categories/add", data=data)

def put_category(data):
    return client.put_json(f"/admin/categories/update", data=data)


# ЗАКАЗЫ (Получить все заказы, доступные сотруднику)
def get_emp_orders(employee_id):
    return client.get(f"/admin/orders/{employee_id}")

def get_order(orders, id):
    return next((o for o in orders if o['id'] == id), None)

# Изменить статус заказа
def put_order_update(data):
    return client.put_json("/admin/orders/update", data=data)


# СОТРУДНИКИ
def get_employees():
    return client.get("/admin/employees")

def get_employee(employee_id):
    return client.get(f"/admin/employees/{employee_id}")

def post_employee_auth(data):
    return client.post_json("/admin/employees/authenticate", data=data)

def post_employee(data):
    return client.post_json("/admin/employees/add", data=data)

def put_employee(employee_id, data):
    return client.put_json(f"/admin/employees/update/{employee_id}", data=data)

def del_employee(employee_id):
    return client.delete(f"/admin/employees/delete/{employee_id}")


#Филиалы
def get_branches():
    return client.get(f"/admin/branches")

def post_branch(data):
    return client.post_json(f'/admin/branches/add', data=data)

def put_branch(data):
    return client.put_json(f'/admin/branches/update', data=data)
