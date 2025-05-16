from flask import Flask, request, session, redirect, url_for, render_template_string
import pyotp
import qrcode
import io
import base64

app = Flask(__name__)
app.secret_key = 'chave-super-secreta'

# Usuário simulado
fake_user = {
    "username": "admin",
    "password": "admin123",  # Em produção: nunca guardar senhas em texto puro
    "otp_secret": pyotp.random_base32()  # Gerado apenas uma vez e salvo no banco
}

@app.route('/')
def home():
    if session.get("authenticated"):
        return "<h1>Acesso autorizado ✅</h1>"
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    html = '''
    <form method="POST">
        Usuário: <input name="username"><br>
        Senha: <input type="password" name="password"><br>
        <button type="submit">Login</button>
    </form>
    '''
    if request.method == 'POST':
        if request.form['username'] == fake_user['username'] and request.form['password'] == fake_user['password']:
            session['pre_otp'] = True  # Passou pela primeira etapa
            return redirect(url_for('otp_verify'))
        return "Credenciais inválidas"
    return html

@app.route('/otp_verify', methods=['GET', 'POST'])
def otp_verify():
    if not session.get('pre_otp'):
        return redirect(url_for('login'))

    html = '''
    <form method="POST">
        Código OTP: <input name="otp"><br>
        <button type="submit">Verificar</button>
    </form>
    '''
    if request.method == 'POST':
        otp = request.form['otp']
        totp = pyotp.TOTP(fake_user['otp_secret'])
        if totp.verify(otp):
            session.pop('pre_otp')
            session['authenticated'] = True
            return redirect(url_for('home'))
        return "Código inválido ❌"
    return html

@app.route('/qrcode')
def qr():
    totp_uri = pyotp.totp.TOTP(fake_user['otp_secret']).provisioning_uri(name=fake_user['username'], issuer_name="TCC-Login-Seguro")
    img = qrcode.make(totp_uri)
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    base64_img = base64.b64encode(buf.getvalue()).decode()
    return f'<img src="data:image/png;base64,{base64_img}">'

if __name__ == '__main__':
    app.run(debug=True)
