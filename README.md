Desafio: API Bancária Assíncrona com FastAPI

Este repositório descreve um desafio para implementar uma API RESTful bancária assíncrona utilizando FastAPI, com autenticação JWT, cadastro de transações e geração de extrato.

🎯 Objetivo

Criar uma aplicação backend moderna, segura e eficiente capaz de:

Registrar transações bancárias (depósitos e saques).

Exibir o extrato de uma conta corrente.

Utilizar JWT para autenticação.

Empregar o modelo assíncrono do FastAPI.

📌 Funcionalidades Requeridas

1. Cadastro de Transações

Implementar endpoint para depósitos.

Implementar endpoint para saques.

Somente valores positivos são permitidos.

Para saques, validar se há saldo disponível.

2. Exibição de Extrato

Retornar todas as transações associadas a uma conta corrente.

Incluir detalhes da operação, valor, data e tipo (depósito/saque).

3. Autenticação com JWT

Implementar login que retorne um token JWT.

Proteger endpoints sensíveis.

🛠️ Requisitos Técnicos

Framework

FastAPI (obrigatório)

Operações assíncronas (async def)

Modelagem de Dados

Entidade ContaCorrente (One-to-Many com transações)

Entidade Transacao (valor, tipo, timestamp, id da conta)

Banco de dados pode ser SQLAlchemy (sync) ou encode/databases (async)

Regras de Negócio

Não permitir valores negativos.

Não permitir saque sem saldo.

Segurança

Implementação de autenticação JWT.

Endpoints protegidos devem exigir token válido.

📂 Estrutura Sugerida do Projeto

project/
├── app/
│   ├── main.py
│   ├── models/
│   │   ├── conta.py
│   │   └── transacao.py
│   ├── routers/
│   │   ├── auth.py
│   │   ├── transacoes.py
│   │   └── extrato.py
│   ├── core/
│   │   ├── security.py
│   │   └── config.py
│   └── database.py
└── README.md

🚀 Entregáveis

Você deve entregar:

Código funcional da API.

Arquivo README.md com instruções de uso.

Exemplos de requisições (via cURL, HTTPie ou docs do Swagger).

Script de inicialização (opcional): Dockerfile ou docker-compose.

📎 Observações

Sinta-se livre para melhorar o desafio.

Boa organização de código e testes são bem-vindos.

Pode usar qualquer banco (SQLite, PostgreSQL etc.).

Boa sorte e divirta-se construindo sua API! 🚀


