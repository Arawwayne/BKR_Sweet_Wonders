import os
import sys
from dotenv import load_dotenv

def get_base_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

base_dir = get_base_path()
env_path = os.path.join(base_dir, '.env')
load_dotenv(dotenv_path=env_path)

SERVER_HOST = os.getenv("SERVER_HOST")
SERVER_PORT = os.getenv("SERVER_PORT")