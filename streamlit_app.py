import streamlit as st

# Definir o título da página
st.title("Consultar SKU")

# Criar o campo de entrada de texto para SKU
sku = st.text_input("Digite o SKU", key='sku_input')

# Se o SKU for inserido, você pode exibir algo
if sku:
    st.write(f"Você digitou: {sku}")
