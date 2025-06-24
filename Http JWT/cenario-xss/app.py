from flask import Flask, render_template, request
import jwt
import datetime
import json

app = Flask(__name__)
app.secret_key = 'chave-secreta'

@app.route('/login')
def login():
    # Gera o JWT
    payload = {
        'user': 'admin',
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
    }
    token = jwt.encode(payload, app.secret_key, algorithm='HS256')
    return render_template('login.html', token=token)

@app.route('/refletido')
def refletido():
    # Pega parâmetro da URL: /refletido?msg=<script>...</script>
    msg = request.args.get('msg', '')
    return render_template('refletido.html', msg=msg)

@app.route('/coletar', methods=['POST'])
def coletar():
    # Endpoint que simula o servidor externo para capturar o token
    data = request.get_json()
    print(f"[!] TOKEN ROUBADO: {data.get('token')}")
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
