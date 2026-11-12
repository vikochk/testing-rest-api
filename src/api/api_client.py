import requests


class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url
    
    def get_request(self, endpoint):
        url = f'{self.base_url}{endpoint}'
        response = requests.get(url)
        return response
    
    def post_request(self, endpoint, new_data_json):
        url = f'{self.base_url}{endpoint}'
        response = requests.post(url, json=new_data_json)
        return response