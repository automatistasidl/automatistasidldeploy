import streamlit as st
import streamlit.components.v1 as components

# Inserir HTML com JavaScript para focar no campo de entrada de SKU e capturar a leitura completa do scanner
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

                let timer;

                // Detecta a alteração no input e verifica se o scanner terminou de ler
                document.getElementById("sku_input").addEventListener("input", function() {
                    clearTimeout(timer);  // Limpa o timer anterior
                    timer = setTimeout(function() {
                        var skuValue = document.getElementById("sku_input").value;
                        if (skuValue.trim() !== "") {
                            alert("Você digitou: " + skuValue);
                        }
                    }, 500);  // Aguarda 500ms para verificar se o scanner terminou de enviar o código
                });
            </script>
        </body>
    </html>
"""

# Exibe o HTML e JavaScript
components.html(html_code, height=200)
