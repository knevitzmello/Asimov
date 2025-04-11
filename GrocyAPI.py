import requests

class GrocyAPI:
    """
    Classe para interagir com a API do Grocy, gerenciando listas de compras e tarefas.
    """
    def __init__(self, base_url, api_key, home_assistant_webhook_url_grocy):
        """
        Inicializa a classe com a URL base do Grocy e a chave da API.

        :param base_url: URL base do Grocy (ex: http://192.168.0.235:9192/api/objects).
        :param api_key: Chave de API para autenticação no Grocy.
        """
        self.base_url = base_url.rstrip('/')  # Remove barra final, se existir
        self.headers = {
            'GROCY-API-KEY': api_key,
            'Content-Type': 'application/json'
        }
        self.base_url = home_assistant_webhook_url_grocy

    def add_shopping_list_item(self, note):
        """
        Adiciona um item à lista de compras do Grocy.

        :param note: Descrição do item a ser adicionado.
        :return: Resposta da API ou None em caso de erro.
        """
        url = f"{self.base_url}/shopping_list"
        data = {"note": note, "row_created_timestamp": None}
        return self._post_request(url, data)

    def add_task(self, task_name, due_date=None):
        """
        Adiciona uma tarefa à lista de tarefas do Grocy.

        :param task_name: Nome da tarefa.
        :param due_date: Data de vencimento da tarefa (formato ISO 8601, opcional).
        :return: Resposta da API ou None em caso de erro.
        """
        url = f"{self.base_url}/tasks"
        data = {"name": task_name, "due_date": due_date, "row_created_timestamp": None}
        return self._post_request(url, data)

    def get_shopping_list(self):
        """
        Busca os itens da lista de compras do Grocy.

        :return: Lista de itens da API ou None em caso de erro.
        """
        url = f"{self.base_url}/shopping_list"
        return self._get_request(url)

    def get_tasks(self):
        """
        Busca as tarefas do Grocy.

        :return: Lista de tarefas da API ou None em caso de erro.
        """
        url = f"{self.base_url}/tasks"
        return self._get_request(url)

    def _get_request(self, url):
        """
        Método privado para realizar requisições GET à API.

        :param url: URL completa do endpoint.
        :return: Resposta JSON ou None em caso de erro.
        """
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição GET para {url}: {e}")
            return None

    def _post_request(self, url, data):
        """
        Método privado para realizar requisições POST à API.

        :param url: URL completa do endpoint.
        :param data: Dados a serem enviados na requisição.
        :return: Resposta JSON ou None em caso de erro.
        """
        try:
            response = requests.post(url, headers=self.headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição POST para {url}: {e}")
            return None
