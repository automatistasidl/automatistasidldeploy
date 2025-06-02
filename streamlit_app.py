import streamlit as st

# Campo de entrada de texto
sku = st.text_input("Digite o SKU", key="sku_input")

# Script para focar o campo automaticamente
st.components.v1.html(
    """
    <script>
        const sleep = (ms) => new Promise(r => setTimeout(r, ms));
        window.addEventListener("load", async () => {
            await sleep(100);
            const input = window.parent.document.querySelector('input[placeholder="Digite o SKU"]');
            if (input) {
                input.focus();
            }
        });
    </script>
    """,
    height=0,
)
# Título da página
st.title("Consultar SKU")

# Mostrar valor digitado
if sku:
    st.write(f"Você digitou: {sku}")
