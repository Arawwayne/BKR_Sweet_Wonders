import os
import httpx

API_BASE_URL = "http://127.0.0.1:8000"


def fetch_all_products():
    response = httpx.get(
        f"{API_BASE_URL}/admin/products",
        timeout=10
    )
    response.raise_for_status()
    return response.json()


def upload_product_image(image_path: str):
    file_handle = None

    try:
        filename = os.path.basename(image_path)
        file_handle = open(image_path, "rb")

        files = {
            "image_file": (filename, file_handle, "application/octet-stream")
        }

        response = httpx.post(
            f"{API_BASE_URL}/admin/products/upload-image",
            files=files,
            timeout=20
        )

        try:
            result = response.json()
        except Exception:
            result = {"message": "Сервер вернул некорректный ответ"}

        if response.status_code != 200:
            raise Exception(result.get("message", "Неизвестная ошибка сервера"))

        return result["image_url"]

    except httpx.RequestError as e:
        raise Exception(f"Ошибка подключения к серверу: {str(e)}")

    finally:
        if file_handle is not None:
            file_handle.close()


def add_product(
    name: str,
    category_id: int | None,
    sale_price: float,
    cost_price: float,
    composition: str | None,
    description: str | None,
    calories: int | None,
    protein: float | None,
    fat: float | None,
    carbs: float | None,
    weight: int | None,
    is_visible: bool,
    image_url: str | None,
):
    json_data = {
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
        "image_url": image_url,
        "is_visible": is_visible,
    }

    try:
        response = httpx.post(
            f"{API_BASE_URL}/admin/products/add",
            json=json_data,
            timeout=20
        )

        try:
            result = response.json()
        except Exception:
            result = {"message": "Сервер вернул некорректный ответ"}

        if response.status_code != 200:
            raise Exception(result.get("message", "Неизвестная ошибка сервера"))

        return result

    except httpx.RequestError as e:
        raise Exception(f"Ошибка подключения к серверу: {str(e)}")


def update_product(
    product_id: int,
    name: str,
    category_id: int | None,
    sale_price: float,
    cost_price: float,
    composition: str | None,
    description: str | None,
    calories: int | None,
    protein: float | None,
    fat: float | None,
    carbs: float | None,
    weight: int | None,
    is_visible: bool,
    image_url: str | None,
):
    json_data = {
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
        "image_url": image_url,
        "is_visible": is_visible,
    }

    try:
        response = httpx.put(
            f"{API_BASE_URL}/admin/products/update",
            json=json_data,
            timeout=20
        )

        try:
            result = response.json()
        except Exception:
            result = {"message": "Сервер вернул некорректный ответ"}

        if response.status_code != 200:
            raise Exception(result.get("message", "Неизвестная ошибка сервера"))

        return result

    except httpx.RequestError as e:
        raise Exception(f"Ошибка подключения к серверу: {str(e)}")