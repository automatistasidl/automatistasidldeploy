import streamlit as st

# Definir o título da página
st.title("Consultar SKU")

# Adicionar o código JavaScript para forçar o foco
st.markdown("""
    <script>
        window.addEventListener('load', function() {
            setTimeout(function() {
                document.getElementById("sku_input").focus();
            }, 100);  // Atrasar o foco para garantir que o campo seja renderizado primeiro
        });
    </script>
""", unsafe_allow_html=True)

# Campo de entrada de texto
sku = st.text_input("Digite o SKU", key="sku_input")

# Mostrar o valor digitado
if sku:
    st.write(f"Você digitou: {sku}")
