# CRM | Dashboard Gerencial (Omie)

Dashboard em **Streamlit** para acompanhamento gerencial de oportunidades ativas do CRM da Omie.

## Status atual do projeto

O projeto está em um **MVP funcional** (não apenas estrutura inicial). Hoje a aplicação já:

- Integra com 4 endpoints da API Omie CRM:
  - `ListarOportunidades`
  - `ListarFases`
  - `ListarUsuarios`
  - `ListarContas`
- Faz paginação automática para oportunidades e contas.
- Consolida os dados em um dataset único com `pandas`.
- Calcula indicadores derivados, como:
  - `dias_inatividade`
  - `ticket_total`
- Exibe visão gerencial com:
  - KPIs principais
  - gráficos por fase, vendedor e inatividade
  - tabela de oportunidades críticas
- Permite filtros globais por:
  - período (`dtAlteracao`)
  - vendedor
  - fase
  - faixa de inatividade
  - busca textual por conta/oportunidade
- Permite exportar **CSV filtrado** e recarregar os dados limpando cache.

## Stack

- Python 3
- Streamlit
- pandas
- requests

## Estrutura do repositório

- `main.py`: aplicação completa (coleta da API, transformação, métricas, filtros e interface).
- `README.md`: documentação do projeto.

## Como executar localmente

### 1) Instale dependências

```bash
pip install streamlit pandas requests
```

### 2) Configure credenciais da Omie

Crie o arquivo `.streamlit/secrets.toml`:

```toml
app_key = "SUA_APP_KEY"
app_secret = "SUA_APP_SECRET"
```

### 3) Rode o dashboard

```bash
streamlit run main.py
```

## Como o app está organizado

### Camada de coleta (com cache)

As funções abaixo usam `@st.cache_data` para reduzir chamadas repetidas à API:

- `get_opportunities()`
- `get_fases()`
- `get_usuario()`
- `get_contas()`
- `build_dataset()`

### Camada de transformação

- Normalização de JSON com `pd.json_normalize`.
- Renomeação e seleção de colunas relevantes.
- Conversão de tipos numéricos e datas.
- Enriquecimento por `merge` entre oportunidades, fases, usuários e contas.

### Camada de visualização

- **Sidebar** com filtros globais.
- **Tab "Visão Geral"** com KPIs, gráficos e lista de oportunidades críticas.
- **Tab "Base"** com seleção dinâmica de colunas e tabela detalhada.

## Limitações conhecidas

- Não há suíte de testes automatizados no repositório neste momento.
- O projeto está em arquivo único (`main.py`), ainda sem modularização por camadas/pacotes.
- Dependência direta de credenciais válidas da API Omie para execução completa.

## Próximos passos recomendados

- Modularizar código em pacotes (`api/`, `services/`, `ui/`).
- Adicionar tratamento de erros por endpoint com mensagens amigáveis na UI.
- Criar testes unitários para transformação de dados e métricas.
- Incluir visualizações adicionais (ex.: evolução temporal de ticket e volume).
- Configurar lint/format e CI (ex.: `ruff`, `black`, GitHub Actions).
