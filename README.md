# Jujoo Sorveteria

Sistema de gestao para sorveteria com frontend web e backend FastAPI.

## Estrutura

- `frontend.html`: interface web
- `src/api`: rotas da API
- `src/services`: regras de negocio
- `src/data`: persistencia atual em arquivos JSON

## Rodando localmente

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run.py
```

Acesse:

- App: `http://localhost:8000/frontend`
- API: `http://localhost:8000/api`
- Docs: `http://localhost:8000/docs`

## Configuracao por ambiente

Copie `.env.example` e ajuste conforme o ambiente:

```bash
cp .env.example .env
```

Variaveis suportadas:

- `API_HOST`: host do servidor
- `API_PORT`: porta da aplicacao
- `PORT`: alternativa comum em plataformas de deploy
- `CORS_ORIGINS`: dominios permitidos, separados por virgula

Exemplo:

```env
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=https://app.seu-dominio.com,https://www.seu-dominio.com
```

## Deploy tradicional

O frontend agora usa a API no mesmo dominio/origem da pagina:

- frontend: `https://seu-dominio.com/frontend`
- API: `https://seu-dominio.com/api`

Isso significa que o caminho mais simples de deploy e servir tudo pela mesma aplicacao FastAPI, atras de um proxy reverso ou plataforma com HTTPS.

### Opcao 1: Docker

Build:

```bash
docker build -t jujoo-sorveteria .
```

Run:

```bash
docker run -p 8000:8000 \
  -e API_HOST=0.0.0.0 \
  -e API_PORT=8000 \
  -e CORS_ORIGINS=https://seu-dominio.com \
  jujoo-sorveteria
```

### Opcao 2: VM/VPS

Instale Python 3.12+, dependencias e execute:

```bash
API_HOST=0.0.0.0 API_PORT=8000 CORS_ORIGINS=https://seu-dominio.com python run.py
```

Depois coloque um proxy reverso na frente, como Nginx, apontando o dominio para a porta `8000`.

## Recomendacoes para producao

Hoje o sistema persiste dados em JSON dentro de `src/data`. Para um uso remoto real, o ideal e migrar para banco de dados antes de colocar usuarios de verdade.

Prioridades:

1. trocar JSON por PostgreSQL
2. adicionar autenticacao
3. restringir `CORS_ORIGINS` ao dominio real
4. configurar backup dos dados
5. colocar HTTPS no dominio
