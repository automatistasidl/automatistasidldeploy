import streamlit as st
import streamlit.components.v1 as components

# Configuração da página
st.set_page_config(layout="wide")

# Título da aplicação
st.title("Sistema com Foco Automático")

# Solução que funciona com components.html
def focused_text_input(label, key):
    # Gerar um ID único baseado na key
    input_id = f"input_{key}"
    
    # HTML e JavaScript para o campo com foco automático
    html = f"""
    <div>
        <label for="{input_id}" style="font-size: 16px; color: black;">{label}</label>
        <input id="{input_id}" type="text" style="
            width: 100%;
            padding: 8px;
            margin-top: 4px;
            font-size: 16px;
            border: 2px solid #4CAF50;
            border-radius: 4px;
        "/>
        <script>
            document.getElementById("{input_id}").focus();
            
            // Atualizar o Streamlit quando o valor mudar
            document.getElementById("{input_id}").addEventListener("input", function(e) {{
                Streamlit.setComponentValue(e.target.value);
            }});
        </script>
    </div>
    """
    
    # Chamar o componente e obter o valor
    value = components.html(html, height=70, key=key)
    
    return value

# Uso do campo com foco automático
st.write("### Exemplo de Campo com Foco Automático")
user_input = focused_text_input("Digite o SKU:", "sku_input")

if user_input:
    st.success(f"Você digitou: {user_input}")

# Versão alternativa usando st.text_input + JavaScript (menos recomendada)
st.write("### Método Alternativo (pode não funcionar em todos os navegadores)")
alternative_input = st.text_input("Digite outra informação:", key="alt_input")

components.html(f"""
    <script>
        setTimeout(() => {{
            var inputs = window.parent.document.querySelectorAll('input[type="text"]');
            inputs.forEach(input => {{
                if (input.value === "" && input.getAttribute("data-testid") === "textInput") {{
                    input.focus();
                    input.scrollIntoView();
                }}
            }});
        }}, 200);
    </script>
""", height=0)
