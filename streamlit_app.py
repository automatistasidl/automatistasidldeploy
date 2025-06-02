import streamlit as st

# Título da página
st.title("Consultar SKU")

# Campo de entrada de texto
sku = st.text_input("Digite o SKU:", key="sku_input")

# Verifica se o usuário digitou algo
if sku:
    st.success(f"Você digitou: {sku}")
