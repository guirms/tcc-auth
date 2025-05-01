from flask import Flask, request, send_file, session, jsonify, make_response
from flask_session import Session

app = Flask(__name__)

app.config["SECRET_KEY"] = "segredo-super-seguro"
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_COOKIE_HTTPONLY"] = True # Habilitar HttpOnly para cookies de sessão
Session(app)

@app.route("/sem-httponly")
def sem_httponly():
    return send_file("login-inseguro.html")

@app.route("/com-httponly")
def com_httponly():
    return send_file("login-seguro.html")

@app.route("/teste")
def verificar_cookie():
    return send_file("teste.html")

@app.route("/login-inseguro", methods=["POST"])
def login_inseguro():
    username = request.form.get("username")
    password = request.form.get("password")

    if username == "admin" and password == "123":
        session["user"] = username
        resp = make_response("Login inseguro bem-sucedido")
        # Cookie vulnerável
        resp.set_cookie(
            "session",
            session.sid,
            httponly=False,
            samesite="Strict",
            secure=False
        )
        return resp
    return "Credenciais inválidas", 401


@app.route("/login-seguro", methods=["POST"])
def login_seguro():
    username = request.form.get("username")
    password = request.form.get("password")

    if username == "admin" and password == "123":
        session["user"] = username
        resp = make_response("Login seguro bem-sucedido")
        resp.set_cookie(
            "session",
            session.sid,
            httponly=True,
            samesite="Strict",
            secure=False
        )
        return resp
    return "Credenciais inválidas", 401


@app.route("/rota-protegida", methods=["GET"])
def rota_protegida():
    if "user" in session:
        return jsonify({"mensagem": f"Acesso autorizado: {session['user']}"}), 200
    return jsonify({"erro": "Sessão inválida"}), 401

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"mensagem": "Logout realizado"}), 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)
