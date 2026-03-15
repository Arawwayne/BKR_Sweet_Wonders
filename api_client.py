import os
import httpx

API_BASE_URL = "http://127.0.0.1:8000"


def get_all_products():
    response = httpx.get(
        f"{API_BASE_URL}/admin/products",
        timeout=10
    )
    response.raise_for_status()
    return response.json()


def add_product(
    name: str,
    category_id: int,
    sale_price: float,
    cost_price: float,
    composition: str,
    description: str,
    calories: int,
    protein: float,
    fat: float,
    carbs: float,
    weight: int,
    is_visible: bool,
    image_path: str,
):
    file_handle = None

    try:
        filename = os.path.basename(image_path)
        file_handle = open(image_path, "rb")

        data = {
            "name": name,
            "category_id": category_id,
            "sale_price": sale_price,
            "cost_price": cost_price,
            "composition": composition,
            "description": description,
            "calories": calories,
            "protein": protein,
            "fat": fat,
            "carbs": carbs,
            "weight": weight,
            "is_visible": is_visible,
        }

        files = {
            "image_file": (filename, file_handle, "application/octet-stream")
        }

        response = httpx.post(
            f"{API_BASE_URL}/admin/products/add",
            data=data,
            files=files,
            timeout=20
        )

        response.raise_for_status()
        return response.json()

    finally:
        if file_handle:
            file_handle.close()


def update_product(
    product_id: int,
    name: str,
    category_id: int,
    sale_price: float,
    cost_price: float,
    composition: str,
    description: str,
    calories: int,
    protein: float,
    fat: float,
    carbs: float,
    weight: int,
    is_visible: bool,
    image_path: str | None = None,
):
    file_handle = None

    try:
        data = {
            "id": product_id,
            "name": name,
            "category_id": category_id,
            "sale_price": sale_price,
            "cost_price": cost_price,
            "composition": composition,
            "description": description,
            "calories": calories,
            "protein": protein,
            "fat": fat,
            "carbs": carbs,
            "weight": weight,
            "is_visible": is_visible,
        }

        files = None

        if image_path:
            filename = os.path.basename(image_path)
            file_handle = open(image_path, "rb")

            files = {
                "image_file": (filename, file_handle, "application/octet-stream")
            }

        response = httpx.put(
            f"{API_BASE_URL}/admin/products/update",
            data=data,
            files=files,
            timeout=20
        )

        response.raise_for_status()
        return response.json()

    finally:
        if file_handle:
            file_handle.close()