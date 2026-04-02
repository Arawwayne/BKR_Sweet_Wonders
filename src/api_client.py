import requests, os
from config import SERVER_HOST, SERVER_PORT

class APIClient:
    def __init__(self, 
                 base_url: str,
                 ):
        
        self.base_url = base_url

    def get(self, endpoint):
        response = requests.get(f"{self.base_url}/{endpoint}")
        self._handle_errors(response)
        return response.json()


    def post_json(self, endpoint, data):
        response = requests.post(f'{self.base_url}/{endpoint}', json=data)
        self._handle_errors(response)
        return response.json()
    
    def put_json(self, endpoint, data):
        response = requests.put(f'{self.base_url}/{endpoint}', json=data)
        self._handle_errors(response)
        return response.json()
    

    def post_data(self, endpoint, data):
        files = None
        file_handle = None
        image_path = data["image_url"]
        print(image_path)
        try:
            file_handle = open(image_path, 'rb')
            files = {'image_file': file_handle}
            response = requests.post(
                f'{self.base_url}/{endpoint}',
                data=data,
                files=files
            )
            self._handle_errors(response)
            return response.json()
            
        finally:
            if file_handle:
                file_handle.close()
    
    def put_data(self, endpoint, data):
        files = None
        file_handle = None
        image_path = data["image_url"]
        print(image_path)
        try:
            file_handle = open(image_path, 'rb')
            files = {'image_file': file_handle}
            response = requests.put(
                f'{self.base_url}/{endpoint}',
                data=data,
                files=files
            )
            self._handle_errors(response)
            return response.json()
            
        finally:
            if file_handle:
                file_handle.close()

        
    
    
    def _handle_errors(self, response):
        if response.status_code != 200:
            raise Exception(f'Error: {response.status_code} — {response.text}')

if __name__ == "__main__":
    client  = APIClient(f"http://{SERVER_HOST}:{SERVER_PORT}")




        

