import pandas as pd
import plotly.express as px
import streamlit as st
from config import DATABASE_URL
from exagerado_theme import section_header, kpi_card, chart_card, table_card
import requests

def render_secao_loja(df_loja, nome_loja, loja_id, map_lojas, meta_map):

    st.title(f"🏪 {nome_loja}")
    st.markdown("---")

    # ================= KPI =================
    section_header("KPI's da Loja")

    faturamento = df_loja['valor_total'].sum()
    vendas = df_loja['venda_id'].nunique()
    ticket = faturamento / vendas if vendas > 0 else 0

    melhor_hora = (
        df_loja.groupby('hora')['valor_total']
        .sum()
        .idxmax()
    )
    dias_observados = df_loja["data"].nunique()
    dias_totais = 6

    projecao = (faturamento / dias_observados) * dias_totais if dias_observados > 0 else 0

    meta_loja = meta_map.get(loja_id, 0)

    atingimento = faturamento / meta_loja if meta_loja else 0

    atingimento_projetado = projecao / meta_loja if meta_loja else 0

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        kpi_card(
            "💰 Faturamento",
            f"R$ {faturamento:,.2f}",
            "",
            "positive",
            "green"
        )

    with col2:
        kpi_card(
            "🎯 Meta",
            f"R$ {meta_loja:,.0f}",
            "",
            "neutral",
            "blue"
        )

    with col3:
        kpi_card(
            "📊 Atingimento",
            f"{atingimento*100:.1f}%",
            "",
            "positive" if atingimento >= 1 else "negative",
            "purple"
        )

    with col4:
        kpi_card(
            "🔮 Projeção",
            f"R$ {projecao:,.0f}",
            "",
            "neutral",
            "orange"
        )

    with col5:
        kpi_card(
            "🚀 Proj. vs Meta",
            f"{atingimento_projetado*100:.1f}%",
            "",
            "positive" if atingimento_projetado >= 1 else "negative",
            "green"
        )

    st.markdown("---")

    # ================= GRÁFICOS =================
    st.subheader("📊 Desempenho")

    col1, col2 = st.columns(2)

    # ===== POR DIA =====
    faturamento_dia = (
        df_loja.groupby('data')['valor_total']
        .sum()
        .reset_index()
    )

    faturamento_dia["data"] = pd.to_datetime(faturamento_dia["data"])
    faturamento_dia["data_str"] = faturamento_dia["data"].dt.strftime("%d/%m")

    fig_dia = px.line(
        faturamento_dia,
        x='data_str',
        y='valor_total',
        markers=True
    )

    fig_dia.update_traces(line=dict(color="#6B3FA0", width=3))
    fig_dia.update_layout(xaxis=dict(type='category'))

    # ===== POR HORA =====
    faturamento_hora = (
        df_loja.groupby('hora')['valor_total']
        .sum()
        .reset_index()
        .sort_values("hora")
    )

    faturamento_hora["hora_str"] = faturamento_hora["hora"].astype(int).astype(str) + "h"

    fig_hora = px.bar(
        faturamento_hora,
        x='hora_str',
        y='valor_total'
    )

    fig_hora.update_traces(marker_color="#F59E0B")
    fig_hora.update_layout(xaxis=dict(type='category'))

    with col1:
        chart_card("Faturamento por Dia", fig_dia)

    with col2:
        chart_card("Faturamento por Hora", fig_hora)

    df_meta = pd.DataFrame({
        "categoria": ["Atual", "Projeção", "Meta"],
        "valor": [faturamento, projecao, meta_loja]
    })

    fig_meta = px.bar(df_meta, x="categoria", y="valor")

    fig_meta.update_traces(
        marker_color=["#6B3FA0", "#F59E0B", "#10B981"]
    )

    chart_card("Meta vs Real", fig_meta)

    st.markdown("---")

    # ================= TABELA =================

    st.subheader("📅 Desempenho por Dia")

    vendas_dia = df_loja.pivot_table(
        index=None,
        columns='data',
        values='valor_total',
        aggfunc='sum',
        fill_value=0
    )

    # garante ordenação das datas
    vendas_dia = vendas_dia.sort_index(axis=1)

    # adiciona total
    vendas_dia["Total"] = vendas_dia.sum(axis=1)

    # reset index pra virar dataframe normal
    vendas_dia = vendas_dia.reset_index(drop=True)

    # formata nomes das colunas (datas)
    vendas_dia.columns = [
        c.strftime("%d/%m") if isinstance(c, pd.Timestamp) else c
        for c in vendas_dia.columns
    ]

    table_card(
        vendas_dia,
        col_formats={
            col: (lambda x: f"R$ {x:,.2f}")
            for col in vendas_dia.columns
        }
    )

    st.subheader("📦 Top Produtos")

    top_prod = (
        df_loja
        .groupby('nome_produto')
        .agg({
            'quantidade': 'sum',
            'valor_total': 'sum'
        })
        .rename(columns={
            'quantidade': 'Quantidade',
            'valor_total': 'Faturamento'
        })
        .reset_index()
    )

    faturamento_total = top_prod["Faturamento"].sum()

    top_prod["Proporção"] = top_prod["Faturamento"] / faturamento_total

    top_prod = top_prod.sort_values(
        "Quantidade", ascending=False
    ).head(5)

    def medalha(i):
        if i == 0:
            return "🥇"
        elif i == 1:
            return "🥈"
        elif i == 2:
            return "🥉"
        else:
            return f"{i+1}º"

    top_prod["Ticket Médio"] = top_prod["Faturamento"] / top_prod["Quantidade"]
    top_prod = top_prod.reset_index(drop=True)
    top_prod["Posição"] = top_prod.index.map(medalha)

    top_prod = top_prod[
        ["Posição", "nome_produto", "Quantidade", "Faturamento", "Proporção", "Ticket Médio"]
    ]

    table_card(
        top_prod,
        col_labels={
            "Posição": "#",
            "nome_produto": "Produto",
            "Quantidade": "Qtd",
            "Faturamento": "Faturamento",
            "Proporção": "% Loja",
            "Ticket Médio": "Ticket Médio"
        },
        col_formats={
            "Faturamento": lambda x: f"R$ {x:,.2f}",
            "Proporção": lambda x: f"{x*100:.1f}%",
            "Ticket Médio": lambda x: f"R$ {x:,.2f}"
        }
    )

    st.markdown("---")

    # ================= BOTÃO =================
    if st.button(f"📸 Gerar relatório {nome_loja}"):
        try:
            url_api = st.secrets['api']['URL_API_TRIG']
            webhook_token = st.secrets["api"]["WEBHOOK_TOKEN"]
            
            params = {
                "loja_id": loja_id,
                "token": webhook_token
            }

            with st.spinner(f"Acionando motor na Oracle para gerar e enviar relatório..."):
                response = requests.post(url_api, params=params)

            if response.status_code == 200:
                st.success(f"✅ Relatório da {nome_loja} enviado para o WhatsApp!")
                st.balloons()
            else:
                st.error(f"⚠️ Erro no servidor: {response.status_code} - {response.text}")
                
        except Exception as e:
            st.error(f"💥 Falha de conexão com o backend: {e}")
