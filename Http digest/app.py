from flask import Flask
from flask_httpauth import HTTPDigestAuth

app = Flask(__name__)
app.config['SECRET_KEY'] = 'chave_teste_digest'
auth = HTTPDigestAuth(realm="Authentication Required")  # compatível com o Postman

users = {
    "admin": "senha123"
}

@auth.get_password
def get_pw(username):
    return users.get(username)

@app.route('/')
@auth.login_required
def digest_view():
    return f"Bem-vindo {auth.username()}"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
