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
    section_header,
    kpi_card,
    chart_card,
    resumo_estrategico,
    table_card,
    priority_header,
    simulacao_card
)
from database import engine

st.set_page_config(
    page_title='Audit de Vendas - Exagerado',
    layout='wide',
    initial_sidebar_state='expanded',
)

inject_theme()

@st.cache_data(ttl=300) # Cache de 5 minutos para o histórico completo
def load_full_event_data():
    # Puxa absolutamente tudo da tabela de vendas
    query = "SELECT * FROM vendas_itens ORDER BY timestamp ASC"
    df = pd.read_sql(query, engine)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['data'] = df['timestamp'].dt.date
    df['hora'] = df['timestamp'].dt.hour
    return df

df_completo = load_full_event_data()

# SideBar

with st.sidebar:
    st.image('img/favicon.ico', width=50)
    sidebar_logo()

    st.markdown('### Lojas Auditadas')

    opcao = st.radio(
        'Lojas',
        ['Painel Geral', 'Loja 1', 'Loja 2', 'Loja 3', 'Loja 4', 'Loja 5', 'Loja 6', 'Loja 7'],
        index=0,
        label_visibility='collapsed',
    )

    st.markdown('<hr style="border:none;border-top:1px solid rgba(255,255,255,0.08);margin:16px 0">', unsafe_allow_html=True)



### APLICA FILTROS ###

if opcao == "Painel Geral":
    st.title("📊 Relatório de Auditoria de Vendas")
    
    # 1. Ranking de Lojas (Tabela consolidada)
    st.subheader("🏆 Ranking de Lojas")
    ranking_lojas = df_completo.groupby('id_loja').agg({
        'valor_total': 'sum',
        'venda_id': 'nunique',
        'quantidade': 'sum'
    }).rename(columns={'venda_id': 'Vendas', 'valor_total': 'Faturamento'}).sort_values('Faturamento', ascending=False)
    
    # Cálculo de Ticket Médio
    ranking_lojas['Ticket Médio'] = ranking_lojas['Faturamento'] / ranking_lojas['Vendas']
    st.table(ranking_lojas.style.format({"Faturamento": "R$ {:.2f}", "Ticket Médio": "R$ {:.2f}"}))

    # 2. Vendas por Dia (Matriz comparativa)
    st.subheader("📅 Desempenho por Dia")
    vendas_dia = df_completo.pivot_table(
        index='id_loja', 
        columns='data', 
        values='valor_total', 
        aggfunc='sum', 
        fill_value=0
    )
    st.dataframe(vendas_dia.style.format("R$ {:.2f}"), use_container_width=True)

    # 3. Top 5 Produtos Mais Vendidos (Geral)
    st.subheader("📦 Top 5 Produtos Mais Vendidos")
    top_5 = df_completo.groupby(['nome_produto', 'id_loja']).agg({
        'quantidade': 'sum',
        'valor_total': 'sum'
    }).sort_values('quantidade', ascending=False).head(5)
    st.table(top_5.style.format({"valor_total": "R$ {:.2f}"}))