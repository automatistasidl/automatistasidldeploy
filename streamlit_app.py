import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from datetime import datetime

# Inicializa a tabela no session_state
if 'skus' not in st.session_state:
    st.session_state.skus = pd.DataFrame(columns=['SKU', 'Data/Hora'])

# Função para adicionar SKU
def add_sku(sku):
    if sku:  # Só adiciona se não for vazio
        new_row = pd.DataFrame({
            'SKU': [sku],
            'Data/Hora': [datetime.now().strftime('%d/%m/%Y %H:%M:%S')]
        })
        st.session_state.skus = pd.concat([st.session_state.skus, new_row], ignore_index=True)

# Componente HTML/JS
html_code = f"""
<script>
function sendSkuToPython(sku) {{
    // Usa o Streamlit para enviar dados para o Python
    parent.window.streamlitAPI.runScript({{
        "is_sku": true,
        "sku_value": sku
    }});
}}

document.addEventListener('DOMContentLoaded', function() {{
    const input = document.getElementById('sku_input');
    input.focus();
    
    input.addEventListener('keypress', function(e) {{
        if (e.key === 'Enter') {{
            const sku = this.value.trim();
            if (sku) {{
                sendSkuToPython(sku);
                this.value = '';
                setTimeout(() => input.focus(), 50);  // Garante o foco
            }}
        }}
    }});
}});
</script>

<style>
    #sku_input {{
        font-size: 18px;
        padding: 12px 20px;
        width: 300px;
        border: 2px solid #4a90e2;
        border-radius: 25px;
        outline: none;
        transition: all 0.3s;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        text-align: center;
        display: block;
        margin: 0 auto;
    }}
    #sku_input:focus {{
        border-color: #FF5733;
        box-shadow: 0 0 8px rgba(255, 87, 51, 0.6);
    }}
</style>

<div style="text-align: center; margin-bottom: 20px;">
    <h3 style="color: #333;">Digite o SKU e pressione Enter</h3>
    <input id="sku_input" type="text" placeholder="Ex: ABC12345" />
</div>
"""

# Exibe o componente
components.html(html_code, height=150)

# Processa os dados recebidos do JavaScript
if 'is_sku' in st.query_params and 'sku_value' in st.query_params:
    add_sku(st.query_params['sku_value'])
    st.query_params.clear()  # Limpa os parâmetros
    st.rerun()  # Atualiza a página para mostrar a tabela

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
    
    # Botão para limpar a tabela
    if st.button("Limpar Todos os SKUs", type="primary"):
        st.session_state.skus = pd.DataFrame(columns=['SKU', 'Data/Hora'])
        st.rerun()
else:
    st.info("Nenhum SKU registrado ainda. Digite um SKU acima e pressione Enter.")

# CSS adicional para melhorar a tabela
st.markdown("""
<style>
    .stDataFrame [data-testid='stDataFrameContainer'] {
        border: 1px solid #e1e4e8;
        border-radius: 8px;
    }
    .stButton>button {
        background-color: #FF5733;
        color: white;
        border: none;
    }
    .stButton>button:hover {
        background-color: #E04B2D;
    }
</style>
""", unsafe_allow_html=True)
