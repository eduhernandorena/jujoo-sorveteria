# Jujoo Sorveteria

Sistema de gestão para sorveteria com frontend web (arquivo único) e backend FastAPI.

O projeto foi desenhado para operação rápida no balcão/cozinha, cobrindo estoque, produtos, vendas, compras, produção, caixa e relatórios.

## Funcionalidades atuais

- **Dashboard diário**
  - Vendas do dia (valor e quantidade)
  - Saldo de caixa atual/do dia
  - Itens de estoque e alertas de estoque baixo
  - Total produzido no dia

- **Produtos**
  - CRUD de produtos
  - Categorias (`sorvete`, `picole`, `acai`, `topping`, `bebida`, `acompanhamento`)
  - Cadastro de receita por produto (matéria-prima, quantidade, unidade)
  - Catálogo com edição rápida pela própria tela

- **Estoque (matérias-primas)**
  - CRUD de matérias-primas
  - Ajuste de estoque (adicionar/remover)
  - Resumo de estoque e itens abaixo do mínimo

- **Produção**
  - Lançamento de produção com múltiplos itens
  - Consumo automático de matéria-prima via receita do produto
  - Validação de estoque insuficiente antes de confirmar produção

- **Vendas**
  - Registro de venda com itens e desconto
  - Processamento de pagamento via mock
  - Emissão de NFC-e via mock
  - Geração automática de entrada no caixa

- **Compras**
  - Registro de compras por fornecedor
  - Atualização automática de estoque
  - Geração automática de saída no caixa

- **Caixa**
  - Lançamentos manuais de entrada/saída
  - Saldo atual e saldo do dia
  - Fechamento diário e mensal por forma de pagamento

- **Relatórios**
  - Vendas, compras, lucratividade, estoque, caixa, produção e dashboard
  - Agregações por período e por forma de pagamento/fornecedor/produto

- **Monitoramento**
  - Endpoints de status e informações de recursos (`/api/monitor/status`, `/api/monitor/info`)

## Arquitetura

Arquitetura em camadas:

- **Apresentação**
  - `frontend.html`: UI completa (HTML + CSS + JS) servida pela própria API.
  - `src/api/routes/*`: endpoints HTTP por domínio.

- **Aplicação (regras de negócio)**
  - `src/services/*`: orquestra casos de uso e integra domínios (ex.: venda -> caixa + NFC-e mock).

- **Domínio / contratos**
  - `src/models/*`: modelos Pydantic de entrada/saída e entidades de negócio.

- **Persistência**
  - `src/repositories/arquivo_repo.py`: repositório genérico em JSON.
  - `src/data/*.json`: base atual de dados local.

- **Infra / utilitários**
  - `src/core/config.py`: variáveis de ambiente e caminhos.
  - `src/utils/*`: logging, helpers, monitor.
  - `src/mocks/*`: simulações de pagamento e NFC-e.

### Fluxo resumido de requisições

1. Frontend chama endpoint em `/api/...`.
2. Rota delega para o serviço correspondente.
3. Serviço aplica regras de negócio e chama repositórios/serviços auxiliares.
4. Repositório persiste em JSON.
5. Serviço retorna DTO de resposta para a rota.

## Endpoints principais

Base da API: `/api`

- `GET/POST/PUT/DELETE /produtos`
- `GET/POST/PUT/DELETE /estoque`
- `POST /estoque/{materia_id}/adicionar`
- `POST /estoque/{materia_id}/remover`
- `GET/POST /vendas`
- `GET /vendas/do-dia`
- `GET/POST /compras`
- `GET /compras/do-dia`
- `GET/POST /producao`
- `GET /producao/do-dia`
- `GET /caixa/saldo`
- `GET /caixa/movimentos`
- `POST /caixa/movimento`
- `POST /caixa/fechamento-diario`
- `POST /caixa/fechamento-mensal`
- `GET /relatorios/{vendas|compras|lucratividade|estoque|caixa|producao|dashboard}`
- `GET /monitor/{status|info}`

## Estrutura do projeto

- `frontend.html`: interface web
- `run.py`: inicialização local via Uvicorn
- `src/api`: aplicação FastAPI e rotas
- `src/services`: regras de negócio
- `src/models`: contratos/entidades
- `src/repositories`: persistência em arquivo
- `src/data`: dados JSON
- `src/mocks`: integrações simuladas
- `tests`: testes unitários e integrados
- `CHANGELOG.md`: histórico consolidado de mudanças

## Rodando localmente

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run.py
```

Acesse:

- App: `http://localhost:8000/frontend`
- API base: `http://localhost:8000/api`
- Docs: `http://localhost:8000/docs`
- Healthcheck: `http://localhost:8000/health`

## Configuração por ambiente

Copie `.env.example` e ajuste conforme o ambiente:

```bash
cp .env.example .env
```

Variáveis suportadas:

- `API_HOST`: host do servidor
- `API_PORT`: porta da aplicação
- `PORT`: fallback comum em plataformas de deploy
- `CORS_ORIGINS`: domínios permitidos, separados por vírgula

Exemplo:

```env
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=https://app.seu-dominio.com,https://www.seu-dominio.com
```

## Deploy

O frontend e a API podem ser servidos no mesmo domínio:

- Frontend: `https://seu-dominio.com/frontend`
- API: `https://seu-dominio.com/api`

### Opção 1: Docker

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

### Opção 2: VM/VPS

```bash
API_HOST=0.0.0.0 API_PORT=8000 CORS_ORIGINS=https://seu-dominio.com python run.py
```

Depois, publique com proxy reverso (ex.: Nginx) apontando para a porta `8000`.

## Rodada 1 — Configuração Segura

- Cors: CORS_ORIGINS agora exige configuração explícita; sem origens definidas, o CORS não será habilitado.
- Logging: logs terão fallback para stdout caso não seja possível escrever no arquivo de logs.
- Frontend: a rota /frontend verifica a existência de frontend.html e retorna 404 claro se não encontrado.
- Validação de entradas: validações básicas para pontos críticos (ex.: estoque) para evitar estados inválidos.
- Documentação de configuração: README atualizado com vars de ambiente esperadas (API_HOST, API_PORT, CORS_ORIGINS).

## Limitações atuais e próximos passos

Hoje a persistência é local em JSON (`src/data`). Para produção com múltiplos usuários, recomenda-se:

1. Migrar para PostgreSQL.
2. Adicionar autenticação/autorização.
3. Restringir `CORS_ORIGINS` ao domínio real.
4. Configurar backup e retenção de dados.
5. Habilitar HTTPS com certificados válidos.

## Rodada 4 — Documentação e Governança

- Guia de QA/CI: definição de padrões mínimos de qualidade, execução de testes, linting e verificação de estilo de código.
- Configuração de CI: inclusão de workflow (GitHub Actions) para rodar testes automaticamente em PRs e pushes, com relatório de falhas.
- Migração e governança de API: constar diretrizes de migração entre versões (Rodadas 2 vs 3) com compatibilidade e planos de descontinuação.
- Backup e recuperação de dados: recomendações para ambientes de produção (DB, snapshots, políticas de retenção).
- Segurança operacional: checklist de aspectos de segurança (CORS, autenticação, TLS, logs, secrets).
- Checklist de validação: lista de cenários de teste para rodadas futuras, incluindo casos de erro e limites.
- Documentação externa: links para guias de uso, exemplos de chamadas, e um changelog evolutivo com cada rodada.
