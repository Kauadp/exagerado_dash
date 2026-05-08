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
    chart_card,
    render_tabela_planejamento
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

@st.cache_data(ttl=10)
def load_full_event_data():
    query = "SELECT * FROM vendas_itens ORDER BY timestamp ASC"
    df = pd.read_sql(query, engine)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['data'] = df['timestamp'].dt.date
    df['hora'] = df['timestamp'].dt.hour
    return df

def load_forecast_data():
    query = """
       WITH ultima_carga AS (
        SELECT MAX(criado_em) as max_criado FROM previsoes_vendas
    )
    SELECT loja, previsao, timestamp_previsao 
    FROM previsoes_vendas 
    WHERE criado_em >= (SELECT max_criado FROM ultima_carga) - INTERVAL '1 minute'
    ORDER BY timestamp_previsao ASC;
        """
    df = pd.read_sql(query, engine)
    df['timestamp_previsao'] = pd.to_datetime(df['timestamp_previsao'])
    df = df[
        (df['timestamp_previsao'].dt.hour >= 10) & 
        (df['timestamp_previsao'].dt.hour <= 22)
    ].copy()
    return df


df_completo = load_full_event_data()

map_lojas = {
    205709335: "Vans",
    205709338: "Arezzo",
    205785185: "Off Premium",
    206057004: "Ida",
    205613392: "Aramis",
    205406209: "High",
    206057013: "Vix",
    206057007: "Surto dos 50"
}

meta_map = {
    205709335: 130000,  # Meta de vendas para a loja Vans
    205709338: 200000,  # Meta de vendas para a loja Arezzo
    205785185: 200000,  # Meta de vendas para a loja Off Premium
    206057004: 200000,   # Meta de vendas para a loja Ida
    205613392: 300000,  # Meta de vendas para a loja Aramis
    205406209: 150000,   # Meta de vendas para a loja High
    206057013: 50000,   # Meta de vendas para a loja Vix
    206057007: 30000   # Meta de vendas para a loja Surto dos 50
}


# SideBar

with st.sidebar:
    st.image('img/favicon.ico', width=50)
    sidebar_logo()

    st.markdown('### Lojas Auditadas')

    opcoes_lojas = ["Painel Geral", "Previsão Amanhã"] + list(map_lojas.values())

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
    section_header("📊 KPIs Gerais")

    # =========================
    # BASE DE CÁLCULO
    # =========================
    total_faturamento = df_completo['valor_total'].sum()
    total_vendas = df_completo['venda_id'].nunique()
    total_itens = df_completo['quantidade'].sum()

    ticket_medio = total_faturamento / total_vendas if total_vendas else 0
    pa = total_itens / total_vendas if total_vendas else 0

    # vendas por minuto (últimos dados)
    vendas_por_min = (
        df_completo
        .set_index('timestamp')
        .groupby(pd.Grouper(freq='1min'))['venda_id']
        .nunique()
        .mean()
    )

    meta_total = sum(meta_map.values())

    atingimento = total_faturamento / meta_total if meta_total else 0

    dias_observados = df_completo["data"].nunique()
    dias_totais = 6

    projecao = (total_faturamento / dias_observados) * dias_totais if dias_observados else 0

    atingimento_projetado = projecao / meta_total if meta_total else 0

    # =========================
    # KPIs PRINCIPAIS
    # =========================
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        kpi_card("💰 Faturamento", f"R$ {total_faturamento:,.2f}", "", "positive", "green")

    with col2:
        kpi_card("🎯 Meta", f"R$ {meta_total:,.0f}", "", "neutral", "blue")

    with col3:
        kpi_card("📊 Atingimento", f"{atingimento*100:.1f}%", "", 
                "positive" if atingimento >= 1 else "negative", "purple")

    with col4:
        kpi_card("🔮 Projeção", f"R$ {projecao:,.0f}", "", "neutral", "orange")

    with col5:
        kpi_card("🚀 Proj. vs Meta", f"{atingimento_projetado*100:.1f}%", "", 
                "positive" if atingimento_projetado >= 1 else "negative", "green")

    with col6:
        kpi_card("🧾 Vendas", f"{total_vendas}", "", "neutral", "yellow")

    # =========================
    # KPIs DE AUDITORIA
    # =========================
    st.markdown("")
    section_header("📊 Comportamento de Vendas")

    col1, col2, col3 = st.columns(3)

    with col1:
        kpi_card(
            "🎯 Ticket Médio",
            f"R$ {ticket_medio:,.2f}",
            "",
            "neutral",
            "purple"
        )

    with col2:
        kpi_card(
            "📦 P.A",
            f"{pa:.2f}",
            "",
            "neutral",
            "orange"
        )

    with col3:
        melhor_hora = df_completo.groupby('hora')['valor_total'].sum().idxmax()

        kpi_card(
            "⏰ Pico de Vendas",
            f"{melhor_hora}h",
            "",
            "positive",
            "green"
        )

    st.markdown("---")

    # =========================
    # GRÁFICOS
    # =========================
    st.title("📈 Análise Temporal")

    col1, col2 = st.columns(2)

    # Faturamento por dia
    faturamento_dia = (
        df_completo.groupby('data')['valor_total']
        .sum()
        .reset_index()
    )
    faturamento_dia["data_str"] = pd.to_datetime(faturamento_dia["data"]).dt.strftime("%d/%m")

    fig_dia = px.line(
        faturamento_dia,
        x='data_str',
        y='valor_total',
        markers=True
    )
    fig_dia.update_traces(line=dict(width=3, color=COLOR_PRIMARY), marker=dict(size=6, color=COLOR_PRIMARY))
    fig_dia.update_layout(margin=dict(l=10, r=10, t=30, b=10))

    # Faturamento por hora
    faturamento_hora = (
        df_completo.groupby('hora')['valor_total']
        .sum()
        .reset_index()
    )
    faturamento_hora["hora_str"] = faturamento_hora["hora"].astype(str) + "h"

    fig_hora = px.bar(
        faturamento_hora,
        x='hora_str',
        y='valor_total'
    )
    fig_hora.update_layout(margin=dict(l=10, r=10, t=30, b=10))
    fig_hora.update_traces(
        marker_color=COLOR_SECONDARY
    )

    with col1:
        chart_card(fig=fig_dia, title="Faturamento por Dia")

    with col2:
        chart_card(fig=fig_hora, title="Faturamento por Hora")

    # =========================
    # CURVA ACUMULADA
    # =========================
    df_sorted = df_completo.sort_values("timestamp")
    df_sorted["acumulado"] = df_sorted["valor_total"].cumsum()

    fig_acum = px.line(
        df_sorted,
        x="timestamp",
        y="acumulado"
    )

    fig_acum.update_layout(
        margin=dict(l=10, r=10, t=30, b=10),
        xaxis_title="Tempo",
        yaxis_title="R$"
    )
    fig_acum.update_traces(
        line=dict(color=COLOR_ACCENT, width=3)
    )

    chart_card(fig=fig_acum, title="📊 Faturamento Acumulado")

    df_meta = pd.DataFrame({
        "categoria": ["Atual", "Projeção", "Meta"],
        "valor": [total_faturamento, projecao, meta_total]
    })

    fig_meta = px.bar(df_meta, x="categoria", y="valor")
    fig_meta.update_traces(
        marker_color=[COLOR_PRIMARY, COLOR_SECONDARY, COLOR_ACCENT]
    )
    chart_card(fig=fig_meta, title="Meta vs Real")

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
        .reset_index()
    )

    # Mapear nome da loja
    ranking_lojas["Loja"] = ranking_lojas["id_loja"].map(map_lojas)

    # Mapear meta corretamente
    ranking_lojas["Meta"] = ranking_lojas["id_loja"].map(meta_map)

    # Proteção contra NaN
    ranking_lojas["Meta"] = ranking_lojas["Meta"].fillna(0)

    # Ticket médio
    ranking_lojas["Ticket Médio"] = ranking_lojas["Faturamento"] / ranking_lojas["Vendas"]

    # Projeção
    ranking_lojas["Projeção"] = np.where(
        dias_observados > 0,
        (ranking_lojas["Faturamento"] / dias_observados) * dias_totais,
        0
    )

    # Atingimento
    ranking_lojas["Atingimento"] = np.where(
        ranking_lojas["Meta"] > 0,
        ranking_lojas["Faturamento"] / ranking_lojas["Meta"],
        0
    )

    # Projeção vs Meta
    ranking_lojas["Proj. vs Meta"] = np.where(
        ranking_lojas["Meta"] > 0,
        ranking_lojas["Projeção"] / ranking_lojas["Meta"],
        0
    )

    # Seleção final (AGORA sim)
    ranking_lojas = ranking_lojas[
        ["Loja", "Faturamento", "Meta", "Atingimento", "Projeção", "Proj. vs Meta", "Vendas", "Ticket Médio"]
    ]

    ranking_lojas = ranking_lojas.sort_values("Faturamento", ascending=False)

    table_card(
        ranking_lojas,
        title="Ranking de Lojas",
        col_labels={
            "Loja": "Loja",
            "Faturamento": "Faturamento",
            "Meta": "Meta",
            "Atingimento": "% Meta",
            "Projeção": "Projeção",
            "Proj. vs Meta": "% Proj",
            "Vendas": "Vendas",
            "Ticket Médio": "Ticket"
        },
        col_formats={
            "Faturamento": lambda x: f"R$ {x:,.0f}",
            "Meta": lambda x: f"R$ {x:,.0f}",
            "Projeção": lambda x: f"R$ {x:,.0f}",
            "Atingimento": lambda x: f"{x*100:.1f}%",
            "Proj. vs Meta": lambda x: f"{x*100:.1f}%",
            "Vendas": lambda x: f"{int(x)}",
            "Ticket Médio": lambda x: f"R$ {x:,.2f}"
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

    linha_total = vendas_dia.sum().to_frame().T 
    linha_total.index = ["Total Geral"]

    vendas_dia["Loja"] = vendas_dia.index.map(map_lojas)
    vendas_dia = vendas_dia.reset_index(drop=True)

    linha_total["Loja"] = "Total"
    vendas_dia = pd.concat([vendas_dia, linha_total], ignore_index=True)

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

elif opcao == "Previsão Amanhã":
    st.title("🔮 Previsão de Vendas para Amanhã")

    st.markdown("---")

    df_forecast = load_forecast_data()

    # Cálculo Kpi's

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
        .reset_index()
    )
    ranking_lojas["Loja"] = ranking_lojas["id_loja"].map(map_lojas)
    ranking_lojas["Ticket Médio"] = ranking_lojas["Faturamento"] / ranking_lojas["Vendas"]
    dict_tickets = ranking_lojas.set_index('Loja')['Ticket Médio'].to_dict()
    df_forecast_prev = df_forecast[df_forecast['loja'] != 'Fluxo'].copy()
    df_forecast_prev['ticket_atual'] = df_forecast_prev['loja'].map(dict_tickets)
    df_forecast_prev['faturamento_previsto'] = df_forecast_prev['previsao'] * df_forecast_prev['ticket_atual']
    faturamento_previsao = df_forecast_prev['faturamento_previsto'].sum()

    fluxo = df_forecast[df_forecast['loja'] == 'Fluxo']
    pico_fluxo_horario = fluxo.sort_values('previsao', ascending=False).iloc[0]
    pico_fluxo_hora = pico_fluxo_horario['timestamp_previsao'].hour
    pico_fluxo_previsao = pico_fluxo_horario['previsao']

    df_fluxo_prev = df_forecast[df_forecast['loja'] == 'Fluxo'].copy()
    df_vendas_prev = df_forecast[df_forecast['loja'] != 'Fluxo'].copy()
    df_vendas_total = df_vendas_prev.groupby('timestamp_previsao')['previsao'].sum().reset_index()
    df_fluxo_prev['previsao'] = df_fluxo_prev['previsao'].clip(lower=0)
    df_corr = pd.merge(
        df_fluxo_prev[['timestamp_previsao', 'previsao']], 
        df_vendas_total[['timestamp_previsao', 'previsao']], 
        on='timestamp_previsao', 
        suffixes=('_fluxo', '_vendas')
    )
    lags = {}
    for i in range(4):
        lags[f"{i}h"] = df_corr['previsao_fluxo'].corr(df_corr['previsao_vendas'].shift(-i))
    delay_vencedor = max(lags, key=lags.get)
    corr_vencedora = lags[delay_vencedor]
    def calcular_delay_otimo(df_alinhado):
        correlacoes = []
        for delay in range(4): 
            corr = df_alinhado['previsao_fluxo'].corr(df_alinhado['previsao_vendas'].shift(-delay))
            correlacoes.append(corr if pd.notna(corr) else -1) # evita erro de argmax em NaNs      
        return np.argmax(correlacoes)
    janela_horas = calcular_delay_otimo(df_corr)
    if corr_vencedora < 0.4:
        msg_corr = "O volume de pessoas no pavilhão não converte em vendas."
        cor_corr = "red"
    else:
        msg_corr = "O volume de pessoas no pavilhão é um bom indicador para prever vendas."
        cor_corr = "green"
    
    # Kpi's

    col1, col2, col3 = st.columns(3)

    with col1:
        kpi_card("💰 Faturamento", f"R$ {faturamento_previsao:,.2f}", "", "positive", "green")

    with col2:
        kpi_card("⏰ Pico de Fluxo", f"{pico_fluxo_hora}h", f"Previsão: {pico_fluxo_previsao:.0f}", "neutral", "purple")

    with col3:
        kpi_card("⏳ Delay Conversão", f"{janela_horas}h", f"{msg_corr}", "neutral", cor_corr)

    st.markdown("---")

    st.subheader("Gráficos de Previsão")
    lojas_selecionadas = st.multiselect("Filtrar Lojas", df_vendas_prev['loja'].unique(), default=df_vendas_prev['loja'].unique())
    df_filtrado = df_vendas_prev[df_vendas_prev['loja'].isin(lojas_selecionadas)]

    col1, col2 = st.columns(2)

    with col1:
        fig_prev_vendas = px.line(
            df_filtrado,
            x='timestamp_previsao',
            y='previsao',
            color='loja',  
            markers=True, 
            template='plotly_white'
        )

        # 2. Estilização Profissional
        fig_prev_vendas.update_layout(
            margin=dict(l=10, r=10, t=50, b=10),
            legend=dict(
                orientation="h",      
                yanchor="bottom",
                y=1.02,             
                xanchor="right",
                x=1,
                title_text=''        
            ),
            hovermode="x unified",    
            xaxis=dict(showgrid=False),
            yaxis=dict(title='Peças Previstas', showgrid=True, gridcolor='LightGray')
        )
        fig_prev_vendas.update_traces(line=dict(width=2.5))
        fig_prev_vendas.update_xaxes(title_text='')

        chart_card(fig=fig_prev_vendas, title="Previsão de Vendas por Loja")
    with col2:
        fig_prev_fluxo = px.line(
            df_fluxo_prev,
            x='timestamp_previsao',
            y='previsao'
        )
        fig_prev_fluxo.update_layout(margin=dict(l=10, r=10, t=30, b=10))
        fig_prev_fluxo.update_traces(line=dict(width=3, color=COLOR_SECONDARY))
        fig_prev_fluxo.update_xaxes(title_text='')
        chart_card(fig=fig_prev_fluxo, title="Previsão de Fluxo por Hora")

    st.markdown("---")

    st.subheader("Tabela Resumo")

    render_tabela_planejamento(df_vendas_prev, df_fluxo_prev, dict_tickets)



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

    render_secao_loja(df_loja, nome_loja, loja_id, map_lojas, meta_map)