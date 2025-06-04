import streamlit as st
import pandas as pd
from datetime import datetime
import streamlit.components.v1 as components
import json

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

# Componente HTML/JS com comunicação correta
html_code = """
<div style="text-align: center; margin-bottom: 20px;">
    <h3 style="color: #333;">Digite o SKU e pressione Enter</h3>
    <input id="sku_input" type="text" placeholder="Ex: ABC12345" 
           style="font-size: 18px; padding: 12px 20px; width: 300px;
                  border: 2px solid #4a90e2; border-radius: 25px;
                  outline: none; box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                  text-align: center; display: block; margin: 0 auto;" />
</div>

<script>
const input = document.getElementById('sku_input');
input.focus();

input.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        const sku = this.value.trim();
        if (sku) {
            // Envia o valor para o Streamlit
            Streamlit.setComponentValue(sku);
            this.value = '';
            setTimeout(() => input.focus(), 10);
        }
    }
});
</script>
"""

# Cria e renderiza o componente
sku_input = components.html(
    html_code, 
    height=150, 
    key="sku_input_component"
)

# Verifica se há novo SKU recebido
if sku_input is not None:
    add_sku(sku_input)
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
