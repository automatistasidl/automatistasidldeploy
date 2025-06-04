import streamlit as st
import pandas as pd
from datetime import datetime

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
        'input_value': '',
        'focus_trigger': 0  # Gatilho para focar no campo
    }

# Funções auxiliares
def handle_input(value):
    if not value or len(value) < 3:
        st.session_state.app_data['message'] = "Mínimo 3 caracteres"
        return
    
    value = value.upper()
    current_step = st.session_state.app_data['step']
    
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
    
    # Limpa o campo e aciona o foco
    st.session_state.app_data['input_value'] = ''
    st.session_state.app_data['focus_trigger'] += 1

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
        st.session_state.app_data['focus_trigger'] += 1

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
placeholders = {
    1: "Bipe o USUÁRIO e pressione Enter",
    2: "Bipe o BULTO e pressione Enter",
    3: "Bipe o SKU e pressione Enter"
}

input_value = st.text_input(
    placeholders[st.session_state.app_data['step']],
    value=st.session_state.app_data['input_value'],
    key='main_input',
    on_change=lambda: handle_input(st.session_state.main_input),
    label_visibility='collapsed'
)

# Script avançado para manter o foco
focus_trigger = st.session_state.app_data['focus_trigger']
st.markdown(f"""
<script>
// Gatilho para focar quando necessário
const focusTrigger = {focus_trigger};

function focusInput() {{
    const input = document.querySelector('input[aria-label="main_input"]');
    if (input) {{
        input.focus();
        
        // Move o cursor para o final do texto
        const value = input.value;
        input.value = '';
        input.value = value;
    }}
}}

// Foca imediatamente se o campo estiver visível
if (document.readyState === 'complete') {{
    focusInput();
}} else {{
    document.addEventListener('DOMContentLoaded', focusInput);
}}

// Observa mudanças no DOM para manter o foco
const observer = new MutationObserver((mutations) => {{
    mutations.forEach((mutation) => {{
        if (!mutation.addedNodes) return;
        focusInput();
    }});
}});

observer.observe(document.body, {{
    childList: true,
    subtree: true,
    attributes: false,
    characterData: false
}});

// Foca quando a página ganha visibilidade
document.addEventListener('visibilitychange', () => {{
    if (document.visibilityState === 'visible') {{
        focusInput();
    }}
}});
</script>
""", unsafe_allow_html=True)

# Exibe mensagens
if st.session_state.app_data['message']:
    st.success(st.session_state.app_data['message'])
    # Limpa a mensagem após 3 segundos
    st.session_state.app_data['message'] = ''

# Botão para finalizar bulto
if st.session_state.app_data['step'] == 3:
    if st.button("✅ Finalizar Bulto", type="primary", use_container_width=True):
        finalize_bulto()

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
