import streamlit as st
import pandas as pd
from datetime import datetime
import streamlit.components.v1 as components
import time

# Configuração da página
st.set_page_config(page_title="Registro de SKUs", page_icon="📦", layout="centered")

# Inicializa a tabela no session_state
if 'skus' not in st.session_state:
    st.session_state.skus = pd.DataFrame(columns=['SKU', 'Data/Hora'])

# Função para adicionar SKU
def add_sku(sku):
    if sku:  # Só adiciona se não for vazio
        # Validação simples do SKU (pode ser personalizada)
        if len(sku) < 3:
            st.session_state.last_sku_status = "error"
            st.session_state.last_sku_message = "SKU muito curto (mín. 3 caracteres)"
            return False
        
        new_row = pd.DataFrame({
            'SKU': [sku.upper()],  # Converte para maiúsculas
            'Data/Hora': [datetime.now().strftime('%d/%m/%Y %H:%M:%S')]
        })
        st.session_state.skus = pd.concat([st.session_state.skus, new_row], ignore_index=True)
        st.session_state.last_sku_status = "success"
        st.session_state.last_sku_message = f"SKU {sku} adicionado com sucesso!"
        return True
    return False

# Componente HTML/JS com foco automático
html_code = """
<div style="text-align: center; margin-bottom: 20px;">
    <h3 style="color: #333;">Digite o SKU e pressione Enter</h3>
    <input id="sku_input" type="text" placeholder="Ex: ABC12345" autofocus
           style="font-size: 18px; padding: 12px 20px; width: 300px;
                  border: 2px solid #4a90e2; border-radius: 25px;
                  outline: none; box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                  text-align: center; display: block; margin: 0 auto;" />
    <div id="status_message" style="height: 24px; margin-top: 8px;"></div>
</div>

<script>
// Função para focar no input (redundante com autofocus, mas útil como fallback)
function focusInput() {
    const input = document.getElementById('sku_input');
    input.focus();
}

// Verifica se há mensagem de status para exibir
if (window.parent.stSessionState && window.parent.stSessionState.last_sku_message) {
    const statusDiv = document.getElementById('status_message');
    const status = window.parent.stSessionState.last_sku_status;
    const message = window.parent.stSessionState.last_sku_message;
    
    statusDiv.textContent = message;
    statusDiv.style.color = status === 'success' ? 'green' : 'red';
    statusDiv.style.fontWeight = 'bold';
    
    // Limpa a mensagem após 3 segundos
    setTimeout(() => {
        statusDiv.textContent = '';
        window.parent.stSessionState.last_sku_message = '';
    }, 3000);
}

// Configura o listener para o evento Enter
const input = document.getElementById('sku_input');
input.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        const sku = this.value.trim();
        if (sku) {
            // Envia os dados para o Streamlit
            window.parent.postMessage({
                type: 'streamlit:setComponentValue',
                value: sku
            }, '*');
            
            // Limpa o campo e mantém o foco
            this.value = '';
            setTimeout(focusInput, 10);
        }
    }
});

// Foca no input quando a página carrega
document.addEventListener('DOMContentLoaded', focusInput);
// Foca no input sempre que o componente é atualizado
focusInput();
</script>
"""

# Título da aplicação
st.title("📦 Sistema de Registro de SKUs")

# Cria um placeholder para o componente
input_placeholder = st.empty()
status_placeholder = st.empty()

# Exibe o componente HTML
with input_placeholder:
    components.html(html_code, height=180)

# Verifica se há dados recebidos
if 'streamlit:setComponentValue' in st.session_state:
    sku = st.session_state['streamlit:setComponentValue']
    if add_sku(sku):
        st.rerun()
    else:
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
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Limpar Todos os SKUs", type="primary"):
            st.session_state.skus = pd.DataFrame(columns=['SKU', 'Data/Hora'])
            st.session_state.last_sku_status = "info"
            st.session_state.last_sku_message = "Todos os SKUs foram removidos"
            st.rerun()
    with col2:
        if st.button("Exportar para CSV"):
            csv = st.session_state.skus.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Baixar CSV",
                data=csv,
                file_name='skus_registrados.csv',
                mime='text/csv'
            )
else:
    st.info("Nenhum SKU registrado ainda. Digite um SKU acima e pressione Enter.")

# Adiciona um pouco de espaço no final
st.markdown("<br><br>", unsafe_allow_html=True)
