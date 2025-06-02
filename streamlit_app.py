import streamlit as st

# Campo de entrada de texto
sku = st.text_input("Digite o SKU", key="sku_input")

# Script para focar o campo automaticamente
st.markdown(
    """
    <script>
        const sleep = (ms) => new Promise(r => setTimeout(r, ms));
        window.onload = async function() {
            await sleep(100);  // Aguarda a renderização
            const inputElements = parent.document.querySelectorAll("input");
            for (let input of inputElements) {
                if (input.placeholder === "Digite o SKU") {
                    input.focus();
                    break;
                }
            }
        }
    </script>
    """,
    unsafe_allow_html=True
)

# Título da página
st.title("Consultar SKU")

# Mostrar valor digitado
if sku:
    st.write(f"Você digitou: {sku}")
