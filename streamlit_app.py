import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

# Inicializa a tabela no session_state se não existir
if 'sku_table' not in st.session_state:
    st.session_state.sku_table = pd.DataFrame(columns=['SKU'])

# HTML com CSS, JavaScript e lógica para capturar Enter
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
            const input = document.getElementById("sku_input");
            
            // Focar no campo quando a página carregar
            window.onload = function() {
                input.focus();
            };
            
            // Capturar tecla Enter
            input.addEventListener("keypress", function(event) {
                if (event.key === "Enter") {
                    const skuValue = input.value.trim();
                    if (skuValue) {
                        // Enviar o valor para o Streamlit
                        parent.window.streamlitAPI.runScript(
                            {"data": skuValue, "isEnter": true}
                        );
                        
                        // Limpar o campo e manter o foco
                        input.value = '';
                        input.focus();
                    }
                }
            });
            
            // Opcional: Limpar placeholder quando em foco
            input.addEventListener('focus', function() {
                this.placeholder = '';
            });
            
            input.addEventListener('blur', function() {
                this.placeholder = 'Ex: ABC12345';
            });
        </script>
    </body>
</html>
"""

# Função para adicionar SKU à tabela
def add_sku(sku):
    new_row = pd.DataFrame({'SKU': [sku]})
    st.session_state.sku_table = pd.concat([st.session_state.sku_table, new_row], ignore_index=True)

# Componente HTML
components.html(html_code, height=200)

# Se recebermos dados via JavaScript
if st.experimental_get_query_params().get('isEnter'):
    sku = st.experimental_get_query_params().get('data')[0]
    add_sku(sku)
    st.experimental_set_query_params()  # Limpa os parâmetros

# Exibe a tabela de SKUs
if not st.session_state.sku_table.empty:
    st.write("### SKUs Adicionados")
    st.dataframe(st.session_state.sku_table, use_container_width=True)
    
    # Botão para limpar a tabela
    if st.button("Limpar Tabela"):
        st.session_state.sku_table = pd.DataFrame(columns=['SKU'])
        st.rerun()
