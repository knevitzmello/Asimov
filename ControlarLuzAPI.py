import requests

class ControlarLuzAPI:
    def __init__(self):
        self.headers = {'Content-Type': 'application/json'}
        self.webhook_url = 'http://192.168.0.235:8123/api/webhook/controlar_luz'
        
    def enviar_webhook(self, comando, area):
        print(self.webhook_url)
        payload = {
            "estado": comando,
            "area": area
        }
        print(f"Enviando comando para webhook: {payload}")
        try:
            # Enviar requisição POST ao webhook
            response = requests.post(self.webhook_url, json=payload, headers=self.headers)
            if response.status_code == 200:
                print(f"Webhook enviado com sucesso:\n comando = {comando} \n area = {area}")
            else:
                print(f"Erro ao enviar webhook: {response.status_code}, {response.text}")
        except Exception as e:
            print(f"Erro ao conectar ao webhook: {e}")

    def ligar_luz(self, area):
        """Liga a luz em uma área específica."""
        self.enviar_webhook("ligar", area)

    def desligar_luz(self, area):
        """Desliga a luz em uma área específica."""
        self.enviar_webhook("desligar", area)
