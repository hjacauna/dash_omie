# CRM | Dashboard Gerencial (Omie)

Aplicação em **Streamlit** para monitorar oportunidades ativas do CRM da Omie com visão gerencial, filtros globais e exportação de dados.

## Situação atual do projeto

O projeto está em produção técnica no formato de **MVP funcional em arquivo único** (`main.py`).

Hoje, o sistema já entrega:

- Coleta de dados na API Omie CRM usando:
  - `ListarOportunidades` (somente status `A`)
  - `ListarFases`
  - `ListarUsuarios`
  - `ListarContas`
- Paginação automática para oportunidades e contas.
- Cache de dados com `st.cache_data` (TTL de 30 ou 60 minutos, conforme endpoint).
- Enriquecimento dos dados por `merge` entre oportunidades, fases, usuários e contas.
- Cálculo de métricas derivadas:
  - `dias_inatividade`
  - `ticket_total`
- Interface de análise com:
  - KPIs (volume, ticket total, ticket médio, inatividade média e % > 30 dias)
  - gráfico de oportunidades por fase
  - gráfico de ticket por vendedor (top 10)
  - distribuição por faixas de inatividade
  - tabela de oportunidades mais críticas
- Filtros globais por período, vendedor, fase, inatividade e busca textual.
- Exportação da base filtrada para CSV.
- Botão para limpar cache e recarregar dados.

## Stack atual

- Python 3
- Streamlit
- pandas
- requests

## Estrutura do repositório

- `main.py`: lógica completa da aplicação (API, transformação de dados e UI).
- `README.md`: documentação do projeto.

## Como executar localmente

### 1) Instale as dependências

```bash
pip install streamlit pandas requests
```

### 2) Configure credenciais da Omie

Crie `.streamlit/secrets.toml` com:

```toml
app_key = "SUA_APP_KEY"
app_secret = "SUA_APP_SECRET"
```

### 3) Execute o app

```bash
streamlit run main.py
```

## Fluxo funcional implementado

### 1. Coleta (API)

Funções de coleta:

- `get_opportunities()`
- `get_fases()`
- `get_usuario()`
- `get_contas()`

### 2. Consolidação e transformação

A função `build_dataset()`:

- junta as fontes por chaves de vendedor, fase e conta;
- seleciona colunas úteis para o painel;
- padroniza tipos (número/data);
- cria `dias_inatividade` e `ticket_total`;
- preenche ausências com rótulos padrão (`Sem vendedor`, `Sem fase`, `Sem conta`).

### 3. Visualização e exploração

- Sidebar com filtros globais.
- Aba **Visão Geral** para KPIs e gráficos.
- Aba **Base** para inspeção tabular com seleção de colunas.

## Limitações atuais

- Projeto ainda monolítico (sem separação em módulos/pacotes).
- Sem suíte de testes automatizados versionada no repositório.
- Sem camada formal de logging/observabilidade.
- Dependência direta de credenciais válidas no `st.secrets`.

## Próximas melhorias recomendadas

- Modularizar em camadas (`clients`, `services`, `ui`).
- Adicionar tratamento de erro por endpoint com mensagens mais detalhadas na interface.
- Incluir testes unitários para transformação e métricas.
- Padronizar qualidade de código com lint/format (`ruff`, `black`) + CI.
- Evoluir visualizações com série temporal e comparação por períodos.
