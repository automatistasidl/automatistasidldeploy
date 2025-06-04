import streamlit as st
import pandas as pd
from datetime import datetime
import streamlit.components.v1 as components

# Inicializa a tabela no session_state
if 'skus' not in st.session_state:
    st.session_state.skus = pd.DataFrame(columns=['SKU', 'Data/Hora'])
if 'input_counter' not in st.session_state:
    st.session_state.input_counter = 0

# Incrementa o contador para forçar um novo input
st.session_state.input_counter += 1

# Cria o campo de texto com uma chave única baseada no contador
input_key = f"sku_input_{st.session_state.input_counter}"
sku_input = st.text_input(
    "Digite o SKU e pressione Enter", 
    placeholder="Ex: ABC12345",
    key=input_key,
    autofocus=True
)

# JavaScript para focar automaticamente no campo
components.html(
    f"""
    <script>
        window.addEventListener('load', function() {{
            setTimeout(function() {{
                var input = document.querySelector('input[data-testid="stTextInput"]');
                if (input) {{
                    input.focus();
                }}
            }}, 100);
        }});
    </script>
    """,
    height=0
)

# Quando Enter é pressionado no campo de texto
if sku_input:
    # Adiciona à tabela
    new_row = pd.DataFrame({
        'SKU': [sku_input],
        'Data/Hora': [datetime.now().strftime('%d/%m/%Y %H:%M:%S')]
    })
    st.session_state.skus = pd.concat([st.session_state.skus, new_row], ignore_index=True)
    
    # Força a recriação do campo para limpá-lo
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
