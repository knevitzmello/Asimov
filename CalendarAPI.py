import requests

class CalendarAPI():
    def __init__(self, home_assistant_webhook_url_criar_evento):
        self.webhook_url = home_assistant_webhook_url_criar_evento

    def criar_evento(self, titulo, data_inicio, data_fim):
        """Envia um webhook para o Home Assistant criar um evento no Google Calendar."""
        evento_dados = {
            "titulo": titulo,
            "data_inicio": data_inicio,
            "data_fim": data_fim,
        }

        # Enviar os dados do evento via webhook para o Home Assistant
        response = requests.post(self.webhook_url, json=evento_dados)

        if response.status_code == 200:
            print(f"Evento '{titulo}' criado com sucesso!")
        else:
            print(f"Falha ao criar o evento. Código de status: {response.status_code}")

    def process_command(self, command, parameters):
        """Implementação do método abstrato para processar comandos."""
        if command == "criar_evento":
            titulo, descricao, data_inicio, data_fim = parameters
            self.criar_evento(titulo, descricao, data_inicio, data_fim)
