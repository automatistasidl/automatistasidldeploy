import streamlit as st
from streamlit_javascript import st_javascript

# Configuração da página
st.set_page_config(layout="wide")

# Função para focar no campo de texto
def focus_on_input():
    st_javascript("""
    setTimeout(() => {
        const inputs = window.parent.document.querySelectorAll('input[type="text"]');
        if (inputs.length > 0) {
            inputs[0].focus();
        }
    }, 100);
    """)

# Título da aplicação
st.title("Exemplo de Foco Automático")

# Adicionando estilo CSS para destacar o campo com foco
st.markdown("""
    <style>
        .focused-field {
            border: 2px solid #4CAF50 !important;
            box-shadow: 0 0 8px #4CAF50 !important;
        }
    </style>
""", unsafe_allow_html=True)

# Campo de texto que receberá o foco
nome = st.text_input("Digite seu nome:", key="nome_input")

# Chamada para focar no campo
focus_on_input()

# Botão de submissão
if st.button("Enviar"):
    if nome:
        st.success(f"Olá, {nome}! Seja bem-vindo(a).")
    else:
        st.warning("Por favor, digite seu nome.")
