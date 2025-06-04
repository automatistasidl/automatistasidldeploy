import streamlit as st
import pandas as pd
from datetime import datetime

# Inicializa a tabela no session_state
if 'skus' not in st.session_state:
    st.session_state.skus = pd.DataFrame(columns=['SKU', 'Data/Hora'])
if 'clear_input' not in st.session_state:
    st.session_state.clear_input = False

# Cria um container para o input
input_container = st.empty()

# Lógica para limpar o input quando necessário
if st.session_state.clear_input:
    sku_input = input_container.text_input(
        "Digite o SKU e pressione Enter", 
        placeholder="Ex: ABC12345",
        key="sku_input_clear"
    )
    st.session_state.clear_input = False
else:
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
    
    # Marca para limpar o input na próxima renderização
    st.session_state.clear_input = True
    st.rerun()

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
    st.info("Nenhum SKU registrado ainda. Digite um SKU acima e pressione Enter.")
