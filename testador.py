from flask import Flask, request

app = Flask(__name__)

@app.route('/mensagem', methods=['POST'])
def receber_mensagem():
    data = request.get_json()
    texto = data.get('mensagem', '')
    print(f"mensagem recebida: {texto}")
    # Aqui você pode processar a mensagem como quiser
    return 'Recebido', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
