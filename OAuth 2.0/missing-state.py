from flask import Flask, redirect, request, session
import requests
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Substitua com suas credenciais do Google Cloud
CLIENT_ID = "328734257891-nl2hr9p1qpp5np1u9tc6odn6av5l58fp.apps.googleusercontent.com"
CLIENT_SECRET = "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"
REDIRECT_URI = "http://localhost:5000/oauth/callback"

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://openidconnect.googleapis.com/v1/userinfo"

@app.route("/")
def home():
    email = session.get("email")
    if email:
        return f"<h1>Logado como {email}</h1><a href='/logout'>Logout</a>"
    return "<a href='/login'>Entrar com Google</a>"

@app.route("/login")
def login():
    auth_url = (
        f"{GOOGLE_AUTH_URL}?response_type=code"
        f"&client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope=openid%20email"
        # ⚠️ intencionalmente sem o parâmetro state
    )
    return redirect(auth_url)

@app.route("/oauth/callback")
def callback():
    code = request.args.get("code")

    # Troca o code pelo access token
    token_response = requests.post(GOOGLE_TOKEN_URL, data={
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code"
    }, verify=False).json()

    access_token = token_response.get("access_token")
    id_token = token_response.get("id_token")

    # Consulta os dados do usuário
    userinfo = requests.get(
    GOOGLE_USERINFO_URL,
    headers={"Authorization": f"Bearer {access_token}"},
    verify=False  # 👈 Desativa a verificação SSL aqui também
).json()

    session["email"] = userinfo.get("email")
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

