import streamlit as st
import streamlit.components.v1 as components

# Título da página
st.title("Consultar SKU")

# Campo de entrada de texto
sku = st.text_input("Digite o SKU", key="sku_input")

# Mostrar o valor digitado
if sku:
    st.write(f"Você digitou: {sku}")

# Inserir HTML com JavaScript para focar no campo de entrada de SKU
html_code = """
    <html>
        <head>
            <style>
                #sku_input {
                    font-size: 20px;
                    color: #FF5733;
                    cursor: pointer;
                }
            </style>
        </head>
        <body>
            <input id="sku_input" type="text" value="" placeholder="Digite o SKU" />

            <script>
                // Focar no campo de entrada de SKU após o carregamento da página
                window.onload = function() {
                    document.getElementById("sku_input").focus();
                };
            </script>
        </body>
    </html>
"""

# Exibe o HTML e JavaScript
components.html(html_code, height=200)
