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

🧱 Estrutura Inicial do Projeto (com código)

A seguir está uma estrutura mínima funcional para iniciar o desafio.

project/
├── app/
│   ├── main.py
│   ├── database.py
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
│   └── schemas.py
└── README.md
main.py
from fastapi import FastAPI
from app.routers import auth, transacoes, extrato


app = FastAPI(title="API Bancária Assíncrona")


app.include_router(auth.router)
app.include_router(transacoes.router)
app.include_router(extrato.router)
database.py
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base


DATABASE_URL = "sqlite+aiosqlite:///./db.sqlite3"


engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)
Base = declarative_base()
Modelos: conta.py e transacao.py
from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Conta(Base):
    __tablename__ = "contas"
    id = Column(Integer, primary_key=True, index=True)
    usuario = Column(String, unique=True, index=True)
    saldo = Column(Float, default=0)


    transacoes = relationship("Transacao", back_populates="conta")


class Transacao(Base):
    __tablename__ = "transacoes"
    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String)
    valor = Column(Float)
    data = Column(DateTime, default=datetime.utcnow)
    conta_id = Column(Integer, ForeignKey("contas.id"))


    conta = relationship("Conta", back_populates="transacoes")
auth.py
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import criar_token


router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends()):
    token = criar_token({"sub": form.username})
    return {"access_token": token, "token_type": "bearer"}
security.py
from datetime import datetime, timedelta
from jose import jwt


SECRET_KEY = "changeme"
ALGORITHM = "HS256"




def criar_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=5)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)



Projeto completo — arquivos principais

Cole os arquivos nas pastas indicadas. Todos os endpoints são assíncronos e usam async.

pyproject.toml / requirements.txt
fastapi
uvicorn[standard]
SQLAlchemy
aiosqlite
alembic
python-jose[cryptography]
passlib[bcrypt]
python-dotenv
pytest
pytest-asyncio
httpx
app/main.py
from fastapi import FastAPI
from app.routers import auth, transacoes, extrato
from app.database import init_db


app = FastAPI(title="API Bancária Assíncrona")


app.include_router(auth.router)
app.include_router(transacoes.router)
app.include_router(extrato.router)


@app.on_event("startup")
async def startup():
    await init_db()
app/database.py
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import text


DATABASE_URL = "sqlite+aiosqlite:///./db.sqlite3"


engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)
Base = declarative_base()


async def init_db():
    # Cria tabelas se não existirem
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
app/models/conta.py
from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.orm import relationship
from app.database import Base


class Conta(Base):
    __tablename__ = "contas"
    id = Column(Integer, primary_key=True, index=True)
    usuario = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    saldo = Column(Float, default=0.0)


    transacoes = relationship("Transacao", back_populates="conta", cascade="all, delete-orphan")
app/models/transacao.py
from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Transacao(Base):
    __tablename__ = "transacoes"
    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String, nullable=False)  # 'deposito' ou 'saque'
    valor = Column(Float, nullable=False)
    data = Column(DateTime, default=datetime.utcnow)
    conta_id = Column(Integer, ForeignKey("contas.id"), nullable=False)


    conta = relationship("Conta", back_populates="transacoes")
app/schemas.py
from pydantic import BaseModel, Field, condecimal
from typing import List
from datetime import datetime


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ContaCreate(BaseModel):
    usuario: str
    senha: str


class ContaOut(BaseModel):
    id: int
    usuario: str
    saldo: float


    class Config:
        orm_mode = True


class TransacaoCreate(BaseModel):
    tipo: str = Field(..., regex="^(deposito|saque)$")
    valor: float = Field(..., gt=0)


class TransacaoOut(BaseModel):
    id: int
    tipo: str
    valor: float
    data: datetime


    class Config:
        orm_mode = True


class Extrato(BaseModel):
    conta: ContaOut
    transacoes: List[TransacaoOut]
app/core/config.py
from pydantic import BaseSettings


class Settings(BaseSettings):
    secret_key: str = "CHANGE_ME"
    algorithm: str = "HS256"
    access_token_expires_minutes: int = 60 * 6


    class Config:
        env_file = ".env"


settings = Settings()
app/core/security.py
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")




def hash_password(password: str) -> str:
    return pwd_context.hash(password)




def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)




def criar_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expires_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)




def verificar_token(token: str):
    return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy import select
from app.database import AsyncSessionLocal
from app.models.conta import Conta
from app.core.security import criar_token, verify_password, hash_password, verify_password as _verify
from app.schemas import Token, ContaCreate, ContaOut


router = APIRouter(prefix="/auth", tags=["Autenticação"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@router.post("/register", response_model=ContaOut)
async def register(payload: ContaCreate):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            stmt = select(Conta).where(Conta.usuario == payload.usuario)
            res = await session.execute(stmt)
            existing = res.scalar_one_or_none()
            if existing:
                raise HTTPException(status_code=400, detail="Usuário já existe")
            conta = Conta(usuario=payload.usuario, hashed_password=hash_password(payload.senha))
            session.add(conta)
            await session.flush()
            return conta


@router.post("/login", response_model=Token)
async def login(form: OAuth2PasswordRequestForm = Depends()):
    async with AsyncSessionLocal() as session:
        stmt = select(Co
                      



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
