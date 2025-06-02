import streamlit as st
import streamlit.components.v1 as components

# Inserir HTML com JavaScript para focar no campo de entrada de SKU e exibir o valor após pressionar Enter
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

                // Exibir valor do SKU ao pressionar "Enter"
                document.getElementById("sku_input").addEventListener("keypress", function(event) {
                    if (event.key === "Enter") {
                        var skuValue = document.getElementById("sku_input").value;
                        alert("Você digitou: " + skuValue);
                    }
                });
            </script>
        </body>
    </html>
"""

# Exibe o HTML e JavaScript
components.html(html_code, height=200)
