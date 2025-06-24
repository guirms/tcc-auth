# from flask import Flask, redirect, request, session
# import requests
# import os
# import urllib.parse

# app = Flask(__name__)
# app.secret_key = os.urandom(24)

# CLIENT_ID = "328734257891-nl2hr9p1qpp5np1u9tc6odn6av5l58fp.apps.googleusercontent.com"
# CLIENT_SECRET = "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"
# REDIRECT_URI = "http://localhost:5000/oauth/callback"
# GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
# GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
# GOOGLE_USERINFO_URL = "https://openidconnect.googleapis.com/v1/userinfo"

# @app.route('/')
# def home():
#     # Redireciona para o Google com parâmetros OAuth
#     redirect_uri_param = request.args.get("next", "http://localhost:5000/profile")
#     session["next"] = redirect_uri_param  # VULNERÁVEL: salva o redirecionamento sem validar
#     auth_url = (
#         f"{GOOGLE_AUTH_URL}?response_type=code"
#         f"&client_id={CLIENT_ID}"
#         f"&redirect_uri={REDIRECT_URI}"
#         f"&scope=openid%20email%20profile"
#         f"&access_type=offline"
#         f"&prompt=consent"
#     )
#     return redirect(auth_url)

# @app.route('/oauth/callback')
# def oauth_callback():
#     code = request.args.get("code")
#     if not code:
#         return "Código não fornecido", 400

#     data = {
#         'code': code,
#         'client_id': CLIENT_ID,
#         'client_secret': CLIENT_SECRET,
#         'redirect_uri': REDIRECT_URI,
#         'grant_type': 'authorization_code'
#     }

#     token_response = requests.post(GOOGLE_TOKEN_URL, data=data)
#     token_json = token_response.json()
#     access_token = token_json.get("access_token")

#     if not access_token:
#         return "Falha ao obter o token de acesso", 400

#     # Faz requisição para obter dados do usuário
#     headers = {"Authorization": f"Bearer {access_token}"}
#     userinfo_response = requests.get(GOOGLE_USERINFO_URL, headers=headers)
#     userinfo = userinfo_response.json()

#     # VULNERABILIDADE DE OPEN REDIRECT
#     unsafe_redirect = session.get("next", "/profile")
#     return redirect(f"{unsafe_redirect}?access_token={access_token}")

# @app.route('/profile')
# def profile():
#     return "Usuário autenticado com sucesso."

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, redirect, request, session
import requests
import os
from urllib.parse import urlparse

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Credenciais do projeto OAuth
CLIENT_ID = "328734257891-nl2hr9p1qpp5np1u9tc6odn6av5l58fp.apps.googleusercontent.com"
CLIENT_SECRET = "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"
REDIRECT_URI = "http://localhost:5000/oauth/callback"

# URLs do Google
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://openidconnect.googleapis.com/v1/userinfo"

# Domínios e hosts permitidos para redirecionamento
ALLOWED_HOSTS = ["localhost:4000", "127.0.0.1:4000"]

def is_safe_redirect(url):
    """Verifica se o redirecionamento é seguro (interno ou para host autorizado)."""
    parsed = urlparse(url)
    return not parsed.netloc or parsed.netloc in ALLOWED_HOSTS

@app.route('/')
def home():
    # Parâmetro `next` para redirecionamento após login
    next_url = request.args.get("next", "/profile")
    session["next"] = next_url  # Armazena na sessão
    # Constrói a URL de autenticação com o Google
    auth_url = (
        f"{GOOGLE_AUTH_URL}?response_type=code"
        f"&client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope=openid%20email%20profile"
        f"&access_type=offline"
        f"&prompt=consent"
    )
    return redirect(auth_url)

@app.route('/oauth/callback')
def oauth_callback():
    # Recebe o código de autorização
    code = request.args.get("code")
    if not code:
        return "Código de autorização ausente.", 400

    # Troca código por access_token
    data = {
        'code': code,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI,
        'grant_type': 'authorization_code'
    }

    token_response = requests.post(GOOGLE_TOKEN_URL, data=data)
    token_json = token_response.json()
    access_token = token_json.get("access_token")

    if not access_token:
        return "Falha ao obter token de acesso.", 400

    # Obtém dados do usuário autenticado
    headers = {"Authorization": f"Bearer {access_token}"}
    userinfo_response = requests.get(GOOGLE_USERINFO_URL, headers=headers)
    userinfo = userinfo_response.json()

    # Redirecionamento pós-login (validado)
    redirect_url = session.get("next", "/profile")
    if is_safe_redirect(redirect_url):
        return redirect(redirect_url)  # redirecionamento seguro
    else:
        return redirect("/profile")  # fallback seguro

@app.route('/profile')
def profile():
    return "Login realizado com sucesso. Esta é a área protegida."

if __name__ == '__main__':
    app.run(debug=True)



# http://localhost:5000/?next=http://localhost:8000/captura
