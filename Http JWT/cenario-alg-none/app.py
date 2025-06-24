from flask import Flask, request, jsonify
import jwt

app = Flask(__name__)
app.secret_key = 'segredo123'

# ✅ Endpoint protegido
@app.route('/protegido')
def protegido():
    auth_header = request.headers.get('Authorization')

    if not auth_header:
        return jsonify({'erro': 'Token não fornecido'}), 401

    token = auth_header.split()[1]

    try:
        # ⚠️ AQUI está o erro: allow algorithms sem filtrar explicitamente
        payload = jwt.decode(token, app.secret_key, options={"verify_signature": False})
        return jsonify({'mensagem': 'Acesso autorizado', 'usuario': payload.get('name'), 'admin': payload.get('admin')})
    except Exception as e:
        return jsonify({'erro': 'Token inválido', 'detalhes': str(e)}), 401

if __name__ == '__main__':
    app.run(debug=True)
