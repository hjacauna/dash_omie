# Dashboard CRM Omie

Projeto em desenvolvimento para construção de um dashboard com dados do CRM da Omie.

## Objetivo

Entregar um dashboard simples, confiável e evolutivo para acompanhamento de oportunidades comerciais no CRM da Omie, permitindo:

- Visualizar pipeline de vendas por fase.
- Acompanhar oportunidades por vendedor e conta.
- Monitorar previsões (ano/mês) e composição de ticket.
- Apoiar decisões comerciais com dados atualizados da API Omie.

## Fase atual do projeto

No estágio atual, o projeto está em **MVP técnico inicial**, com foco em integração e estruturação de dados:

- Aplicação base em **Streamlit**.
- Consumo da API Omie para:
  - `ListarOportunidades`
  - `ListarFases` (função implementada e pronta para uso).
- Transformação inicial dos dados retornados para um formato tabular com **pandas**.
- Extração de campos relevantes de oportunidades, incluindo:
  - vendedor (`nCodVendedor`)
  - conta (`nCodConta`)
  - descrição da oportunidade (`cDesOp`)
  - status/fase (`nCodStatus`)
  - previsão (`nAnoPrev`, `nMesPrev`)
  - informações de ticket (meses, produtos, recorrência e serviços)

## Tecnologias

- Python
- Streamlit
- pandas
- requests

## Estrutura atual

- `main.py`: integração com API Omie, tratamento inicial dos dados e execução da coleta de oportunidades.

## Como executar

1. Instale as dependências (exemplo):

   ```bash
   pip install streamlit pandas requests
   ```

2. Configure as credenciais da Omie no `st.secrets` (por exemplo, em `.streamlit/secrets.toml`):

   ```toml
   app_key = "SUA_APP_KEY"
   app_secret = "SUA_APP_SECRET"
   ```

3. Execute a aplicação:

   ```bash
   streamlit run main.py
   ```

## Próximos passos sugeridos

- Construir visualizações do funil por fase.
- Criar KPIs (volume de oportunidades, ticket médio, previsão por período).
- Adicionar filtros por vendedor, período e status.
- Melhorar tratamento de erros e logging das chamadas API.
- Organizar código em camadas (coleta, transformação, visualização).
- Incluir testes e validações de qualidade dos dados.

