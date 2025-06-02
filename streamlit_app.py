import streamlit as st
import streamlit.components.v1 as components

# Definir título
st.title("Consultar SKU")

# Campo de entrada de texto
sku = st.text_input("Digite o SKU", key="sku_input")

# Código HTML + JS para focar o campo
components.html("""
    <script>
        window.onload = function() {
            var skuInput = document.getElementById("sku_input");
            if (skuInput) {
                skuInput.focus();
            }
        }
    </script>
""", height=0)

# Mostrar valor digitado
if sku:
    st.write(f"Você digitou: {sku}")
