import streamlit as st
import pandas as pd
from datetime import datetime

# Inicializa a tabela no session_state
if 'skus' not in st.session_state:
    st.session_state.skus = pd.DataFrame(columns=['SKU', 'Data/Hora'])

# Usamos um formulário para capturar o input e limpar o campo
with st.form(key='sku_form'):
    sku_input = st.text_input(
        "Digite o SKU e pressione Enter", 
        placeholder="Ex: ABC12345",
        key="sku_input"
    )
    submit_button = st.form_submit_button("Adicionar")

# Quando o formulário é submetido
if submit_button and sku_input:
    # Adiciona à tabela
    new_row = pd.DataFrame({
        'SKU': [sku_input],
        'Data/Hora': [datetime.now().strftime('%d/%m/%Y %H:%M:%S')]
    })
    st.session_state.skus = pd.concat([st.session_state.skus, new_row], ignore_index=True)
    
    # Não precisamos limpar manualmente, o formulário já faz isso

# Exibe a tabela de SKUs
if not st.session_state.skus.empty:
    st.write("### SKUs Registrados")
    st.dataframe(
        st.session_state.skus,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Data/Hora": st.column_config.DatetimeColumn(
                format="DD/MM/YYYY HH:mm:ss"
            )
        }
    )
    
    if st.button("Limpar Todos os SKUs", type="primary"):
        st.session_state.skus = pd.DataFrame(columns=['SKU', 'Data/Hora'])
        st.rerun()
else:
    st.info("Nenhum SKU registrado ainda. Digite um SKU acima e pressione o botão 'Adicionar'.")
