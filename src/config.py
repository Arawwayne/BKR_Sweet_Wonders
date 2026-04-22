import os
import sys
from dotenv import load_dotenv
from pathlib import Path


def resource_path(relative_path):
    """Получить путь к файлу, работает и в .py и в .exe"""
    try:
        # PyInstaller создает временную папку и хранит путь в _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

# Загрузка .env файла
env_path = resource_path('.env')
load_dotenv(dotenv_path=env_path)

SERVER_HOST = os.getenv("SERVER_HOST")
SERVER_PORT = os.getenv("SERVER_PORT")