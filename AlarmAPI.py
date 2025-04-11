import requests

class AlarmAPI:
    def __init__(self):
        self.headers = {'Content-Type': 'application/json'}
        self.webhook_url = 'http://192.168.0.235:8123/api/webhook/criar_alarme'
        
    def criar_alarme(self, parametros):
        if "despertador" in parametros:
            dados = {
                "acao": "set_despertador",
                "horario": parametros["despertador"]
            }
        else:
            print("Parâmetro 'despertador' não encontrado.")
            return

        print(self.webhook_url)
        print(f"Enviando comando para webhook: {dados}")
        try:
            response = requests.post(self.webhook_url, json=dados, headers=self.headers)
            if response.status_code == 200:
                print(f"Webhook enviado com sucesso: {dados}")
            else:
                print(f"Erro ao enviar webhook: {response.status_code}, {response.text}")
        except Exception as e:
            print(f"Erro ao conectar ao webhook: {e}")

    def criar_despertador(self, parametros):
        if parametros == None:
            return 0
        dados = {
            "tipo": "despertador",
            "horario": parametros
        }
        print(self.webhook_url)
        print(f"Enviando comando para webhook: {dados}")
        try:
            response = requests.post(self.webhook_url, json=dados, headers=self.headers)
            if response.status_code == 200:
                print(f"Webhook enviado com sucesso: {dados}")
            else:
                print(f"Erro ao enviar webhook: {response.status_code}, {response.text}")
        except Exception as e:
            print(f"Erro ao conectar ao webhook: {e}")
    
    def set_horadedormir(self, parametros):
        if parametros == None:
            return 0
        dados = {
            "tipo": "dormir",
            "horario": parametros
        }
        print(self.webhook_url)
        print(f"Enviando comando para webhook: {dados}")
        try:
            response = requests.post(self.webhook_url, json=dados, headers=self.headers)
            if response.status_code == 200:
                print(f"Webhook enviado com sucesso: {dados}")
            else:
                print(f"Erro ao enviar webhook: {response.status_code}, {response.text}")
        except Exception as e:
            print(f"Erro ao conectar ao webhook: {e}")