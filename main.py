#%%
import pandas as pd
import requests
import streamlit as st
import requests
import json

st.set_page_config(page_title="CRM - Oportunidades", layout="wide")

def get_opportunities():

    # Suas credenciais da Omie
    APP_KEY = st.secrets["app_key"]
    APP_SECRET = st.secrets["app_secret"]

    # Endpoint da API
    URL = "https://app.omie.com.br/api/v1/crm/oportunidades/"

    # Estrutura do corpo da requisição conforme o cURL fornecido
    payload = {
        "call": "ListarOportunidades",
        "param": [
            {
                "pagina": 1,
                "registros_por_pagina": 20,
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

        df = pd.DataFrame(data["cadastros"])

        return df.head()  # Exibe as primeiras linhas do DataFrame

    except requests.exceptions.HTTPError as err:
        print(f"Erro na API: {err}")
        print(f"Detalhes do erro: {response.text}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")


#%%

get_opportunities()

