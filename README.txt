No http digest, é necessário fazer duas requisições para logar. Na primeira, que dará 401, você deve obter os dados "realm", "nonce" e "opaque" que são retornados no header da resposta. Após isso, preencha os campos avançados do postman de forma manual. Aí funcionará.

Passo a passo para rodar
1 - cd /pasta-do-metodo
2 - venv\Scripts\activate
3 - python app.py 