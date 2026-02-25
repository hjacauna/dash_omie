# main.py
import json
import requests
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="CRM | Dashboard Gerencial",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------
# Estilo
# ----------------------------
st.markdown(
    """
<style>
    .block-container {padding-top: 1.2rem; padding-bottom: 2rem;}
    [data-testid="stMetricValue"] {font-size: 1.6rem;}
    [data-testid="stMetricLabel"] {opacity: .75;}
    .small-note {opacity:.7; font-size:.9rem;}
    .stDataFrame {border-radius: 14px;}
</style>
""",
    unsafe_allow_html=True,
)

# ----------------------------
# API helpers (cache)
# ----------------------------
@st.cache_data(ttl=60 * 30, show_spinner=False)
def get_opportunities():
    APP_KEY = st.secrets["app_key"]
    APP_SECRET = st.secrets["app_secret"]
    URL = "https://app.omie.com.br/api/v1/crm/oportunidades/"
    headers = {"Content-type": "application/json"}

    pagina = 1
    cadastros = []

    with requests.Session() as session:
        while True:
            payload = {
                "call": "ListarOportunidades",
                "param": [{"pagina": pagina, "registros_por_pagina": 100, "status": "A"}],
                "app_key": APP_KEY,
                "app_secret": APP_SECRET,
            }
            resp = session.post(URL, headers=headers, json=payload, timeout=60)
            resp.raise_for_status()
            data = resp.json()

            cadastros.extend(data.get("cadastros", []))
            total_de_paginas = int(data.get("total_de_paginas", 1))
            if pagina >= total_de_paginas:
                break
            pagina += 1

    df = pd.json_normalize(cadastros)

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
        "outrasInf.dAlteracao": "dtAlteracao",
    }

    df_out = df.rename(columns=col_map).reindex(columns=list(col_map.values()))

    for c in ["ticket Produtos", "ticket Meses", "ticket Recorrencia", "ticket Servico"]:
        df_out[c] = pd.to_numeric(df_out[c], errors="coerce")

    df_out["dtAlteracao"] = pd.to_datetime(
        df_out["dtAlteracao"], dayfirst=True, errors="coerce"
    )

    return df_out


@st.cache_data(ttl=60 * 60, show_spinner=False)
def get_fases():
    APP_KEY = st.secrets["app_key"]
    APP_SECRET = st.secrets["app_secret"]
    URL = "https://app.omie.com.br/api/v1/crm/fases/"
    headers = {"Content-type": "application/json"}

    payload = {
        "call": "ListarFases",
        "param": [{"pagina": 1, "registros_por_pagina": 200}],
        "app_key": APP_KEY,
        "app_secret": APP_SECRET,
    }

    resp = requests.post(URL, headers=headers, data=json.dumps(payload), timeout=60)
    resp.raise_for_status()
    data = resp.json()

    df = pd.json_normalize(data.get("cadastros", []))
    col_map = {"nCodigo": "nCodFase", "cDescrUsuario": "cDescFase"}
    return df.rename(columns=col_map).reindex(columns=list(col_map.values()))


@st.cache_data(ttl=60 * 60, show_spinner=False)
def get_usuario():
    APP_KEY = st.secrets["app_key"]
    APP_SECRET = st.secrets["app_secret"]
    URL = "https://app.omie.com.br/api/v1/crm/usuarios/"
    headers = {"Content-type": "application/json"}

    payload = {
        "call": "ListarUsuarios",
        "param": [{"pagina": 1, "registros_por_pagina": 500}],
        "app_key": APP_KEY,
        "app_secret": APP_SECRET,
    }

    resp = requests.post(URL, headers=headers, data=json.dumps(payload), timeout=60)
    resp.raise_for_status()
    data = resp.json()

    df = pd.json_normalize(data.get("cadastros", []))
    col_map = {"nCodigo": "nCodVendedor", "cNome": "cNomeUsuario", "cEmail": "Email"}
    return df.rename(columns=col_map).reindex(columns=list(col_map.values()))


@st.cache_data(ttl=60 * 60, show_spinner=False)
def get_contas():
    APP_KEY = st.secrets["app_key"]
    APP_SECRET = st.secrets["app_secret"]
    URL = "https://app.omie.com.br/api/v1/crm/contas/"
    headers = {"Content-type": "application/json"}

    pagina = 1
    cadastros = []

    with requests.Session() as session:
        while True:
            payload = {
                "call": "ListarContas",
                "param": [{"pagina": pagina, "registros_por_pagina": 100}],
                "app_key": APP_KEY,
                "app_secret": APP_SECRET,
            }
            resp = session.post(URL, headers=headers, json=payload, timeout=60)
            resp.raise_for_status()
            data = resp.json()

            cadastros.extend(data.get("cadastros", []))
            total_de_paginas = int(data.get("total_de_paginas", 1))
            if pagina >= total_de_paginas:
                break
            pagina += 1

    df = pd.json_normalize(cadastros)
    col_map = {
        "identificacao.cDoc": "CNPJ/CPF",
        "identificacao.cNome": "NomeConta",
        "identificacao.nCod": "nCodConta",
    }
    return df.rename(columns=col_map).reindex(columns=list(col_map.values()))


@st.cache_data(ttl=60 * 30, show_spinner=False)
def build_dataset():
    df_o = get_opportunities()
    df_f = get_fases()
    df_u = get_usuario()
    df_c = get_contas()

    df = df_o.merge(df_f, on="nCodFase", how="left")
    df = df.merge(df_u, on="nCodVendedor", how="left")
    df = df.merge(df_c, on="nCodConta", how="left")

    df_final = df[
        [
            "NomeConta",
            "CNPJ/CPF",
            "cNomeUsuario",
            "dtAlteracao",
            "cDescFase",
            "ticket Servico",
            "ticket Recorrencia",
            "ticket Produtos",
            "ticket Meses",
            "cDesOp",
        ]
    ].copy()

    hoje = pd.Timestamp.now().normalize()
    df_final["dias_inatividade"] = (hoje - df_final["dtAlteracao"]).dt.days

    df_final["ticket_total"] = (
        df_final[["ticket Servico", "ticket Recorrencia", "ticket Produtos"]]
        .fillna(0)
        .sum(axis=1)
    )

    # padroniza nulos
    df_final["cNomeUsuario"] = df_final["cNomeUsuario"].fillna("Sem vendedor")
    df_final["cDescFase"] = df_final["cDescFase"].fillna("Sem fase")
    df_final["NomeConta"] = df_final["NomeConta"].fillna("Sem conta")

    return df_final


def brl(v: float) -> str:
    v = float(v or 0)
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def metric_row(df_view: pd.DataFrame):
    total_ops = len(df_view)
    ticket_total = float(df_view["ticket_total"].sum(skipna=True) or 0)
    ticket_medio = float(df_view["ticket_total"].mean(skipna=True) or 0)
    inat_media = float(df_view["dias_inatividade"].mean(skipna=True) or 0)
    pct_criticas = (
        (df_view["dias_inatividade"].fillna(-1) > 15).mean() * 100
        if total_ops > 0
        else 0
    )

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Oportunidades", f"{total_ops:,}".replace(",", "."))
    c2.metric("Ticket total", brl(ticket_total))
    c3.metric("Ticket médio", brl(ticket_medio))
    c4.metric("Inatividade média", f"{inat_media:.1f} dias")
    c5.metric("% > 15 dias", f"{pct_criticas:.1f}%")

# ----------------------------
# Carrega dataset
# ----------------------------
with st.spinner("Carregando dados do CRM..."):
    df = build_dataset()

# ----------------------------
# Sidebar: filtros globais
# ----------------------------
st.sidebar.title("Filtros (globais)")

min_date = df["dtAlteracao"].min()
max_date = df["dtAlteracao"].max()

default_start = (min_date.date() if pd.notna(min_date) else pd.Timestamp.today().date())
default_end = (max_date.date() if pd.notna(max_date) else pd.Timestamp.today().date())

date_range = st.sidebar.date_input(
    "Período (dtAlteracao)",
    value=(default_start, default_end),
)

vendedores = ["Todos"] + sorted(df["cNomeUsuario"].dropna().unique().tolist())
fases = ["Todas"] + sorted(df["cDescFase"].dropna().unique().tolist())

sel_vendedor_global = st.sidebar.selectbox("Vendedor (global)", vendedores, index=0)
sel_fase_global = st.sidebar.selectbox("Fase (global)", fases, index=0)

min_inat = int(df["dias_inatividade"].min(skipna=True) if pd.notna(df["dias_inatividade"].min(skipna=True)) else 0)
max_inat = int(df["dias_inatividade"].max(skipna=True) if pd.notna(df["dias_inatividade"].max(skipna=True)) else 0)

inat_range = st.sidebar.slider(
    "Dias de inatividade",
    min_value=min_inat,
    max_value=max_inat,
    value=(min_inat, max_inat),
)

search = st.sidebar.text_input("Buscar (Conta / Oportunidade)", value="")

st.sidebar.markdown("---")
if st.sidebar.button("🔄 Recarregar dados (limpar cache)"):
    st.cache_data.clear()
    st.rerun()

# aplica filtros globais
df_filt = df.copy()

if isinstance(date_range, tuple) and len(date_range) == 2:
    d0, d1 = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    df_filt = df_filt[(df_filt["dtAlteracao"] >= d0) & (df_filt["dtAlteracao"] <= d1)]

if sel_vendedor_global != "Todos":
    df_filt = df_filt[df_filt["cNomeUsuario"] == sel_vendedor_global]

if sel_fase_global != "Todas":
    df_filt = df_filt[df_filt["cDescFase"] == sel_fase_global]

df_filt = df_filt[
    (df_filt["dias_inatividade"].fillna(0).astype(int) >= inat_range[0])
    & (df_filt["dias_inatividade"].fillna(0).astype(int) <= inat_range[1])
]

if search.strip():
    s = search.strip().lower()
    df_filt = df_filt[
        df_filt["NomeConta"].fillna("").str.lower().str.contains(s)
        | df_filt["cDesOp"].fillna("").str.lower().str.contains(s)
    ]

# ----------------------------
# Header + Download
# ----------------------------
st.title("CRM | Dashboard Gerencial")
st.caption("Visão gerencial de oportunidades ativas com tabs por área, ranking e drill-down.")

csv = df_filt.to_csv(index=False, sep=";", encoding="utf-8-sig")
st.download_button(
    label="⬇️ Baixar dados filtrados (CSV)",
    data=csv,
    file_name="oportunidades_filtradas.csv",
    mime="text/csv",
)

st.markdown("---")

# ----------------------------
# Tabs
# ----------------------------
tab1,tab2, tab5 = st.tabs(
    ["Visão Geral","Vendedores", "Base"]
)

# ----------------------------
# Tab 1: Visão Geral
# ----------------------------
with tab1:
    metric_row(df_filt)

    cA, cB = st.columns((1, 1))
    with cA:
        st.subheader("Oportunidades por fase")
        fase_counts = (
            df_filt["cDescFase"]
            .value_counts()
            .rename_axis("Fase")
            .reset_index(name="Oportunidades")
        )
        st.bar_chart(fase_counts.set_index("Fase")["Oportunidades"])

    with cB:
        st.subheader("Ticket total por vendedor (Top 10)")
        vend = (
            df_filt.groupby("cNomeUsuario")["ticket_total"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )
        st.bar_chart(vend.set_index("cNomeUsuario")["ticket_total"])

    cC, cD = st.columns((1, 1))
    with cC:
        st.subheader("Distribuição de inatividade")
        bins = [-1, 7, 14, 30, 60, 90, 10**9]
        labels = ["0-7", "8-14", "15-30", "31-60", "61-90", "90+"]
        faixa = pd.cut(df_filt["dias_inatividade"].fillna(-1), bins=bins, labels=labels)
        dist = faixa.value_counts().reindex(labels).fillna(0).astype(int)
        st.bar_chart(dist)

    with cD:
        st.subheader("Ticket total por fase (Top 20)")
        vend = (
            df_filt.groupby("cDescFase")["ticket_total"]
            .sum()
            .sort_values(ascending=False)
            .head(20)
            .reset_index()
        )
        st.bar_chart(vend.set_index("cDescFase")["ticket_total"])


    st.subheader("Oportunidades críticas (mais paradas)")
    crit = (
            df_filt.sort_values("dias_inatividade", ascending=False)
            .head(15)[
                [
                    "NomeConta",
                    "cNomeUsuario",
                    "cDescFase",
                    "dias_inatividade",
                    "ticket_total",
                    "cDesOp",
                ]
            ]
            .copy()
        )
    st.dataframe(crit, use_container_width=True, hide_index=True)



# ----------------------------
# Tab 2: Vendedores
# ----------------------------
with tab2:
    st.subheader("Análise por vendedor")

    vendedores_tab =["Todos"] + sorted(df_filt["cNomeUsuario"].dropna().unique().tolist())
    sel_vend_tab = st.selectbox(
        "Selecione um vendedor",
        options=vendedores_tab if vendedores_tab else ["Sem dados"],
        index=0,
    )
    if sel_vend_tab == "Todos":
        df_v = df_filt.copy()
    else:
        df_v = df_filt[df_filt["cNomeUsuario"] == sel_vend_tab].copy()

    metric_row(df_v)

    c1, c2 = st.columns((1, 1))
    with c1:
        st.subheader("Funil: oportunidades por fase (do vendedor)")
        funil = (
            df_v["cDescFase"]
            .value_counts()
            .rename_axis("Fase")
            .reset_index(name="Oportunidades")
        )
        st.bar_chart(funil.set_index("Fase")["Oportunidades"])

    with c2:
        st.subheader("Top contas por ticket (vendedor)")
        top_contas_v = (
            df_v.groupby("NomeConta")["ticket_total"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )
        st.bar_chart(top_contas_v.set_index("NomeConta")["ticket_total"])

    st.subheader("Críticas do vendedor (mais paradas)")
    crit_v = (
        df_v.sort_values(["dias_inatividade", "ticket_total"], ascending=[False, False])
        .head(20)[
            [
                "NomeConta",
                "cDescFase",
                "dtAlteracao",
                "dias_inatividade",
                "ticket_total",
                "cDesOp",
            ]
        ]
        .copy()
    )
    st.dataframe(crit_v, use_container_width=True, hide_index=True)


# ----------------------------
# Tab 5: Base (tabela + seleção de colunas)
# ----------------------------
with tab5:
    st.subheader("Base (dados filtrados)")

    show_cols = st.multiselect(
        "Colunas",
        options=list(df_filt.columns),
        default=[
            "NomeConta",
            "CNPJ/CPF",
            "cNomeUsuario",
            "cDescFase",
            "dtAlteracao",
            "dias_inatividade",
            "ticket Servico",
            "ticket Recorrencia",
            "ticket Produtos",
            "ticket Meses",
            "ticket_total",
            "cDesOp",
        ],
    )

    st.dataframe(
        df_filt[show_cols].sort_values(["dias_inatividade", "ticket_total"], ascending=[False, False]),
        use_container_width=True,
        hide_index=True,
    )

    st.caption("⬇️ O botão no topo exporta exatamente o que está filtrado (em todas as abas).")