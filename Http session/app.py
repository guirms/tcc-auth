from flask import Flask, render_template_string, request, send_file, session, jsonify, make_response
from flask_session import Session

app = Flask(__name__)
app.config["SECRET_KEY"] = "segredo-super-seguro"
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# SAMESITE = STRICT
# @app.route("/")
# def index():
#     username = request.args.get("name", "Visitante")
    
#     # Cookie vulnerável: sem HttpOnly
#     resp = make_response(render_template_string(f"""
#         <h2>Bem-vindo, {username}!</h2>
#         <p><a href="/comentario">Ver comentários</a></p>
#     """))
#     resp.set_cookie("session",
#             session.sid,
#             httponly=False,
#             samesite="Strict")  # <-- vulnerável aqui
#     return resp

# @app.route("/comentario")
# def comentario():
#     # Página com campo de comentário mal filtrado (vulnerável a XSS)
#     comentario = request.args.get("msg", "Sem comentários.")
#     return render_template_string(f"""
#         <h2>Comentários:</h2>
#         <p>{comentario}</p>
#         <hr>
#         <form method="get">
#             <input type="text" name="msg" placeholder="Deixe seu comentário">
#             <button type="submit">Enviar</button>
#         </form>
#     """)

# SAMESITE = LAX
@app.route("/")
def index():
    resp = make_response("""
        <h2>Bem-vindo</h2>
        <p><a href='/transferir'>Transferir dinheiro</a></p>
    """)
    # Cookie com SameSite configurável
    resp.set_cookie("sessionid", session.sid,
                    samesite="Lax",
                    httponly=False,# ou "Strict", ou "None"
                    secure=False)    # usar True se for https
    return resp

@app.route("/transferir", methods=["GET", "POST"])
def transferir():
    if request.method == "POST":
        return "Transferência realizada com base no cookie: " + request.cookies.get("sessionid", "sem cookie")
    return """
        <form method="post">
            <input type="submit" value="Transferir R$1000">
        </form>
    """


if __name__ == "__main__":
    app.run(debug=True, port=5000)