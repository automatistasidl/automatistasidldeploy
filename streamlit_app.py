import streamlit as st
import pandas as pd
from datetime import datetime
import streamlit.components.v1 as components

# Configuração da página
st.set_page_config(page_title="Registro de Bultos", page_icon="📦", layout="centered")

# Estados da aplicação
if 'app_state' not in st.session_state:
    st.session_state.app_state = {
        'current_step': 1,  # 1=Usuário, 2=Bulto, 3=SKUs
        'user': None,
        'bulto': None,
        'skus': pd.DataFrame(columns=['Usuário', 'Bulto', 'SKU', 'Data/Hora']),
        'current_skus': [],
        'last_message': ''
    }

# Funções auxiliares
def register_user(user):
    if user and len(user) >= 3:
        st.session_state.app_state['user'] = user.upper()
        st.session_state.app_state['current_step'] = 2
        st.session_state.app_state['last_message'] = f"Usuário {user.upper()} registrado"
        return True
    st.session_state.app_state['last_message'] = "Usuário inválido (mín. 3 caracteres)"
    return False

def register_bulto(bulto):
    if bulto and len(bulto) >= 3:
        st.session_state.app_state['bulto'] = bulto.upper()
        st.session_state.app_state['current_step'] = 3
        st.session_state.app_state['last_message'] = f"Bulto {bulto.upper()} registrado"
        return True
    st.session_state.app_state['last_message'] = "Bulto inválido (mín. 3 caracteres)"
    return False

def add_sku(sku):
    if sku and len(sku) >= 3:
        sku = sku.upper()
        st.session_state.app_state['current_skus'].append(sku)
        st.session_state.app_state['last_message'] = f"SKU {sku} adicionado"
        return True
    st.session_state.app_state['last_message'] = "SKU inválido (mín. 3 caracteres)"
    return False

def finalize_bulto():
    if (st.session_state.app_state['user'] and 
        st.session_state.app_state['bulto'] and 
        st.session_state.app_state['current_skus']):
        
        new_rows = pd.DataFrame({
            'Usuário': [st.session_state.app_state['user']] * len(st.session_state.app_state['current_skus']),
            'Bulto': [st.session_state.app_state['bulto']] * len(st.session_state.app_state['current_skus']),
            'SKU': st.session_state.app_state['current_skus'],
            'Data/Hora': [datetime.now().strftime('%d/%m/%Y %H:%M:%S')] * len(st.session_state.app_state['current_skus'])
        })
        
        st.session_state.app_state['skus'] = pd.concat(
            [st.session_state.app_state['skus'], new_rows], 
            ignore_index=True
        )
        
        st.session_state.app_state['current_skus'] = []
        st.session_state.app_state['current_step'] = 2
        st.session_state.app_state['last_message'] = f"Bulto {st.session_state.app_state['bulto']} finalizado!"
        st.session_state.app_state['bulto'] = None
        return True
    
    st.session_state.app_state['last_message'] = "Não há SKUs para finalizar"
    return False

# Componente HTML/JS com foco automático
def get_input_component():
    current_step = st.session_state.app_state['current_step']
    last_message = st.session_state.app_state['last_message']
    
    placeholders = {
        1: "Bipe o código do USUÁRIO e pressione Enter",
        2: "Bipe o código do BULTO e pressione Enter",
        3: "Bipe o SKU e pressione Enter"
    }
    
    input_id = f"step_{current_step}_input"
    placeholder_text = placeholders.get(current_step, "")
    
    # Cor da mensagem baseada no conteúdo
    message_color = "green"
    if "inválido" in last_message or "Não há" in last_message:
        message_color = "red"
    elif "finalizado" in last_message:
        message_color = "blue"
    
    html_code = f"""
    <div style="text-align: center; margin-bottom: 20px;">
        <h3 style="color: #333;">{placeholder_text}</h3>
        <input id="{input_id}" type="text" autofocus
               style="font-size: 18px; padding: 12px 20px; width: 300px;
                      border: 2px solid #4a90e2; border-radius: 25px;
                      outline: none; box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                      text-align: center; display: block; margin: 0 auto;" />
        <div id="status_message" style="height: 24px; margin-top: 8px; color: {message_color}; font-weight: bold;">
            {last_message}
        </div>
    </div>

    <script>
    // Função para enviar dados para o Streamlit
    function sendValue(value) {{
        const data = {{
            step: {current_step},
            value: value
        }};
        window.parent.postMessage({{
            type: 'streamlit:setComponentValue',
            data: data
        }}, '*');
    }}
    
    // Configura o input
    function setupInput() {{
        const input = document.getElementById("{input_id}");
        
        input.focus();
        
        input.addEventListener("keypress", function(e) {{
            if (e.key === "Enter") {{
                const value = this.value.trim();
                if (value) {{
                    sendValue(value);
                    this.value = "";
                    setTimeout(() => input.focus(), 10);
                }}
            }}
        }});
    }}
    
    // Inicializa
    document.addEventListener("DOMContentLoaded", setupInput);
    setupInput();
    
    // Limpa a mensagem após 3 segundos
    setTimeout(() => {{
        const msgDiv = document.getElementById("status_message");
        if (msgDiv) msgDiv.textContent = "";
    }}, 3000);
    </script>
    """
    return html_code

# Interface principal
st.title("📦 Sistema de Registro de Bultos")

# Mostra o estado atual
with st.expander("Progresso Atual", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        user = st.session_state.app_state['user'] or "Não registrado"
        st.metric("👤 Usuário", user)
    
    with col2:
        bulto = st.session_state.app_state['bulto'] or "Não registrado"
        st.metric("📦 Bulto", bulto)
    
    if st.session_state.app_state['current_step'] == 3:
        st.write("📝 SKUs neste bulto:")
        if st.session_state.app_state['current_skus']:
            for sku in st.session_state.app_state['current_skus']:
                st.write(f"- {sku}")
        else:
            st.write("Nenhum SKU registrado ainda")

# Componente de entrada
input_placeholder = st.empty()
with input_placeholder:
    components.html(get_input_component(), height=180)

# Botão para finalizar bulto (apenas na etapa 3)
if st.session_state.app_state['current_step'] == 3:
    if st.button("✅ Finalizar Bulto", type="primary", use_container_width=True):
        finalize_bulto()
        st.rerun()

# Processa entrada do usuário
if 'streamlit:setComponentValue' in st.session_state:
    data = st.session_state['streamlit:setComponentValue'].get('data', {})
    value = data.get('value', '')
    step = data.get('step', 0)
    
    if step == 1:
        register_user(value)
    elif step == 2:
        register_bulto(value)
    elif step == 3:
        add_sku(value)
    
    if 'streamlit:setComponentValue' in st.session_state:
        del st.session_state['streamlit:setComponentValue']
    st.rerun()

# Exibe todos os registros
if not st.session_state.app_state['skus'].empty:
    st.write("### Registros Completos")
    st.dataframe(
        st.session_state.app_state['skus'],
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
            st.session_state.app_state['skus'] = pd.DataFrame(columns=['Usuário', 'Bulto', 'SKU', 'Data/Hora'])
            st.rerun()
    with col2:
        csv = st.session_state.app_state['skus'].to_csv(index=False).encode('utf-8')
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
