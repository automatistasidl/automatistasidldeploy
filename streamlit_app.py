import streamlit as st
import pandas as pd
from datetime import datetime

# Inicializa a tabela no session_state
if 'skus' not in st.session_state:
    st.session_state.skus = pd.DataFrame(columns=['SKU', 'Data/Hora'])

# Cria um container para o input
input_container = st.empty()
sku_input = input_container.text_input(
    "Digite o SKU e pressione Enter", 
    placeholder="Ex: ABC12345",
    key="sku_input"
)

# Quando Enter é pressionado no campo de texto
if sku_input:
    # Adiciona à tabela
    new_row = pd.DataFrame({
        'SKU': [sku_input],
        'Data/Hora': [datetime.now().strftime('%d/%m/%Y %H:%M:%S')]
    })
    st.session_state.skus = pd.concat([st.session_state.skus, new_row], ignore_index=True)
    
    # Recria o input para limpar o campo
    sku_input = input_container.text_input(
        "Digite o SKU e pressione Enter", 
        placeholder="Ex: ABC12345",
        key="sku_input_new"
    )
    st.rerun()

# Restante do código permanece igual...
