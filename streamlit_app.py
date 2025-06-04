import streamlit as st
import streamlit.components.v1 as components

# HTML com CSS e JavaScript melhorados
html_code = """
<html>
    <head>
        <style>
            .input-container {
                display: flex;
                justify-content: center;
                padding: 20px;
            }
            
            #sku_input {
                font-size: 18px;
                padding: 12px 20px;
                width: 300px;
                border: 2px solid #4a90e2;
                border-radius: 25px;
                outline: none;
                transition: all 0.3s ease;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                text-align: center;
            }
            
            #sku_input:focus {
                border-color: #FF5733;
                box-shadow: 0 0 8px rgba(255, 87, 51, 0.6);
                transform: scale(1.02);
            }
            
            #sku_input::placeholder {
                color: #aaa;
                font-style: italic;
            }
            
            body {
                background-color: #f5f5f5;
                font-family: 'Arial', sans-serif;
            }
            
            .title {
                text-align: center;
                color: #333;
                margin-bottom: 20px;
                font-size: 24px;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <div class="title">Digite o SKU do produto</div>
        <div class="input-container">
            <input id="sku_input" type="text" value="" placeholder="Ex: ABC12345" />
        </div>

        <script>
            window.onload = function() {
                const input = document.getElementById("sku_input");
                input.focus();
                
                // Opcional: Limpar o placeholder quando em foco
                input.addEventListener('focus', function() {
                    this.placeholder = '';
                });
                
                input.addEventListener('blur', function() {
                    this.placeholder = 'Ex: ABC12345';
                });
            };
        </script>
    </body>
</html>
"""

# Exibe o HTML e JavaScript
components.html(html_code, height=200)
