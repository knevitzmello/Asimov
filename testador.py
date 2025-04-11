from GrocyAPI import GrocyAPI
import requests

def send_to_webhook(items):
    webhook_url = 'http://192.168.0.235:8123/api/webhook/notifica_lista'
    headers = {'Content-Type': 'application/json'}
    data = {'items': items}  # Monta o payload com os itens
    try:
        response = requests.post(webhook_url, json=data, headers=headers)
        response.raise_for_status()
        print("Dados enviados com sucesso.")
    except requests.exceptions.RequestException as e:
        print(f"Erro ao enviar para o webhook: {e}")