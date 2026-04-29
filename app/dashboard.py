import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import unicodedata
import sys
import os

from exagerado_theme import (
    inject_theme,
    sidebar_logo,
    table_card,
    section_header,
    kpi_card,
    chart_card
)
from database import engine
from services import render_secao_loja

st.set_page_config(
    page_title='Audit de Vendas - Exagerado',
    layout='wide',
    initial_sidebar_state='expanded',
)
COLOR_PRIMARY = "#6B3FA0"   # roxo
COLOR_SECONDARY = "#F59E0B" # amarelo/laranja
COLOR_ACCENT = "#10B981"    # verde

inject_theme()

@st.cache_data(ttl=300)
def load_full_event_data():
    query = "SELECT * FROM vendas_itens ORDER BY timestamp ASC"
    df = pd.read_sql(query, engine)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['data'] = df['timestamp'].dt.date
    df['hora'] = df['timestamp'].dt.hour
    return df

df_completo = load_full_event_data()

map_lojas = {
    205906072: "Loja Teste"
}

# SideBar

with st.sidebar:
    st.image('img/favicon.ico', width=50)
    sidebar_logo()

    st.markdown('### Lojas Auditadas')

    opcoes_lojas = ["Painel Geral"] + list(map_lojas.values())

    opcao = st.radio(
        'Lojas',
        opcoes_lojas,
        index=0,
        label_visibility='collapsed',
    )

    st.markdown('<hr style="border:none;border-top:1px solid rgba(255,255,255,0.08);margin:16px 0">', unsafe_allow_html=True)

st.title("📊 Relatório de Auditoria de Vendas")

if opcao == "Painel Geral":
    st.title("Visão Geral das Lojas")

    st.markdown("---")
    
    section_header("Kpi's Gerais")

    col1, col2, col3 = st.columns(3)

    with col1:
        melhor_dia = df_completo.groupby('data')['valor_total'].sum().idxmax()
        kpi_card(
            "📅Melhor Dia de Vendas",
            f"{melhor_dia.strftime('%d/%m/%Y')}",
            f"Faturamento: R$ {df_completo.groupby('data')['valor_total'].sum().max():,.2f}",
            "positive",
            "green"
        )

    with col2:
        melhor_hora = df_completo.groupby('hora')['valor_total'].sum().idxmax()
        kpi_card(
            "⏰ Melhor Hora de Vendas",
            f"{melhor_hora}:00 - {melhor_hora+1}:00",
            f"Faturamento: R$ {df_completo.groupby('hora')['valor_total'].sum().max():,.2f}",
            "positive",
            "green"
        )

    with col3:
        dias_observados = df_completo["data"].nunique()
        dias_totais = 6
        total_vendas = df_completo['valor_total'].sum()
        kpi_card(
            "💰 Faturamento Total",
            f"R$ {total_vendas:,.2f}",
            f"Projeção de Vendas: R$ {df_completo['valor_total'].sum() / dias_observados * dias_totais:,.2f}",
            "positive",
            "green"
        )

    st.markdown("---")
   
    st.title("Gráficos Rápidos")
    col1, col2 = st.columns(2)

    faturamento_dia = (
        df_completo
        .groupby('data')['valor_total']
        .sum()
        .reset_index()
    )

    faturamento_dia["data"] = pd.to_datetime(faturamento_dia["data"])
    faturamento_dia["data_str"] = faturamento_dia["data"].dt.strftime("%d/%m")

    fig_faturamento = px.line(
        faturamento_dia,
        x='data_str',
        y='valor_total',
        markers=True
    )

    fig_faturamento.update_traces(
        line=dict(color=COLOR_PRIMARY, width=3),
        marker=dict(size=6)
    )

    fig_faturamento.update_layout(
        margin=dict(l=10, r=10, t=30, b=10),
        xaxis_title="",
        yaxis_title="R$",
        xaxis=dict(type='category')
    )

    ranking_lojas = (
        df_completo
        .groupby('id_loja')
        .agg({
            'valor_total': 'sum',
            'venda_id': 'nunique'
        })
        .rename(columns={
            'valor_total': 'Faturamento',
            'venda_id': 'Vendas'
        })
    )
    
    ranking_lojas["Loja"] = ranking_lojas.index.map(map_lojas)
    ranking_lojas = ranking_lojas.reset_index(drop=True)
    ranking_lojas = ranking_lojas[["Loja", "Faturamento", "Vendas"]]
    ranking_lojas['Ticket Médio'] = ranking_lojas['Faturamento'] / ranking_lojas['Vendas']

    ranking_plot = ranking_lojas.copy()

    fig_ranking = px.bar(
        ranking_plot,
        x="Loja",
        y="Faturamento",
        text_auto=True
    )

    fig_ranking.update_traces(
        marker_color=COLOR_PRIMARY,
        textposition="outside"
    )

    fig_ranking.update_layout(
        margin=dict(l=10, r=10, t=30, b=10),
        xaxis_title="",
        yaxis_title="R$",
    )

    faturamento_hora = (
        df_completo
        .groupby('hora')['valor_total']
        .sum()
        .reset_index()
    )

    faturamento_hora = faturamento_hora.sort_values("hora")

    faturamento_hora["hora_str"] = faturamento_hora["hora"].astype(int).astype(str) + "h"

    fig_faturamento_hora = px.bar(
        faturamento_hora,
        x='hora_str',
        y='valor_total'
    )

    fig_faturamento_hora.update_traces(
        marker_color=COLOR_SECONDARY
    )

    fig_faturamento_hora.update_layout(
        margin=dict(l=10, r=10, t=30, b=10),
        xaxis_title="Hora",
        yaxis_title="R$",
        xaxis=dict(type='category')
    )
   
    with col1:
        chart_card(
            fig=fig_faturamento,
            title="Faturamento por Dia"
        )
    with col2:
        chart_card(
            fig=fig_ranking,
            title="Faturamento por Loja"
        )
    chart_card(
        fig=fig_faturamento_hora,
        title="Faturamento por Hora"
    )
   
    st.markdown("---")

    st.title("Tabelas Detalhadas")
    
    # Ranking de Lojas (Tabela consolidada)
    st.subheader("🏆 Ranking de Lojas")
    ranking_lojas = (
        df_completo
        .groupby('id_loja')
        .agg({
            'valor_total': 'sum',
            'venda_id': 'nunique'
        })
        .rename(columns={
            'valor_total': 'Faturamento',
            'venda_id': 'Vendas'
        })
    )
    
    ranking_lojas["Loja"] = ranking_lojas.index.map(map_lojas)
    ranking_lojas = ranking_lojas.reset_index(drop=True)
    ranking_lojas = ranking_lojas[["Loja", "Faturamento", "Vendas"]]
    ranking_lojas['Ticket Médio'] = ranking_lojas['Faturamento'] / ranking_lojas['Vendas']

    dias_observados = df_completo["data"].nunique()
    dias_totais = 6

    ranking_lojas["Projeção de Faturamento"] = (
        ranking_lojas["Faturamento"] / dias_observados
    ) * dias_totais

    ranking_lojas = ranking_lojas.sort_values(
        "Faturamento", ascending=False
    )

    table_card(
        ranking_lojas,
        title="Ranking de Lojas",
        col_labels={
            "Loja": "Loja",
            "Faturamento": "Faturamento",
            "Vendas": "Vendas",
            "Projeção de Faturamento": "Projeção"
        },
        col_formats={
            "Faturamento": lambda x: f"R$ {x:,.2f}",
            "Projeção de Faturamento": lambda x: f"R$ {x:,.2f}",
            "Vendas": lambda x: f"{int(x)}"
        }
    )

    st.markdown("---")

    # Vendas por Dia (Matriz comparativa)
    st.subheader("📅 Desempenho por Dia")

    df_completo["data"] = pd.to_datetime(df_completo["data"])
    vendas_dia = df_completo.pivot_table(
        index='id_loja',
        columns='data',
        values='valor_total',
        aggfunc='sum',
        fill_value=0
    )
    vendas_dia = vendas_dia.sort_index(axis=1)
    vendas_dia["Total"] = vendas_dia.sum(axis=1)
    vendas_dia["Loja"] = vendas_dia.index.map(map_lojas)
    vendas_dia = vendas_dia.reset_index(drop=True)

    cols_datas = [c for c in vendas_dia.columns if isinstance(c, pd.Timestamp)]

    vendas_dia = vendas_dia[
        ["Loja"] + cols_datas + ["Total"]
    ]

    vendas_dia.columns = [
        c.strftime("%d/%m") if isinstance(c, pd.Timestamp) else c
        for c in vendas_dia.columns
    ]
    table_card(
        vendas_dia,
        title="Vendas por Dia",
        col_formats={
            col: (lambda x: f"R$ {x:,.2f}")
            for col in vendas_dia.columns
            if col != "Loja"
        }
    )

    st.markdown("---")

    # Top 5 Produtos Mais Vendidos (Geral)
    st.subheader("📦 Top 5 Produtos Mais Vendidos")

    top_5 = (
        df_completo
        .groupby(['nome_produto', 'id_loja'])
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

    faturamento_loja = (
        df_completo
        .groupby('id_loja')['valor_total']
        .sum()
    )
    top_5["Proporção"] = top_5.apply(
        lambda row: row["Faturamento"] / faturamento_loja[row["id_loja"]],
        axis=1
    )
    top_5 = top_5.sort_values("Quantidade", ascending=False).head(5)
    top_5["Loja"] = top_5["id_loja"].map(map_lojas)
    def medalha(i):
        if i == 0:
            return "🥇"
        elif i == 1:
            return "🥈"
        elif i == 2:
            return "🥉"
        else:
            return f"{i+1}º"

    top_5 = top_5.reset_index(drop=True)
    top_5["Posição"] = top_5.index.map(medalha)
    top_5 = top_5[
        ["Posição", "nome_produto", "Loja", "Quantidade", "Faturamento", "Proporção"]
    ]
    table_card(
        top_5,
        title="Top 5 Produtos",
        col_labels={
            "Posição": "#",
            "nome_produto": "Produto",
            "Loja": "Loja",
            "Quantidade": "Qtd",
            "Faturamento": "Faturamento",
            "Proporção": "% Loja"
        },
        col_formats={
            "Faturamento": lambda x: f"R$ {x:,.2f}",
            "Proporção": lambda x: f"{x*100:.1f}%"
        }
    )

else:
    nome_loja = opcao

    loja_id = next(
        (k for k, v in map_lojas.items() if v == nome_loja),
        None
    )

    if loja_id is None:
        st.error("Loja não encontrada no mapeamento.")
        st.stop()

    df_loja = df_completo[df_completo["id_loja"] == loja_id]

    render_secao_loja(df_loja, nome_loja, loja_id, map_lojas)