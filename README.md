# Exagerado Insights Dashboard

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-FF4B4B?logo=streamlit)
![Plotly](https://img.shields.io/badge/Visualização-Plotly-3F4F75?logo=plotly)
![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-336791?logo=postgresql)
![Status](https://img.shields.io/badge/Status-Development-yellow)

---

## Visão Geral

Dashboard analítico construído em **Streamlit** para visualização em tempo real das vendas processadas pela API do **Exagerado Insights**.

O sistema consome dados do PostgreSQL e transforma informações operacionais em **KPIs, gráficos, relatórios automatizados e prints enviados para WhatsApp via backend**.

O objetivo é fornecer uma camada visual estratégica para tomada de decisão rápida em operações de varejo.

---

## Estrutura
├── app/
│ ├── dashboard.py # Interface principal Streamlit
│ ├── services.py # Lógica de renderização dos dashboards por loja
│ ├── config.py # Configurações e secrets
│ ├── database.py # Conexão com PostgreSQL
│ ├── exagerado_theme.py # Componentes visuais (cards, tabelas, charts)
│ ├── utils.py # Funções auxiliares
│ └── assets/ # Estilos e recursos visuais
├── requirements.txt # Dependências Python
├── .streamlit/
│ └── secrets.toml # Secrets do Streamlit
├── README.md # Documentação
└── app.log # Logs do dashboard

---

## Arquitetura

### Fluxo de Dados
PostgreSQL (API Backend)
↓
Streamlit App
↓
Consulta SQL (SQLAlchemy / pandas)
↓
Processamento (KPIs + agregações)
↓
Renderização (Plotly + HTML + Streamlit UI)
↓
Exportação de relatório (PNG via Playwright)
↓
Envio para Backend (FastAPI /alerts/send-print)

---

## Funcionalidades

### 📊 Dashboard por Loja
- KPIs em tempo real:
  - Faturamento total
  - Número de vendas
  - Ticket médio
  - Projeção de faturamento

---

### 📈 Análises Visuais
- Faturamento por dia
- Faturamento por hora
- Top produtos por:
  - faturamento
  - quantidade
  - tendência recente

---

### 📅 Tabela Analítica
- Desempenho diário consolidado
- Pivot de vendas por data
- Totais automáticos

---

### 📦 Ranking de Produtos
- Top 5 produtos por loja
- Indicadores visuais (🥇🥈🥉)
- Proporção de faturamento

---

### 📸 Geração de Relatórios
- Exportação de dashboard em **imagem PNG**
- Renderização via Playwright (HTML → Screenshot)
- Envio automático para backend

---

## Integração com Backend

O frontend se conecta diretamente com a API:

### Endpoint de envio de print

```python
POST /alerts/send-print
```

### Payload enviado

- `loja_id` → ID da loja selecionada
- `file` → imagem PNG gerada do dashboard
- `token` → autenticação via query param

---

### Fluxo de envio

1. Usuário clica em **“Gerar relatório”**
2. Dashboard renderiza HTML da seção
3. HTML é convertido em PNG (Playwright)
4. Arquivo é enviado via HTTP POST para API
5. Backend processa e envia via WhatsApp

---

## Configuração

### Variáveis do Streamlit

Arquivo `.streamlit/secrets.toml`:

```toml
[api]
URL_API = "http://localhost:8000/alerts/send-print"
WEBHOOK_TOKEN = "seu_token_secreto"

[database]
DATABASE_URL = "postgresql://user:password@localhost:5432/exagerado_db"
```

## Instalação

### Local

pip install -r requirements.txt
streamlit run app/dashboard.py


## Dependências principais

 - Streamlit — UI do dashboard
 - Pandas — manipulação de dados
 - Plotly — gráficos interativos
 - SQLAlchemy — conexão com banco
 - Requests — comunicação com API
 - Playwright — geração de imagens (HTML → PNG)

## Geração de Relatórios

### Pipeline

HTML (dashboard renderizado)
    ↓
Playwright Chromium
    ↓
Screenshot full page
    ↓
PNG salvo localmente
    ↓
Upload para API FastAPI
    ↓
Envio WhatsApp

## Estrutura do Dashboard

### Renderização modular

Cada loja é renderizada por:

```python
render_secao_loja(df_loja, nome_loja, loja_id)
```
Componentes:

 - KPIs (cards)
 - gráficos (Plotly)
 - tabelas (Streamlit custom)
 - insights automáticos
 - ranking de produtos

### Mapeamento de Lojas

Exemplo:

```python

map_lojas = {
    "Loja ES": 205906072,
    "Loja RJ": 205906073
}

```
## Autor

**Kauã Dias**  
Estudante de Estatística | Data Science | Automação com Python

- GitHub: [Kauadp](https://github.com/Kauadp)
- LinkedIn: [kauad](https://www.linkedin.com/in/kauad/)

---