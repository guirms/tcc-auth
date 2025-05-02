from flask import Flask, request, jsonify
import jwt

app = Flask(__name__)
SECRET_KEY = "chave_super_secreta"  # simulação de chave do servidor

@app.route('/login', methods=['POST'])
def login():
    payload = {
        "user_id": 123,
        "role": "admin"
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return jsonify(token=token)

@app.route('/protegido', methods=['GET'])
def protegido():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({"erro": "Token ausente"}), 401

    token = auth_header.split(" ")[1]

    try:
        # VULNERABILIDADE: NÃO está validando o algoritmo corretamente
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256", "none"])
        return jsonify({"mensagem": f"Acesso autorizado para o usuário {payload['user_id']} com papel {payload['role']}"})
    except Exception as e:
        return jsonify({"erro": f"Token inválido: {str(e)}"}), 401

if __name__ == '__main__':
    app.run(debug=True)
