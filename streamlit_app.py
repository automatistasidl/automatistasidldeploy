import streamlit as st

# Título da página
st.title("Consultar SKU")

# Campo de entrada de texto
sku = st.text_input("Digite o SKU", key="sku_input")

# Adicionar código JavaScript para focar o campo sem abrir o teclado
st.markdown("""
    <script>
        function focusWhithoutKeyboard(inputElement) {
            inputElement.setAttribute('readonly', 'readonly');
            inputElement.focus();
            setTimeout(function() {
                inputElement.removeAttribute('readonly');
            }, 100);
        }

        window.onload = function() {
            var inputElement = document.getElementById("sku_input");
            if (inputElement) {
                focusWhithoutKeyboard(inputElement);
            }
        }
    </script>
""", unsafe_allow_html=True)

# Mostrar o valor digitado
if sku:
    st.write(f"Você digitou: {sku}")
