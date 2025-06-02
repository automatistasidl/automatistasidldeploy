import streamlit as st

# Campo de entrada de texto
sku = st.text_input("Digite o SKU", key="sku_input")

# Título da página
st.result("Consultar SKU")

# Mostrar valor digitado
if sku:
    st.write(f"Você digitou: {sku}")
