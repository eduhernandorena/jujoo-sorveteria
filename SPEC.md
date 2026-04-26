# Jujoo Sorveteria - Sistema de Gerenciamento MVP

## 1. Visão Geral do Projeto

**Nome do Projeto:** Jujoo Sorveteria - Sistema de Gestão  
**Tipo:** API REST com interface CLI  
**Funcionalidade Principal:** Sistema completo para gerenciamento de sorveteria com controle de caixa, estoque, vendas, produção e emissão fiscal  
**Usuários Alvo:** Proprietários e funcionários de sorveterias

## 2. Especificação de Funcionalidades

### 2.1 Gestão de Caixa
- **Entrada de valores:** Registro de vendas, recebimentos diversos
- **Saída de valores:** Pagamentos de fornecedores, despesas operacionais
- **Fechamento diário:** Balanço diário com total de entradas, saídas e saldo
- **Fechamento mensal:** Relatório consolidado do mês

### 2.2 Controle de Estoque
- **Cadastro de matérias-primas:** Ingredientes utilizados
- **Controle de quantidade:** Estoque atual e mínimo
- **Baixa automática:** Descontar do estoque ao produzir/vender
- **Alerta de estoque baixo:** Notificação quando atingir nível mínimo

### 2.3 Cadastro de Produtos
- **Produtos finais:** Sorvetes, picolés, toppings, acompanhamentos
- **Receitas:** Ingredientes necessários para cada produto
- **Preços:** Custo de produção e preço de venda
- **Categorias:** Tipos de produtos

### 2.4 Lançamento de Vendas e Compras
- **Vendas:** Registro de vendas com itens, quantidade, forma pagamento
- **Compras:** Registro de compras de matérias-primas
- **Histórico:** Consulta de vendas/compras por período

### 2.5 Produção Diária
- **Registro de produção:** Quantidade produzida de cada produto
- **Baixa de matéria-prima:** Descontar ingredientes do estoque
- **Geração de saída:** Registrar produto final disponível para venda

### 2.6 Pagamentos
- **Dinheiro:** Pagamento em espécie
- **PIX:** Pagamento via chave PIX (mock)
- **Cartão:** Pagamento via cartão de crédito/débito (mock)

### 2.7 Emissão de NFCe (Mock)
- **Geração de cupom fiscal:** Simulação de NFCe
- **Dados do emitente:** Informações da sorveteria
- **Itens vendidos:** Detalhamento dos produtos
- **Totais:** Subtotal, impostos, total

### 2.8 Relatórios
- **Lucratividade:** Análise de lucro por período
- **Vendas:** Relatório de vendas por período/produto
- **Compras:** Relatório de compras por período
- **Estoque:** Situação atual do estoque

### 2.9 Logs e Monitoramento
- **Logs de operações:** Registro de todas as ações
- **Monitor de recursos:** CPU, memória, disco
- **Histórico de erros:** Registro de exceções

### 2.10 Testes
- **Testes unitários:** Testes de funções individuais
- **Testes integrados:** Testes de integração entre módulos

## 3. Arquitetura do Sistema

```
jujoo-sorveteria/
├── src/
│   ├── main.py                 # Ponto de entrada
│   ├── api/                    # API REST (FastAPI)
│   │   ├── routes/
│   │   └── main.py
│   ├── core/                   # Configurações centrais
│   │   ├── config.py
│   │   └── constants.py
│   ├── models/                 # Modelos de dados
│   │   ├── produto.py
│   │   ├── materia_prima.py
│   │   ├── venda.py
│   │   ├── compra.py
│   │   ├── producao.py
│   │   ├── caixa.py
│   │   └── nfce.py
│   ├── services/               # Lógica de negócio
│   │   ├── caixa_service.py
│   │   ├── estoque_service.py
│   │   ├── produto_service.py
│   │   ├── venda_service.py
│   │   ├── compra_service.py
│   │   ├── producao_service.py
│   │   ├── relatorio_service.py
│   │   └── nfce_service.py
│   ├── repositories/           # Persistência
│   │   └── arquivo_repo.py
│   ├── utils/                  # Utilitários
│   │   ├── logger.py
│   │   ├── monitor.py
│   │   └── helpers.py
│   └── mocks/                  # Mocks externos
│       ├── pagto_mock.py
│       └── nfce_mock.py
├── tests/
│   ├── unitarios/
│   └── integrados/
├── data/                      # Dados persistidos
├── logs/                      # Arquivos de log
└── run.py                     # Script de inicialização
```

## 4. Critérios de Aceitação

- [ ] Sistema inicia sem erros
- [ ] API responde em todas as rotas principais
- [ ] Persistência em arquivo funciona corretamente
- [ ] Gestão de caixa registra entradas e saídas
- [ ] Fechamento diário calcula corretamente
- [ ] Fechamento mensal consolida dados
- [ ] Controle de estoque atualiza corretamente
- [ ] Cadastro de produtos CRUD completo
- [ ] Lançamento de vendas funciona
- [ ] Lançamento de compras funciona
- [ ] Produção diária faz baixa de matéria-prima
- [ ] Pagamentos aceitos (dinheiro, PIX, cartão)
- [ ] NFCe mock gerado corretamente
- [ ] Relatórios retornam dados
- [ ] Logs gravados corretamente
- [ ] Monitor de recursos retorna dados
- [ ] Testes unitários passam
- [ ] Testes integrados passam