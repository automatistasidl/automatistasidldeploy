import streamlit as st
import pandas as pd
from datetime import datetime

# Inicializa a tabela no session_state
if 'skus' not in st.session_state:
    st.session_state.skus = pd.DataFrame(columns=['SKU', 'Data/Hora'])

# Cria um campo de texto no Streamlit
sku_input = st.text_input(
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
    
    # Limpa o campo usando a abordagem correta
    st.session_state.sku_input = ""
    # Força a atualização do componente
    st.experimental_rerun()

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
        st.experimental_rerun()
else:
    st.info("Nenhum SKU registrado ainda. Digite um SKU acima e pressione Enter.")
