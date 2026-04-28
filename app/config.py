# Configurações globais do Streamlit
import streamlit as st

# URL para o banco de dados PostgreSQL, armazenada em secrets.toml
DATABASE_URL = st.secrets["postgres"]["url"]