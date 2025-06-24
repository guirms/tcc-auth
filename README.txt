# 🛡️ Métodos de Autenticação de Login em Aplicações Web

Este repositório contém o código-fonte e os experimentos realizados no Trabalho de Conclusão de Curso (TCC) intitulado **"Métodos de Autenticação de Login em Aplicações Web: uma análise de segurança"**, desenvolvido por Bruna Savi e Guilherme Machado Santana, sob orientação do professor Rodrigo Cesar Nunes Maciel.

## 🎯 Objetivo

Analisar e comparar diferentes métodos de autenticação utilizados em aplicações web, destacando suas vulnerabilidades, pontos fortes e limitações de acordo com práticas seguras de desenvolvimento e as diretrizes da OWASP.

## 🔐 Métodos de Autenticação Implementados

Cada método foi implementado em uma API REST utilizando Python com o microframework Flask:

- **HTTP Basic Authentication**
- **HTTP Digest Authentication**
- **Autenticação baseada em Sessão (Cookies)**
- **JSON Web Token (JWT)**
- **OAuth 2.0 com provedor Google**

## 🧪 Estrutura de Testes

Cada método foi submetido a testes de segurança controlados, incluindo:
- Captura de credenciais via Wireshark
- Ataques XSS e roubo de cookies (session hijacking)
- Manipulação e falsificação de JWT
- Exploração de falhas em redirecionamentos (Open Redirect)
- Simulações de CSRF no OAuth 2.0

Os testes foram realizados **intencionalmente em ambiente HTTP**, para permitir a interceptação do tráfego.

## 🧰 Tecnologias Utilizadas

- [Python](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/)
- [Postman](https://www.postman.com/)
- [Wireshark](https://www.wireshark.org/)
- [Burp Suite Community Edition](https://portswigger.net/burp)
- [Google Chrome / Opera GX (para testes de navegador)]
- [Google Authenticator](https://support.google.com/accounts/answer/1066447?hl=pt-BR)