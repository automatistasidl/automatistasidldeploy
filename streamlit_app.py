import streamlit as st

# Título da página
st.title("Consultar SKU")

# Campo de entrada de texto
sku = st.text_input("Digite o SKU", key="sku_input")

# Adicionar código JavaScript para selecionar o texto automaticamente no campo de entrada
st.markdown("""
    <script>
        window.onload = function() {
            var skuInput = document.getElementById("sku_input");
            if (skuInput) {
                skuInput.select();  // Seleciona o texto no campo de entrada
                skuInput.focus();   // Foca no campo de entrada
            }
        }
    </script>
""", unsafe_allow_html=True)

# Mostrar o valor digitado
if sku:
    st.write(f"Você digitou: {sku}")
