import streamlit as st

# Definir o título
st.title("Consultar SKU")

# Script JavaScript para dar foco ao campo
st.markdown("""
    <script>
    document.addEventListener("DOMContentLoaded", function() {
        document.getElementById("sku_input").focus();
    });
    </script>
""", unsafe_allow_html=True)

# Campo de entrada de texto
sku = st.text_input("Digite o SKU", key="sku_input")

# Mostrar valor digitado
if sku:
    st.write(f"Você digitou: {sku}")
