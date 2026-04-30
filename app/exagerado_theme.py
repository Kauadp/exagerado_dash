"""
exagerado_theme.py
Aplique no início do seu app com:  inject_theme()
"""

from streamlit.components.v1 import html
import streamlit as st
import pandas as pd

def inject_theme():
    st.markdown("""
    <style>
    /* =============================================
       MEU EXAGERADO — Custom Streamlit Theme
       Identidade visual: meuexagerado.com.br
    ============================================= */

    /* --- VARIÁVEIS --- */
    :root {
        --ex-black:         #1A1A1A;
        --ex-white:         #F6F4EE;
        --ex-purple:        #6B3FA0;
        --ex-purple-light:  #EDE8F5;
        --ex-purple-mid:    #9B6FCC;
        --ex-gray:          #F2F1EE;
        --ex-gray-mid:      #D4D2CC;
        --ex-gray-dark:     #6B6963;
        --ex-green:         #2E7D5C;
        --ex-green-light:   #E8F4EE;
        --ex-red:           #C0392B;
        --ex-red-light:     #FBEAE8;
        --ex-amber:         #B07818;
        --ex-amber-light:   #FBF3E0;
        --ex-border:        rgba(26,26,26,0.1);
    }

    /* --- FONTE BASE --- */
    html, body, [class*="css"] {
        font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    }

    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Serif+Display:ital@0;1&display=swap');

    /* --- FUNDO PRINCIPAL --- */
    .stApp {
        background-color: var(--ex-white) !important;
    }

    /* --- SIDEBAR --- */
    [data-testid="stSidebar"] {
        background-color: var(--ex-black) !important;
    }

    [data-testid="stSidebar"] * {
        color: rgba(255,255,255,0.7) !important;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: rgba(255,255,255,0.95) !important;
    }

    [data-testid="stSidebar"] .stMarkdown h1 {
        font-family: 'DM Serif Display', serif !important;
        font-style: italic;
        font-size: 20px !important;
        color: #FAFAF8 !important;
        margin-bottom: 2px !important;
    }

    /* Logo / título sidebar */
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p:first-child {
        font-family: 'DM Serif Display', serif !important;
    }

    /* Inputs dentro da sidebar */
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stDateInput label,
    [data-testid="stSidebar"] .stMultiSelect label {
        color: rgba(255,255,255,0.45) !important;
        font-size: 11px !important;
        font-weight: 500 !important;
        letter-spacing: 1.2px !important;
        text-transform: uppercase !important;
    }

    [data-testid="stSidebar"] .stSelectbox > div > div,
    [data-testid="stSidebar"] .stMultiSelect > div > div {
        background-color: rgba(255,255,255,0.07) !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        border-radius: 8px !important;
    }
                
    /* Cor do texto nos selects da Sidebar */
    [data-testid="stSidebar"] [data-testid="stSelectbox"] [data-baseweb="select"] div,
    [data-testid="stSidebar"] [data-testid="stSelectbox"] [data-baseweb="select"] span {
        color: rgba(255,255,255,0.85) !important;
    }
    [data-testid="stSidebar"] [data-testid="stSelectbox"] svg {
        fill: white !important;
    }

    /* Divisor sidebar */
    [data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.08) !important;
        margin: 16px 0 !important;
    }

    /* --- SPINNER --- */
    /* Main: fundo claro → texto escuro */
    [data-testid="stMain"] [data-testid="stSpinner"] p,
    [data-testid="stMain"] [data-testid="stSpinner"] span {
        color: var(--ex-black) !important;
    }

    /* Sidebar: fundo escuro → texto claro */
    [data-testid="stSidebar"] [data-testid="stSpinner"] p,
    [data-testid="stSidebar"] [data-testid="stSpinner"] span {
        color: rgba(255,255,255,0.85) !important;
    }

    /* --- RADIO (menu de seção na sidebar) --- */
    [data-testid="stSidebar"] .stRadio label {
        padding: 8px 10px !important;
        border-radius: 8px !important;
        transition: background 0.15s !important;
        color: rgba(255,255,255,0.55) !important;
        font-size: 13px !important;
    }

    [data-testid="stSidebar"] .stRadio label:hover {
        background: rgba(255,255,255,0.06) !important;
        color: rgba(255,255,255,0.9) !important;
    }

    /* Radio selecionado */
    [data-testid="stSidebar"] .stRadio [data-checked="true"] {
        background: var(--ex-purple) !important;
        color: #fff !important;
    }

    /* --- MÉTRICAS (st.metric) --- */
    [data-testid="stMetricContainer"] {
        background-color: var(--ex-white) !important;
        border: 1px solid var(--ex-border) !important;
        border-radius: 12px !important;
        padding: 16px !important;
        transition: border-color 0.2s !important;
    }

    [data-testid="stMetricContainer"]:hover {
        border-color: rgba(107,63,160,0.3) !important;
    }

    [data-testid="stMetricLabel"] {
        font-size: 10px !important;
        font-weight: 500 !important;
        letter-spacing: 1px !important;
        text-transform: uppercase !important;
        color: var(--ex-gray-dark) !important;
    }

    [data-testid="stMetricValue"] {
        font-family: 'DM Serif Display', serif !important;
        font-size: 28px !important;
        font-style: italic !important;
        color: var(--ex-black) !important;
        line-height: 1.1 !important;
    }

    [data-testid="stMetricDelta"] {
        font-size: 12px !important;
        font-weight: 500 !important;
    }

    /* --- BOTÕES --- */
    .stButton > button {
        background-color: var(--ex-purple) !important;
        color: #fff !important;
        border: none !important;
        border-radius: 8px !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        padding: 8px 20px !important;
        transition: background 0.15s !important;
        position: relative !important;
        z-index: 999 !important;
        pointer-events: auto !important;
        cursor: pointer !important;
    }

    .stButton {
        position: relative !important;
        z-index: 999 !important;
    }

    .stButton > button:hover {
        background-color: #5A348A !important;
    }

    /* Botão secundário */
    .stButton > button[kind="secondary"] {
        background-color: var(--ex-purple-light) !important;
        color: var(--ex-purple) !important;
        border: 1px solid rgba(107,63,160,0.2) !important;
    }

    /* --- TABS --- */
    .stTabs [data-baseweb="tab-list"] {
        background-color: var(--ex-gray) !important;
        border-radius: 10px !important;
        padding: 4px !important;
        gap: 2px !important;
        border-bottom: none !important;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: transparent !important;
        border-radius: 8px !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 12px !important;
        font-weight: 500 !important;
        color: var(--ex-gray-dark) !important;
        padding: 8px 16px !important;
        border: none !important;
    }

    .stTabs [aria-selected="true"] {
        background-color: var(--ex-white) !important;
        color: var(--ex-black) !important;
        box-shadow: 0 1px 4px rgba(0,0,0,0.08) !important;
    }

    /* --- SELECTBOX / INPUTS (MAIN) --- */
    .stSelectbox > div > div,
    .stMultiSelect > div > div {
        border: 1px solid var(--ex-border) !important;
        border-radius: 8px !important;
        background-color: var(--ex-white) !important;
    }

    /* Texto e Seta no Main */
    [data-testid="stMain"] [data-testid="stSelectbox"] [data-baseweb="select"] div,
    [data-testid="stMain"] [data-testid="stSelectbox"] [data-baseweb="select"] span {
        color: var(--ex-black) !important;
    }
    [data-testid="stMain"] [data-testid="stSelectbox"] svg {
        fill: var(--ex-black) !important;
    }

    .stSelectbox > div > div:focus-within,
    .stMultiSelect > div > div:focus-within {
        border-color: var(--ex-purple) !important;
        box-shadow: 0 0 0 2px rgba(107,63,160,0.15) !important;
    }

    /* --- LABELS DOS INPUTS --- */
    .stSelectbox label,
    .stMultiSelect label,
    .stDateInput label,
    .stNumberInput label,
    .stTextInput label {
        font-size: 11px !important;
        font-weight: 500 !important;
        letter-spacing: 0.8px !important;
        text-transform: uppercase !important;
        color: var(--ex-gray-dark) !important;
        margin-bottom: 4px !important;
    }

    /* --- INPUTS UNIFICADOS (SELECT, TEXT, NUMBER) --- */
    /* Força o fundo branco e bordas padrão em todos os campos no Main */
    [data-testid="stMain"] .stSelectbox > div > div,
    [data-testid="stMain"] .stTextInput > div > div,
    [data-testid="stMain"] .stNumberInput > div > div,
    [data-testid="stMain"] div[data-baseweb="input"],
    [data-testid="stMain"] [data-testid="stNumberInput"] > div > div,
    [data-testid="stMain"] [data-testid="stNumberInput"] div[data-baseweb="input"] {
        background-color: var(--ex-white) !important;
        border: 1px solid var(--ex-border) !important;
        border-radius: 8px !important;
    }

    /* NumberInput: container principal (envolve botões + input) - ALTA SPECIFICITY */
    [data-testid="stMain"] div[data-testid="stNumberInput"] > div,
    [data-testid="stMain"] div[data-testid="stNumberInput"] > div > div {
        background-color: var(--ex-white) !important;
        border: 1px solid var(--ex-border) !important;
        border-radius: 8px !important;
    }

    /* NumberInput: container interno do input (onde digita o número) */
    [data-testid="stMain"] .stNumberInput > div > div,
    [data-testid="stMain"] [data-testid="stNumberInput"] > div > div {
        background-color: var(--ex-white) !important;
    }

    /* NumberInput: TODOS os containers internos */
    [data-testid="stMain"] .stNumberInput > div,
    [data-testid="stMain"] .stNumberInput > div > div,
    [data-testid="stMain"] .stNumberInput > div > div > div,
    [data-testid="stMain"] [data-testid="stNumberInput"] > div,
    [data-testid="stMain"] [data-testid="stNumberInput"] > div > div,
    [data-testid="stMain"] [data-testid="stNumberInput"] > div > div > div {
        background-color: var(--ex-white) !important;
    }

    /* Esconde os botões de + e - para um visual clean de digitação */
    [data-testid="stMain"] .stNumberInput button,
    [data-testid="stMain"] [data-testid="stNumberInput"] button {
        display: none !important;
    }

    /* Ajuste fino do texto digitado e do cursor */
    [data-testid="stMain"] input,
    [data-testid="stMain"] [data-testid="stNumberInput"] input {
        color: var(--ex-black) !important;
        caret-color: var(--ex-black) !important;
        cursor: text !important;
        padding-left: 12px !important;
        background-color: transparent !important;
    }

    /* Cursor (caret) piscando - animação de foco */
    [data-testid="stMain"] input:focus,
    [data-testid="stMain"] [data-testid="stNumberInput"] input:focus {
        caret-color: var(--ex-purple) !important;
        animation: cursor-blink 1s infinite;
    }

    @keyframes cursor-blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0; }
    }

    /* Remove a borda/tracejado branco que aparece ao clicar */
    [data-testid="stMain"] input:focus,
    [data-testid="stMain"] [data-testid="stNumberInput"] input:focus {
        outline: none !important;
        box-shadow: none !important;
    }

    /* Placeholder legível (Dica interna da caixa) */
    [data-testid="stMain"] input::placeholder,
    [data-testid="stMain"] [data-testid="stNumberInput"] input::placeholder {
        color: rgba(26, 26, 26, 0.4) !important;
    }

    /* X de limpar o campo (clear button) — ícone preto */
    [data-testid="stMain"] [data-baseweb="input"] [data-baseweb="clear-icon"],
    [data-testid="stMain"] [data-baseweb="input"] button[aria-label="Clear value"],
    [data-testid="stMain"] [data-baseweb="input"] button svg,
    [data-testid="stMain"] [data-baseweb="input"] button svg path,
    [data-testid="stMain"] div[data-baseweb="input"] svg {
        color: var(--ex-black) !important;
        fill: var(--ex-black) !important;
        stroke: var(--ex-black) !important;
        opacity: 0.5 !important;
    }

    [data-testid="stMain"] [data-baseweb="input"] button:hover svg,
    [data-testid="stMain"] [data-baseweb="input"] button:hover svg path,
    [data-testid="stMain"] div[data-baseweb="input"] button:hover svg {
        opacity: 1 !important;
    }

    /* Efeito de foco roxo ao clicar */
    [data-testid="stMain"] div[data-baseweb="input"]:focus-within,
    [data-testid="stMain"] [data-testid="stNumberInput"] div[data-baseweb="input"]:focus-within {
        border-color: var(--ex-purple) !important;
        box-shadow: 0 0 0 2px rgba(107,63,160,0.15) !important;
    }

    /* Selectbox foco no Main */
    [data-testid="stMain"] .stSelectbox > div > div:focus-within,
    [data-testid="stMain"] .stMultiSelect > div > div:focus-within {
        border-color: var(--ex-purple) !important;
        box-shadow: 0 0 0 2px rgba(107,63,160,0.15) !important;
    }

    /* Container interno do NumberInput */
    [data-testid="stMain"] .stNumberInput [data-baseweb="input"],
    [data-testid="stMain"] [data-testid="stNumberInput"] [data-baseweb="input"] {
        background-color: var(--ex-white) !important;
    }

    /* --- CABEÇALHOS DA PÁGINA --- */
    h1 {
        font-family: 'DM Serif Display', serif !important;
        font-style: italic !important;
        font-size: 28px !important;
        color: var(--ex-black) !important;
        font-weight: 400 !important;
        letter-spacing: -0.5px !important;
    }

    h2 {
        font-family: 'DM Sans', sans-serif !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        letter-spacing: 1.2px !important;
        text-transform: uppercase !important;
        color: var(--ex-black) !important;
        margin-top: 8px !important;
    }

    h3 {
        font-family: 'DM Sans', sans-serif !important;
        font-size: 12px !important;
        font-weight: 500 !important;
        color: var(--ex-gray-dark) !important;
    }

    /* --- DATAFRAMES / TABELAS --- */
    [data-testid="stDataFrame"] {
        border: 1px solid var(--ex-border) !important;
        border-radius: 12px !important;
        overflow: hidden !important;
    }

    /* --- DIVISORES --- */
    hr {
        border: none !important;
        border-top: 1px solid var(--ex-border) !important;
        margin: 20px 0 !important;
    }

    /* --- EXPANDERS --- */
    .streamlit-expanderHeader {
        font-size: 13px !important;
        font-weight: 500 !important;
        color: var(--ex-black) !important;
        background-color: var(--ex-gray) !important;
        border-radius: 8px !important;
        padding: 10px 14px !important;
    }

    /* --- CAIXAS DE ALERTA (success / warning / error / info) --- */
    [data-testid="stAlert"] {
        border-radius: 10px !important;
        border-left-width: 4px !important;
    }

    /* --- SPINNER --- */
    .stSpinner > div {
        border-top-color: var(--ex-purple) !important;
    }

    /* --- SCROLLBAR GLOBAL --- */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: var(--ex-gray-mid); border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--ex-gray-dark); }
    
    /* Slider fora da sidebar */
    [data-testid="stMain"] .stSlider label,
    [data-testid="stMain"] .stSlider [data-testid="stTickBar"] {
        color: var(--ex-black) !important;
    }

    /* Garante que iframes de componentes customizados não bloqueiem cliques */
    iframe {
        pointer-events: none !important;
    }

    /* Reativa pointer-events apenas dentro dos iframes (afeta só o conteúdo externo) */
    .stButton, .stButton > button,
    .stTextInput, .stNumberInput, .stSelectbox,
    [data-testid="stWidgetLabel"] {
        pointer-events: auto !important;
    }

    /* --- RODAPÉ HIDE --- */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
                
    div[data-baseweb="popover"],
    div[data-baseweb="menu"] {
        background-color: var(--ex-white) !important;
        color: var(--ex-black) !important;
    }

    /* Itens da lista */
    div[role="option"] {
        color: var(--ex-black) !important;
        background-color: var(--ex-white) !important;
    }

    /* Hover */
    div[role="option"]:hover {
        background-color: var(--ex-purple-light) !important;
        color: var(--ex-black) !important;
    }

    /* Esconde o overlay "Press Enter to apply" do Streamlit */
    [data-testid="stNumberInputInstructions"],
    [data-testid="InputInstructions"] {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        pointer-events: none !important;
        height: 0 !important;
        overflow: hidden !important;
        position: absolute !important;
    }

    /* Remove a barrinha/linha branca que aparece embaixo do number input ao digitar */
    [data-testid="stMain"] .stNumberInput [data-baseweb="input"]::after,
    [data-testid="stMain"] .stNumberInput [data-baseweb="input"]::before,
    [data-testid="stMain"] .stNumberInput > div > div::after,
    [data-testid="stMain"] .stNumberInput > div > div::before,
    [data-testid="stMain"] [data-testid="stNumberInput"] [data-baseweb="input"]::after,
    [data-testid="stMain"] [data-testid="stNumberInput"] [data-baseweb="input"]::before {
        display: none !important;
        content: none !important;
        border: none !important;
        background: none !important;
    }

    /* Garante que o input interno não mostre borda/sublinhado extra */
    [data-testid="stMain"] .stNumberInput input,
    [data-testid="stMain"] [data-testid="stNumberInput"] input {
        border: none !important;
        box-shadow: none !important;
        outline: none !important;
    }

    </style>
    """, unsafe_allow_html=True)


# =============================================
# COMPONENTES HELPER
# =============================================
# =============================================

def chart_card(title: str, fig, height: int = 720, return_html: bool = False):
    """Renderiza ou retorna HTML de um card de gráfico Plotly."""

    fig.update_layout(
        autosize=True,
        height=560,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=0, b=20, l=0, r=0),
    )
    fig.update_layout(
        font=dict(color="#1F2937"),
        xaxis=dict(
            showgrid=False,
            zeroline=False
        ),
        yaxis=dict(
            gridcolor="rgba(0,0,0,0.05)",
            zeroline=False
        ),
    )
    fig.update_traces(
        hovertemplate="%{y:,.2f}<extra></extra>"
    )

    chart_html = fig.to_html(
        full_html=False,
        include_plotlyjs='cdn',
        config={'displayModeBar': False, 'responsive': True},
    )

    html_str = f"""
    <div style="background:#ffffff; border:1px solid rgba(26,26,26,0.12); border-radius:12px; padding:18px 20px 16px; margin-bottom:16px;">
        <div style="font-size:13px; font-weight:600; color:#6B6963; margin-bottom:14px;">{title}</div>
        <div style="width:100%; min-height:560px;">
            {chart_html}
        </div>
    </div>
    """

    if return_html:
        return html_str
    else:
        html(html_str, height=height, scrolling=True)

def kpi_card(label, value, delta=None, delta_type="neutral", color="default", return_html: bool = False):
    """
    Renderiza ou retorna HTML de um card de KPI.

    color: "default" | "purple" | "green" | "red" | "amber"
    delta_type: "positive" | "negative" | "neutral"
    """

    colors = {
        "purple": ("var(--ex-purple-light)", "var(--ex-purple)"),
        "green":  ("var(--ex-green-light)",  "var(--ex-green)"),
        "red":    ("var(--ex-red-light)",    "var(--ex-red)"),
        "amber":  ("var(--ex-amber-light)",  "var(--ex-amber)"),
        "default":("#FAFAF8",                "rgba(26,26,26,0.1)"),
    }

    bg, border = colors.get(color, colors["default"])

    delta_colors = {
        "positive": "var(--ex-green)",
        "negative": "var(--ex-red)",
        "neutral":  "var(--ex-gray-dark)",
    }

    delta_color = delta_colors.get(delta_type, "var(--ex-gray-dark)")

    delta_html = (
        f'<div style="font-size:12px;font-weight:500;color:{delta_color};margin-top:6px">{delta}</div>'
        if delta else ""
    )

    html_str = f"""
    <div style="
        background:{bg};
        border:1px solid {border};
        border-radius:12px;
        padding:16px;
        height:100%;
    ">
        <div style="font-size:10px;font-weight:500;letter-spacing:1px;text-transform:uppercase;color:var(--ex-gray-dark);margin-bottom:8px">{label}</div>
        <div style="font-family:'DM Serif Display',serif;font-size:28px;font-style:italic;color:var(--ex-black);line-height:1.1">{value}</div>
        {delta_html}
    </div>
    """

    if return_html:
        return html_str
    else:
        st.markdown(html_str, unsafe_allow_html=True)


def section_header(title, pill_text=None):
    """Cabeçalho de seção com pílula de badge opcional."""
    pill = f'<span style="font-size:10px;font-weight:500;padding:3px 10px;border-radius:10px;background:var(--ex-purple-light);color:var(--ex-purple);margin-left:10px">{pill_text}</span>' if pill_text else ""
    st.markdown(f"""
    <div style="display:flex;align-items:center;margin-bottom:12px">
        <span style="font-size:11px;font-weight:600;letter-spacing:1.5px;text-transform:uppercase;color:var(--ex-black)">{title}</span>
        {pill}
    </div>
    """, unsafe_allow_html=True)


def sidebar_logo():
    """Renderiza o logo na sidebar."""
    st.sidebar.markdown("""
    <div style="padding:8px 0 16px">
        <div style="font-family:'DM Serif Display',serif;font-size:20px;font-style:italic;color:#FAFAF8;line-height:1.1">
            Meu Exagerado
        </div>
        <div style="font-size:10px;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,0.3);margin-top:3px;font-weight:300">
            Dashboard
        </div>
    </div>
    <hr style="border:none;border-top:1px solid rgba(255,255,255,0.08);margin:0 0 16px">
    """, unsafe_allow_html=True)

def _df_to_html_rows(
    df: pd.DataFrame,
    col_labels: dict = None,
    col_formats: dict = None
) -> str:

    if hasattr(df, "data"):
        df = df.data

    cols = list(df.columns)
    labels = col_labels or {}
    formats = col_formats or {}

    # HEADER
    header_cells = "".join(
        f'<th style="'
        f'padding:10px 14px;'
        f'font-size:10px;font-weight:600;letter-spacing:1.2px;text-transform:uppercase;'
        f'color:#6B6963;border-bottom:1px solid rgba(26,26,26,0.08);'
        f'text-align:left;white-space:nowrap;">'
        f'{labels.get(c, c)}</th>'
        for c in cols
    )

    row_html = ""

    for i, (_, row) in enumerate(df.iterrows()):
        bg = "#ffffff" if i % 2 == 0 else "#FAFAF8"
        cells = ""

        for c in cols:
            val = row[c]

            # 🎯 FORMATAÇÃO
            if c in formats:
                try:
                    formatted = formats[c](val)
                except:
                    formatted = str(val)
            else:
                if isinstance(val, float):
                    formatted = f"{val:.2f}"
                elif val is None:
                    formatted = "—"
                else:
                    formatted = str(val)

            # 🎨 ESTILOS DINÂMICOS
            style_extra = ""

            # 🥇 destaque top 1
            if c == "Posição":
                if val == "🥇":
                    style_extra += "font-weight:700;font-size:15px;"
                elif val in ["🥈", "🥉"]:
                    style_extra += "font-weight:600;"

            # 💰 destacar faturamento alto (primeira linha geralmente)
            if c == "Faturamento" and i == 0:
                style_extra += "font-weight:700;color:#0A7A33;"

            # 📊 destacar proporção alta
            if c == "Proporção":
                try:
                    if val >= 0.5:
                        style_extra += "font-weight:700;color:#B00020;"
                    elif val >= 0.3:
                        style_extra += "font-weight:600;"
                except:
                    pass

            # 🧾 nome do produto mais importante (top 1)
            if c == "nome_produto" and i == 0:
                style_extra += "font-weight:600;"

            cells += (
                f'<td style="'
                f'padding:10px 14px;font-size:13px;color:#1A1A1A;'
                f'border-bottom:1px solid rgba(26,26,26,0.05);'
                f'{style_extra}">'
                f'{formatted}</td>'
            )

        row_html += f'<tr style="background:{bg};">{cells}</tr>'

    return f"""
    <table style="width:100%;border-collapse:collapse;">
        <thead><tr>{header_cells}</tr></thead>
        <tbody>{row_html}</tbody>
    </table>
    """
 
 
def table_card(
    df: pd.DataFrame,
    col_labels: dict = None,
    col_formats: dict = None,
    title: str = None,
    return_html: bool = False 
):
    """
    Renderiza um DataFrame como card estilizado OU retorna HTML.
    """

    if hasattr(df, "data"):
        df = df.data

    title_html = ""
    if title:
        title_html = f"""
        <div style="
            font-size:11px;font-weight:600;letter-spacing:1.5px;
            text-transform:uppercase;color:#6B6963;
            margin-bottom:14px;
        ">{title}</div>
        """

    table_html = _df_to_html_rows(df, col_labels, col_formats)

    html_block = f"""
    <div style="
        background:#ffffff;
        box-shadow: 0 4px 16px rgba(0,0,0,0.06);
        border:none;
        border-radius:12px;
        padding:18px 20px;
        margin-bottom:16px;
        overflow-x:auto;
    ">
        {title_html}
        {table_html}
    </div>
    """

    if return_html:
        return html_block

    n_rows = len(df)
    card_height = 56 + (n_rows * 42) + (44 if title else 0) + 24

    html(html_block, height=card_height, scrolling=False)
 