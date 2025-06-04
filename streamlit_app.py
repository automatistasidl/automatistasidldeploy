import streamlit as st
import pandas as pd
from datetime import datetime
import streamlit.components.v1 as components

# Configuração da página
st.set_page_config(page_title="Registro de Bultos", page_icon="📦", layout="centered")

# Estados da aplicação
if 'app_data' not in st.session_state:
    st.session_state.app_data = {
        'step': 1,  # 1=Usuário, 2=Bulto, 3=SKUs
        'user': '',
        'bulto': '',
        'skus': pd.DataFrame(columns=['Usuário', 'Bulto', 'SKU', 'Data/Hora']),
        'current_skus': [],
        'message': '',
        'input_value': ''  # Novo estado para armazenar o valor de entrada
    }

# Funções auxiliares
def handle_input(value):
    current_step = st.session_state.app_data['step']
    
    if not value or len(value) < 3:
        st.session_state.app_data['message'] = "Mínimo 3 caracteres"
        return
    
    value = value.upper()
    
    if current_step == 1:
        st.session_state.app_data['user'] = value
        st.session_state.app_data['step'] = 2
        st.session_state.app_data['message'] = f"Usuário {value} registrado"
    elif current_step == 2:
        st.session_state.app_data['bulto'] = value
        st.session_state.app_data['step'] = 3
        st.session_state.app_data['message'] = f"Bulto {value} registrado"
    elif current_step == 3:
        st.session_state.app_data['current_skus'].append(value)
        st.session_state.app_data['message'] = f"SKU {value} adicionado"

def finalize_bulto():
    if st.session_state.app_data['current_skus']:
        new_rows = pd.DataFrame({
            'Usuário': [st.session_state.app_data['user']] * len(st.session_state.app_data['current_skus']),
            'Bulto': [st.session_state.app_data['bulto']] * len(st.session_state.app_data['current_skus']),
            'SKU': st.session_state.app_data['current_skus'],
            'Data/Hora': [datetime.now().strftime('%d/%m/%Y %H:%M:%S')] * len(st.session_state.app_data['current_skus'])
        })
        
        st.session_state.app_data['skus'] = pd.concat(
            [st.session_state.app_data['skus'], new_rows], 
            ignore_index=True
        )
        
        st.session_state.app_data['current_skus'] = []
        st.session_state.app_data['step'] = 2
        st.session_state.app_data['message'] = f"Bulto {st.session_state.app_data['bulto']} finalizado!"
        st.session_state.app_data['bulto'] = ''

# Componente HTML/JS - Atualizado para comunicação correta
def get_input_component():
    step = st.session_state.app_data['step']
    message = st.session_state.app_data['message']
    
    placeholders = {
        1: "Bipe o USUÁRIO e pressione Enter",
        2: "Bipe o BULTO e pressione Enter",
        3: "Bipe o SKU e pressione Enter"
    }
    
    html = f"""
    <div style="text-align: center; margin-bottom: 20px;">
        <h3 style="color: #333;">{placeholders[step]}</h3>
        <input id="main_input" type="text" autofocus
               style="font-size: 18px; padding: 12px 20px; width: 300px;
                      border: 2px solid #4a90e2; border-radius: 25px;
                      outline: none; box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                      text-align: center; display: block; margin: 0 auto;" />
        <div id="message" style="height: 24px; margin-top: 8px; color: green; font-weight: bold;">
            {message}
        </div>
    </div>

    <script>
    const input = document.getElementById("main_input");
    
    // Foco automático
    function focusInput() {{
        input.focus();
    }}
    
    // Envia valor para o Streamlit
    function sendValue(value) {{
        const data = {{
            input_value: value
        }};
        window.parent.document.dispatchEvent(
            new CustomEvent("SET_INPUT_VALUE", {{ detail: data }})
        );
    }}
    
    // Evento de tecla
    input.addEventListener("keypress", function(e) {{
        if (e.key === "Enter") {{
            const value = this.value.trim();
            if (value) {{
                sendValue(value);
                this.value = "";
                setTimeout(focusInput, 10);
            }}
        }}
    }});
    
    // Limpa mensagem após 3 segundos
    setTimeout(() => {{
        document.getElementById("message").textContent = "";
    }}, 3000);
    
    // Foco inicial
    focusInput();
    </script>
    """
    return html

# Listener para eventos personalizados
components.html(
    """
    <script>
    window.addEventListener("load", function() {
        window.parent.document.addEventListener("SET_INPUT_VALUE", function(e) {
            const data = e.detail;
            Streamlit.setComponentValue(data.input_value);
        });
    });
    </script>
    """, 
    height=0
)

# Interface principal
st.title("📦 Sistema de Registro de Bultos")

# Mostra estado atual
with st.expander("Progresso Atual", expanded=True):
    cols = st.columns(2)
    cols[0].metric("👤 Usuário", st.session_state.app_data['user'] or "Não registrado")
    cols[1].metric("📦 Bulto", st.session_state.app_data['bulto'] or "Não registrado")
    
    if st.session_state.app_data['step'] == 3:
        st.write("📝 SKUs neste bulto:")
        for sku in st.session_state.app_data['current_skus']:
            st.write(f"- {sku}")

# Componente de entrada
input_value = components.html(get_input_component(), height=180)

# Processa entrada do usuário
if input_value:
    handle_input(input_value)
    st.session_state.app_data['input_value'] = input_value
    st.rerun()

# Botão para finalizar bulto
if st.session_state.app_data['step'] == 3:
    if st.button("✅ Finalizar Bulto", type="primary", use_container_width=True):
        finalize_bulto()
        st.rerun()

# Exibe registros completos
if not st.session_state.app_data['skus'].empty:
    st.write("### Registros Completos")
    st.dataframe(
        st.session_state.app_data['skus'],
        use_container_width=True,
        hide_index=True,
        column_config={
            "Data/Hora": st.column_config.DatetimeColumn(
                format="DD/MM/YYYY HH:mm:ss"
            )
        }
    )
    
    # Opções de exportação
    cols = st.columns(2)
    with cols[0]:
        if st.button("Limpar Registros", type="secondary"):
            st.session_state.app_data['skus'] = pd.DataFrame(columns=['Usuário', 'Bulto', 'SKU', 'Data/Hora'])
            st.rerun()
    with cols[1]:
        csv = st.session_state.app_data['skus'].to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Exportar para CSV",
            data=csv,
            file_name='registros_bultos.csv',
            mime='text/csv',
            use_container_width=True
        )
else:
    st.info("Nenhum registro completo ainda. Comece bipando o usuário.")

# Espaço final
st.markdown("<br><br>", unsafe_allow_html=True)
