import pandas as pd
import plotly.express as px
import streamlit as st
from config import DATABASE_URL
from exagerado_theme import section_header, kpi_card, chart_card, table_card
import requests

def render_secao_loja(df_loja, nome_loja, loja_id, map_lojas):

    st.title(f"🏪 {nome_loja}")
    st.markdown("---")

    # ================= KPI =================
    section_header("KPI's da Loja")

    col1, col2, col3 = st.columns(3)

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

    with col1:
        kpi_card(
            "💰 Faturamento",
            f"R$ {faturamento:,.2f}",
            f"Projeção: R$ {projecao:,.2f}",
            "positive",
            "green"
        )

    with col2:
        kpi_card(
            "🧾 Vendas",
            f"{vendas}",
            "Quantidade total",
            "neutral"
        )

    with col3:
        kpi_card(
            "🎯 Ticket Médio",
            f"R$ {ticket:,.2f}",
            f"Melhor hora: {melhor_hora}h",
            "neutral"
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

    top_prod = top_prod.reset_index(drop=True)
    top_prod["Posição"] = top_prod.index.map(medalha)

    top_prod = top_prod[
        ["Posição", "nome_produto", "Quantidade", "Faturamento", "Proporção"]
    ]

    table_card(
        top_prod,
        col_labels={
            "Posição": "#",
            "nome_produto": "Produto",
            "Quantidade": "Qtd",
            "Faturamento": "Faturamento",
            "Proporção": "% Loja"
        },
        col_formats={
            "Faturamento": lambda x: f"R$ {x:,.2f}",
            "Proporção": lambda x: f"{x*100:.1f}%"
        }
    )

    st.markdown("---")

    # ================= BOTÃO =================
    if st.button(f"📸 Gerar relatório {nome_loja}"):

        html = gerar_html_secao_loja(df_loja, nome_loja)
        #arquivo = LINK ENDPOINT API EM DESENVOLVIMENTO DO BACKEND, RECEBE REQUISICAO E TIRA O PRINT

        st.success("Imagem gerada!")

        try:
            url_api = st.secrets["api"]["URL_API"]
            webhook_token = st.secrets["api"]["WEBHOOK_TOKEN"]
            id_da_loja = loja_id
            with open(arquivo, "rb") as f:
                files = {"file": (arquivo, f, "image/png")}
                data = {"loja_id": id_da_loja}
                params = {"token": webhook_token}

                response = requests.post(url_api, params=params, data=data, files=files)

            if response.status_code == 200:
                st.info("🚀 Sinal enviado para o backend!")
            else:
                st.error(f"⚠️ Erro ao sinalizar backend: {response.status_code}")
                
        except Exception as e:
            st.error(f"💥 Falha na comunicação local: {e}")

        # 3. OPÇÃO DE BAIXAR (Mantém como redundância se você quiser guardar)
        with open(arquivo, "rb") as f:
            st.download_button(
                label="⬇️ Baixar imagem (Cópia Local)",
                data=f,
                file_name=arquivo,
                mime="image/png"
            )

def gerar_html_secao_loja(df_loja, nome_loja):

    # =========================
    # SEGURANÇA (EVITA CRASH)
    # =========================
    if df_loja is None or df_loja.empty:
        return """
        <html>
        <body style="font-family:sans-serif;padding:20px;">
            <h3>Sem dados disponíveis para essa loja</h3>
        </body>
        </html>
        """

    # =========================
    # KPI BASE
    # =========================
    faturamento = df_loja['valor_total'].sum()
    vendas = df_loja['venda_id'].nunique()
    ticket = faturamento / vendas if vendas > 0 else 0

    # =========================
    # PROJEÇÃO
    # =========================
    dias = df_loja["data"].nunique()
    dias_totais = 6
    projecao = (faturamento / dias) * dias_totais if dias > 0 else 0

    percentual = (faturamento / projecao * 100) if projecao > 0 else 0

    # =========================
    # HORAS (INSIGHT OPERACIONAL)
    # =========================
    faturamento_hora = (
        df_loja.groupby('hora')['valor_total']
        .sum()
        .reset_index()
        .sort_values("hora")
    )

    if not faturamento_hora.empty:
        melhor_hora = faturamento_hora.loc[faturamento_hora['valor_total'].idxmax(), 'hora']
        pior_hora = faturamento_hora.loc[faturamento_hora['valor_total'].idxmin(), 'hora']

        ultima_hora = faturamento_hora.iloc[-1]['hora']
        valor_ultima_hora = faturamento_hora.iloc[-1]['valor_total']
        media_hora = faturamento_hora['valor_total'].mean()

        pico = faturamento_hora['valor_total'].max()
        vale = faturamento_hora['valor_total'].min()

        status_hora = "🔥 Acima da média" if valor_ultima_hora >= media_hora else "⚠️ Abaixo da média"
    else:
        melhor_hora = pior_hora = ultima_hora = "-"
        valor_ultima_hora = 0
        pico = vale = 0
        status_hora = "Sem dados"

    # =========================
    # GRÁFICO (DIÁRIO)
    # =========================
    faturamento_dia = (
        df_loja.groupby('data')['valor_total']
        .sum()
        .reset_index()
        .sort_values("data")
    )

    faturamento_dia["data"] = pd.to_datetime(faturamento_dia["data"])
    faturamento_dia["data_str"] = faturamento_dia["data"].dt.strftime("%d/%m")

    fig = px.line(
        faturamento_dia,
        x='data_str',
        y='valor_total',
        markers=True
    )

    fig.update_traces(line=dict(color="#6B3FA0", width=3))

    grafico_html = fig.to_html(full_html=False, include_plotlyjs='cdn')

    # =========================
    # TOP PRODUTOS
    # =========================

    # 💰 FATURAMENTO
    top_fat = (
        df_loja.groupby('nome_produto')['valor_total']
        .sum()
        .sort_values(ascending=False)
        .head(3)
        .reset_index()
    )

    lista_fat = "".join([
        f"<li><b>{row['nome_produto']}</b> — R$ {row['valor_total']:,.2f}</li>"
        for _, row in top_fat.iterrows()
    ])

    # 📦 QUANTIDADE
    top_qtd = (
        df_loja.groupby('nome_produto')['quantidade']
        .sum()
        .sort_values(ascending=False)
        .head(3)
        .reset_index()
    )

    lista_qtd = "".join([
        f"<li><b>{row['nome_produto']}</b> — {int(row['quantidade'])} un</li>"
        for _, row in top_qtd.iterrows()
    ])

    # 🔥 ATUAL (RECENTE)
    ultimas_horas = faturamento_hora.tail(2)['hora'].tolist() if not faturamento_hora.empty else []

    df_recente = df_loja[df_loja['hora'].isin(ultimas_horas)]

    top_recente = (
        df_recente.groupby('nome_produto')['valor_total']
        .sum()
        .sort_values(ascending=False)
        .head(3)
        .reset_index()
    )

    if top_recente.empty:
        lista_recente = "<li>Sem vendas recentes</li>"
    else:
        lista_recente = "".join([
            f"<li><b>{row['nome_produto']}</b> — R$ {row['valor_total']:,.2f}</li>"
            for _, row in top_recente.iterrows()
        ])

    # =========================
    # STATUS COR
    # =========================
    cor_status = "#10B981" if percentual >= 100 else "#F59E0B" if percentual >= 80 else "#EF4444"

    # =========================
    # HTML FINAL
    # =========================
    html = f"""
    <html>
    <body style="font-family:sans-serif;background:#F6F4EE;padding:20px;">

        <div style="max-width:520px;margin:auto;">

            <!-- HEADER -->
            <div style="background:#6B3FA0;color:white;padding:16px;border-radius:12px;">
                <h2 style="margin:0;">🏪 {nome_loja}</h2>
                <p style="margin:4px 0 0 0;font-size:12px;">
                    Atualizado às {pd.Timestamp.now().strftime('%H:%M')}
                </p>
            </div>

            <!-- KPI -->
            <div style="background:white;padding:16px;border-radius:12px;margin-top:12px;">

                <p><b>💰 Faturamento:</b> R$ {faturamento:,.2f}</p>
                <p><b>🧾 Vendas:</b> {vendas}</p>
                <p><b>🎯 Ticket:</b> R$ {ticket:,.2f}</p>

                <hr>

                <p style="color:{cor_status};font-weight:bold;">
                    📊 {percentual:.0f}% da projeção (R$ {projecao:,.2f})
                </p>

            </div>

            <!-- MOMENTO -->
            <div style="background:white;padding:16px;border-radius:12px;margin-top:12px;">

                <b>⏱ Agora</b>

                <p>Última hora: {ultima_hora}h (R$ {valor_ultima_hora:,.2f})</p>
                <p>{status_hora}</p>

            </div>

            <!-- INSIGHTS -->
            <div style="background:white;padding:16px;border-radius:12px;margin-top:12px;">

                <b>📌 Insights</b>

                <p>🔥 Melhor hora: {melhor_hora}h (R$ {pico:,.2f})</p>
                <p>⚠️ Pior hora: {pior_hora}h (R$ {vale:,.2f})</p>

            </div>

            <!-- GRÁFICO -->
            <div style="background:white;padding:16px;border-radius:12px;margin-top:12px;">
                {grafico_html}
            </div>

            <!-- PRODUTOS -->
            <div style="background:white;padding:16px;border-radius:12px;margin-top:12px;">

                <b>🔥 Vendendo Agora</b>
                <ul>{lista_recente}</ul>

                <hr>

                <b>🏆 Top Faturamento</b>
                <ul>{lista_fat}</ul>

                <hr>

                <b>📦 Mais Vendidos</b>
                <ul>{lista_qtd}</ul>

            </div>

        </div>

    </body>
    </html>
    """

    return html