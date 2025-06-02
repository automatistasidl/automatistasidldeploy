import streamlit as st

# Título da página
st.title("Consultar SKU")

# Campo de entrada de texto
sku = st.text_input("Digite o SKU", key="sku_input")

# Mostrar o valor digitado
if sku:
    st.write(f"Você digitou: {sku}")
