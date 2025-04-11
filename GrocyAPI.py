import requests

class GrocyAPI:
    def __init__(self, base_url, api_key, home_assistant_webhook_url_grocy):

        self.base_url = base_url.rstrip('/')  # Remove barra final, se existir
        self.headers = {
            'GROCY-API-KEY': api_key,
            'Content-Type': 'application/json'
        }
        self.base_url = home_assistant_webhook_url_grocy

    def add_shopping_list_item(self, note):
        url = f"{self.base_url}/shopping_list"
        data = {"note": note, "row_created_timestamp": None}
        return self._post_request(url, data)

    def add_task(self, task_name, due_date=None):
        url = f"{self.base_url}/tasks"
        data = {"name": task_name, "due_date": due_date, "row_created_timestamp": None}
        return self._post_request(url, data)

    def get_shopping_list(self):
        url = f"{self.base_url}/shopping_list"
        return self._get_request(url)

    def get_tasks(self):
        url = f"{self.base_url}/tasks"
        return self._get_request(url)

    def _get_request(self, url):
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição GET para {url}: {e}")
            return None

    def _post_request(self, url, data):
        try:
            response = requests.post(url, headers=self.headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição POST para {url}: {e}")
            return None
