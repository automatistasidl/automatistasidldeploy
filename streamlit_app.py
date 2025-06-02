import streamlit as st
import streamlit.components.v1 as components

# Definir o título
st.title("Consultar SKU")

# HTML + JS para foco no campo
components.html("""
    <script>
        document.addEventListener("DOMContentLoaded", function() {
            document.getElementById("sku_input").focus();
        });
    </script>
""", height=0)

# Campo de entrada de texto
sku = st.text_input("Digite o SKU", key="sku_input")

# Mostrar valor digitado
if sku:
    st.write(f"Você digitou: {sku}")
