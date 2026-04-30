# Changelog

Todas as mudanças relevantes do projeto **Jujoo Sorveteria**.

Este arquivo foi consolidado a partir do histórico de commits do repositório.

## [1.3.0] - 2026-04-26

### Added
- Refinamento visual amplo do `frontend.html`, com melhorias de UI/UX para operação diária.
- Ajustes de acessibilidade e responsividade para melhor uso em mobile, tablet e desktop pequeno.

### Changed
- Evolução da navegação, tipografia, áreas de toque, espaçamentos e distribuição de blocos da interface.
- Ajustes de estados visuais (hover/focus) e legibilidade dos cards de produtos.

### Commits
- `3c4e49e` - style: improve frontend design and accessibility
- `c5578f9` - style: enhance frontend layout and responsiveness

---

## [1.2.0] - 2026-04-26

### Added
- Frontend operacional expandido em `frontend.html` com fluxo integrado de:
  - cadastro/edição de produtos e receita;
  - produção com consumo de matérias-primas;
  - estoque, vendas, compras, caixa e relatórios.
- Configurações de deploy e ambiente:
  - `.env.example`
  - `Dockerfile`
  - `.dockerignore`
- Dados iniciais nos JSONs de `src/data` para uso imediato.

### Changed
- Ajustes de rotas/modelos/serviços para suportar receita no produto e produção baseada em receita.
- Melhorias no repositório de persistência em arquivo (`ArquivoRepositorio`) com campos de data e robustez de gravação.
- Atualização do `README.md` na época para refletir deploy e execução.

### Commits
- `169635d` - feat: add initial product and sales data to JSON files

---

## [1.1.1] - 2026-04-26

### Changed
- Atualização de dependências em `requirements.txt`.

### Commits
- `af65d6e` - as

---

## [1.1.0] - 2026-04-26

### Added
- Primeira versão funcional da API FastAPI com módulos de:
  - produtos;
  - estoque;
  - vendas;
  - compras;
  - produção;
  - caixa;
  - relatórios;
  - monitoramento.
- Estrutura em camadas com `routes`, `services`, `models` e `repositories`.
- Persistência local em JSON dentro de `src/data`.
- Mock de pagamento e emissão de NFC-e.
- Testes unitários e integrados.

### Commits
- `31fded4` - Commit Inicial - Projeto Jujoo

---

## [1.0.0] - 2026-04-26

### Added
- Criação inicial do projeto e documentação base.

### Commits
- `75e0795` - first commit
## Unreleased

- Rodada 4: Documentação e Governança
  - Adicionado guia de QA/CI, CI/Repo governance, migração API entre as Rodadas, e checklist de validação.
  - Criação workflow CI básico (.github/workflows/ci.yml) para execução de testes em PRs e push.
