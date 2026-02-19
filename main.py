#%%
import pandas as pd
import requests
import streamlit as st
import requests
import json
import time

st.set_page_config(page_title="CRM - Oportunidades", layout="wide")



def get_opportunities():

    # Suas credenciais da Omie
    APP_KEY = st.secrets["app_key"]
    APP_SECRET = st.secrets["app_secret"]

    # Endpoint da API
    URL = "https://app.omie.com.br/api/v1/crm/oportunidades/"

    # Cabeçalhos obrigatórios
    headers = {
        "Content-type": "application/json"
    }

    try:
        pagina = 1
        cadastros = []

        while True:
            # payload atualizado a cada página
            payload = {
                "call": "ListarOportunidades",
                "param": [
                    {
                        "pagina": pagina,
                        "registros_por_pagina": 100,
                        "status": "A",
                    }
                ],
                "app_key": APP_KEY,
                "app_secret": APP_SECRET
            }

            # Envia a requisição POST para a API
            response = requests.post(URL, headers=headers, data=json.dumps(payload))

            # Verifica se houve erro (4xx ou 5xx)
            response.raise_for_status()

            # Converte a resposta para JSON
            data = response.json()

            # acumula os cadastros da página atual
            cad = data.get("cadastros", [])
            cadastros.extend(cad)

            # controla paginação
            total_de_paginas = int(data.get("total_de_paginas", 1))
            print(f"Carregando página {pagina} de {total_de_paginas} | Registros acumulados: {len(cadastros)}")

            if pagina >= total_de_paginas:
                break

            pagina += 1

        # normaliza tudo de uma vez (todas as páginas)
        df = pd.json_normalize(cadastros)

        # Ajuste os nomes conforme o JSON real (normalmente fica tipo identificacao.nCodVendedor)
        col_map = {
            "identificacao.nCodVendedor": "nCodVendedor",
            "identificacao.nCodConta": "nCodConta",
            "identificacao.cDesOp": "cDesOp",
            "fasesStatus.nCodStatus": "nCodStatus",
            "fasesStatus.nCodFase": "nCodFase",
            "previsaoTemp.nAnoPrev": "nAnoPrev",
            "previsaoTemp.nMesPrev": "nMesPrev",
            "ticket.nMeses": "ticket Meses",
            "ticket.nProdutos": "ticket Produtos",
            "ticket.nRecorrencia": "ticket Recorrencia",
            "ticket.nServicos": "ticket Servico",
            "outrasInf.dAlteracao": "dtAlteracao"
        }

        df_out = (
            df.rename(columns=col_map)
              .reindex(columns=list(col_map.values()))
        )

        return df_out

    except requests.exceptions.HTTPError as err:
        print(f"Erro na API: {err}")
        print(f"Detalhes do erro: {response.text}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")


def get_fases():
    # Suas credenciais da Omie
    APP_KEY = st.secrets["app_key"]
    APP_SECRET = st.secrets["app_secret"]

    # Endpoint da API
    URL = "https://app.omie.com.br/api/v1/crm/fases/"

    # Estrutura do corpo da requisição conforme o cURL fornecido
    payload = {
        "call": "ListarFases",
        "param": [
            {
                "pagina": 1,
                "registros_por_pagina": 10,
            }
        ],
        "app_key": APP_KEY,
        "app_secret": APP_SECRET
    }

    # Cabeçalhos obrigatórios
    headers = {
        "Content-type": "application/json"
    }

    try:
        # Envia a requisição POST para a API
        response = requests.post(URL, headers=headers, data=json.dumps(payload))
        
        # Verifica se houve erro (4xx ou 5xx)
        response.raise_for_status()
        
        # Converte a resposta para JSON
        data = response.json()

        cad = data.get("cadastros", [])

        df = pd.json_normalize(cad)

        col_map = {
            "nCodigo": "nCodFase",
            "cDescrUsuario": "cDescrUsuario"
        }

        df_out = (
            df.rename(columns=col_map)
                .reindex(columns=list(col_map.values()))
        )

        
        return df_out # Exibe as primeiras linhas do DataFrame

    except requests.exceptions.HTTPError as err:
        print(f"Erro na API: {err}")
        print(f"Detalhes do erro: {response.text}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")


def get_usuario():
    # Suas credenciais da Omie
    APP_KEY = st.secrets["app_key"]
    APP_SECRET = st.secrets["app_secret"]

    # Endpoint da API
    URL = "https://app.omie.com.br/api/v1/crm/usuarios/"

    # Estrutura do corpo da requisição conforme o cURL fornecido
    payload = {
        "call": "ListarUsuarios",
        "param": [
            {
                "pagina": 1,
                "registros_por_pagina": 50,
            }
        ],
        "app_key": APP_KEY,
        "app_secret": APP_SECRET
    }

    # Cabeçalhos obrigatórios
    headers = {
        "Content-type": "application/json"
    }

    try:
        # Envia a requisição POST para a API
        response = requests.post(URL, headers=headers, data=json.dumps(payload))
        
        # Verifica se houve erro (4xx ou 5xx)
        response.raise_for_status()
        
        # Converte a resposta para JSON
        data = response.json()

        cad = data.get("cadastros", [])

        df = pd.json_normalize(cad)

        col_map = {
            "nCodigo": "nCodVendedor",
            "cNome": "cNomeUsuario",
            "cEmail": "Email"
        }

        df_out = (
            df.rename(columns=col_map)
                .reindex(columns=list(col_map.values()))
        )

        
        return df_out # Exibe as primeiras linhas do DataFrame

    except requests.exceptions.HTTPError as err:
        print(f"Erro na API: {err}")
        print(f"Detalhes do erro: {response.text}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")


def get_contas():
    APP_KEY = st.secrets["app_key"]
    APP_SECRET = st.secrets["app_secret"]

    URL = "https://app.omie.com.br/api/v1/crm/contas/"
    headers = {"Content-type": "application/json"}

    try:
        pagina = 1
        cadastros = []

        with requests.Session() as session:
            while True:
                payload = {
                    "call": "ListarContas",
                    "param": [{"pagina": pagina, "registros_por_pagina": 100}],
                    "app_key": APP_KEY,
                    "app_secret": APP_SECRET
                }

                # json=payload evita json.dumps + garante header ok
                response = session.post(URL, headers=headers, json=payload, timeout=60)
                response.raise_for_status()
                data = response.json()

                cad = data.get("cadastros", [])
                cadastros.extend(cad)

                total_de_paginas = int(data.get("total_de_paginas", 1))
                print(f"Carregando página {pagina} de {total_de_paginas} | Registros: {len(cadastros)}")

                if pagina >= total_de_paginas:
                    break

                pagina += 1

        df = pd.json_normalize(cadastros)

        col_map = {
            "identificacao.cDoc": "CNPJ/CPF",
            "identificacao.cNome": "NomeConta",
            "identificacao.nCod": "nCodConta"
        }

        df_out = (
            df.rename(columns=col_map)
              .reindex(columns=list(col_map.values()))
        )

        return df_out

    except requests.exceptions.HTTPError as err:
        print(f"Erro na API: {err}")
        print(f"Detalhes do erro: {response.text}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")



df_oportunities = get_opportunities()
df_fases = get_fases()
df_usuarios = get_usuario()
df_contas = get_contas()


df_oportunities = df_oportunities.merge(df_fases, on="nCodFase", how="left")
df_oportunities = df_oportunities.merge(df_usuarios, on="nCodVendedor", how="left")
df_oportunities = df_oportunities.merge(df_contas, on="nCodConta", how="left")

df_oportunities



