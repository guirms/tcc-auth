import hashlib

username = "admin"
realm = "Authentication Required"
nonce = "061ff5ec60ed922462b90973fee53a3d"
uri = "/"
method = "GET"
target_response = "9a925a9dcf754e75844694f00870e3b7"

# Dicionário simples (ou você pode usar um arquivo tipo rockyou.txt)
passwords = ["admin", "123456", "password", "123", "letmein", "root"]
print('a')

for password in passwords:
    ha1 = hashlib.md5(f"{username}:{realm}:{password}".encode()).hexdigest()
    ha2 = hashlib.md5(f"{method}:{uri}".encode()).hexdigest()
    response = hashlib.md5(f"{ha1}:{nonce}:{ha2}".encode()).hexdigest()

    if response == target_response:
        print(f"[+] Senha encontrada: SenhaValida")
        break
    else:
        print(f"[-] Tentativa falhou: {password} -> {response}")
