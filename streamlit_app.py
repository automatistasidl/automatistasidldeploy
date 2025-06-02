import streamlit as st

# Título da página
st.title("Consultar SKU")

# Campo de entrada de texto
sku = st.text_input("Digite o SKU", key="sku_input")

# Inserir o código HTML + JavaScript para foco automático
st.markdown("""
    <script>
        window.onload = function() {
            setTimeout(function() {
                document.getElementById("sku_input").focus();
            }, 100);  // Atraso de 100ms para garantir que o campo esteja renderizado
        }
    </script>
""", unsafe_allow_html=True)

# Mostrar o valor digitado
if sku:
    st.write(f"Você digitou: {sku}")
