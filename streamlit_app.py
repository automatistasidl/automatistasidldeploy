import streamlit as st
import pandas as pd
from datetime import datetime
import streamlit.components.v1 as components
import time

# Configuração da página
st.set_page_config(page_title="Registro de Bultos", page_icon="📦", layout="centered")

# Estados da aplicação
if 'current_step' not in st.session_state:
    st.session_state.current_step = 1  # 1=Usuário, 2=Bulto, 3=SKUs
    st.session_state.user = None
    st.session_state.bulto = None
    st.session_state.skus = pd.DataFrame(columns=['Usuário', 'Bulto', 'SKU', 'Data/Hora'])
    st.session_state.current_skus = []
    st.session_state.last_action = None

# Funções auxiliares
def register_user(user):
    if user and len(user) >= 3:
        st.session_state.user = user.upper()
        st.session_state.current_step = 2
        st.session_state.last_action = {'type': 'user', 'value': user}
        return True
    return False

def register_bulto(bulto):
    if bulto and len(bulto) >= 3:
        st.session_state.bulto = bulto.upper()
        st.session_state.current_step = 3
        st.session_state.last_action = {'type': 'bulto', 'value': bulto}
        return True
    return False

def add_sku(sku):
    if sku and len(sku) >= 3:
        sku = sku.upper()
        st.session_state.current_skus.append(sku)
        st.session_state.last_action = {'type': 'sku', 'value': sku}
        return True
    return False

def finalize_bulto():
    if st.session_state.user and st.session_state.bulto and st.session_state.current_skus:
        new_rows = pd.DataFrame({
            'Usuário': [st.session_state.user] * len(st.session_state.current_skus),
            'Bulto': [st.session_state.bulto] * len(st.session_state.current_skus),
            'SKU': st.session_state.current_skus,
            'Data/Hora': [datetime.now().strftime('%d/%m/%Y %H:%M:%S')] * len(st.session_state.current_skus)
        })
        st.session_state.skus = pd.concat([st.session_state.skus, new_rows], ignore_index=True)
        st.session_state.current_skus = []
        st.session_state.last_action = {'type': 'finalize', 'value': st.session_state.bulto}
        st.session_state.current_step = 2  # Volta para registrar novo bulto
        return True
    return False

# Componente HTML/JS com foco automático
def get_input_component():
    placeholder_text = ""
    input_id = ""
    
    if st.session_state.current_step == 1:
        placeholder_text = "Bipe o código do USUÁRIO e pressione Enter"
        input_id = "user_input"
    elif st.session_state.current_step == 2:
        placeholder_text = "Bipe o código do BULTO e pressione Enter"
        input_id = "bulto_input"
    else:
        placeholder_text = "Bipe o SKU e pressione Enter (ou Finalizar Bulto)"
        input_id = "sku_input"

    html_code = f"""
    <div style="text-align: center; margin-bottom: 20px;">
        <h3 style="color: #333;">{placeholder_text}</h3>
        <input id="{input_id}" type="text" autofocus
               style="font-size: 18px; padding: 12px 20px; width: 300px;
                      border: 2px solid #4a90e2; border-radius: 25px;
                      outline: none; box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                      text-align: center; display: block; margin: 0 auto;" />
        <div id="status_message" style="height: 24px; margin-top: 8px;"></div>
    </div>

    <script>
    function focusInput() {{
        const input = document.getElementById('{input_id}');
        input.focus();
    }}

    // Exibe mensagem de status se houver
    if (window.parent.stSessionState && window.parent.stSessionState.last_action) {{
        const lastAction = window.parent.stSessionState.last_action;
        const statusDiv = document.getElementById('status_message');
        
        if (lastAction.type === 'user') {{
            statusDiv.textContent = `Usuário ${{lastAction.value}} registrado`;
            statusDiv.style.color = 'green';
        }} else if (lastAction.type === 'bulto') {{
            statusDiv.textContent = `Bulto ${{lastAction.value}} registrado`;
            statusDiv.style.color = 'green';
        }} else if (lastAction.type === 'sku') {{
            statusDiv.textContent = `SKU ${{lastAction.value}} adicionado`;
            statusDiv.style.color = 'green';
        }} else if (lastAction.type === 'finalize') {{
            statusDiv.textContent = `Bulto ${{lastAction.value}} finalizado!`;
            statusDiv.style.color = 'blue';
        }}
        
        statusDiv.style.fontWeight = 'bold';
        setTimeout(() => {{ statusDiv.textContent = ''; }}, 3000);
    }}

    // Configura o listener para o evento Enter
    const input = document.getElementById('{input_id}');
    input.addEventListener('keypress', function(e) {{
        if (e.key === 'Enter') {{
            const value = this.value.trim();
            if (value) {{
                window.parent.postMessage({{
                    type: 'streamlit:setComponentValue',
                    value: value
                }}, '*');
                
                this.value = '';
                setTimeout(focusInput, 10);
            }}
        }}
    }});

    // Foca no input
    document.addEventListener('DOMContentLoaded', focusInput);
    focusInput();
    </script>
    """
    return html_code

# Interface principal
st.title("📦 Sistema de Registro de Bultos")

# Mostra o estado atual
with st.expander("Progresso Atual", expanded=True):
    if st.session_state.user:
        st.success(f"👤 Usuário: {st.session_state.user}")
    else:
        st.warning("👤 Usuário: Não registrado")
    
    if st.session_state.bulto:
        st.success(f"📦 Bulto: {st.session_state.bulto}")
    else:
        st.warning("📦 Bulto: Não registrado")
    
    if st.session_state.current_step == 3:
        st.info(f"📝 Adicionando SKUs ao bulto {st.session_state.bulto}")
        if st.session_state.current_skus:
            st.write("SKUs neste bulto:")
            for sku in st.session_state.current_skus:
                st.write(f"- {sku}")

# Componente de entrada
input_placeholder = st.empty()
with input_placeholder:
    components.html(get_input_component(), height=180)

# Botão para finalizar bulto (apenas na etapa 3)
if st.session_state.current_step == 3:
    if st.button("✅ Finalizar Bulto", type="primary", use_container_width=True):
        if finalize_bulto():
            st.rerun()

# Processa entrada do usuário
if 'streamlit:setComponentValue' in st.session_state:
    value = st.session_state['streamlit:setComponentValue']
    
    if st.session_state.current_step == 1:
        register_user(value)
    elif st.session_state.current_step == 2:
        register_bulto(value)
    elif st.session_state.current_step == 3:
        add_sku(value)
    
    st.rerun()

# Exibe todos os registros
if not st.session_state.skus.empty:
    st.write("### Registros Completos")
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
    
    # Opções de exportação
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Limpar Todos os Registros", type="secondary"):
            st.session_state.skus = pd.DataFrame(columns=['Usuário', 'Bulto', 'SKU', 'Data/Hora'])
            st.rerun()
    with col2:
        csv = st.session_state.skus.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Exportar para CSV",
            data=csv,
            file_name='registros_bultos.csv',
            mime='text/csv',
            use_container_width=True
        )
else:
    st.info("Nenhum registro completo ainda. Comece bipando o usuário.")

# Adiciona um pouco de espaço no final
st.markdown("<br><br>", unsafe_allow_html=True)
