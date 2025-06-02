import streamlit as st

# Título da página
st.title("Consultar SKU")

# Campo de entrada
sku = st.text_input("Digite o SKU", key='sku_input')

# JavaScript para focar automaticamente no primeiro campo de input
st.markdown("""
    <script>
        const sleep = (time) => new Promise((resolve) => setTimeout(resolve, time));
        window.onload = async function() {
            await sleep(100);  // Aguarda um pouco para garantir que o input foi carregado
            const input = window.parent.document.querySelector('input');
            if (input) {
                input.focus();
            }
        }
    </script>
""", unsafe_allow_html=True)

# Exibir resultado se o SKU for digitado
if sku:
    st.write(f"Você digitou: {sku}")
