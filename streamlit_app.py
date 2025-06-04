import streamlit as st
import pandas as pd
import pygsheets
import os
import datetime
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components
from datetime import datetime
import io
import smtplib
from email.message import EmailMessage
import pytz
import re

def hora_brasil():
    fuso_brasil = pytz.timezone('America/Sao_Paulo')
    return datetime.now(fuso_brasil).strftime("%d/%m/%Y %H:%M:%S")

# Inicializar session_state
if "cadastros" not in st.session_state:
    st.session_state["cadastros"] = []

# Estados do aplicativo
if "etapa" not in st.session_state:
    st.session_state.etapa = "bulto"  # bulto -> categoria -> sku

# Configuração da página
st.set_page_config(layout="wide")

# CSS personalizado
st.markdown("""
    <style>
        .css-1omjdxh {
            color: white !important;
        }
        .big-font {
            font-size: 30px !important;
            text-align: center;
            margin: 10px 0;
        }
        .category-btn {
            height: 100px !important;
            font-size: 24px !important;
            margin: 10px 0;
            width: 100%;
        }
        .change-btn {
            background-color: #FFA500 !important;
            color: white !important;
            font-weight: bold;
        }
        .change-btn:hover {
            background-color: #FF8C00 !important;
            border-color: #FF8C00 !important;
        }
        .stButton>button {
            height: 60px !important;
            font-size: 20px !important;
        }
        .footer {
            position: fixed;
            bottom: 0;
            right: 10px;
            font-size: 12px;
            text-align: right;
            background-color: #9DD1F1;
            color: black;
            padding: 5px;
            z-index: 100;
        }
        /* Estilo para o campo de entrada com foco */
        .focused-input {
            border: 3px solid #4A90E2 !important;
            box-shadow: 0 0 10px #4A90E2 !important;
        }
        .error-message {
            color: red;
            font-weight: bold;
            margin-top: 5px;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# Funções de validação
def validar_usuario(usuario):
    if len(usuario) != 24:
        return False, "Usuário deve ter exatamente 24 caracteres, certifique-se de que bipou o usuário corretamente."
    return True, ""

def validar_bulto(bulto):
    if len(bulto) != 24:
        return False, "Bulto deve ter exatamente 24 caracteres"
    if not bulto.isdigit():
        return False, "Bulto deve conter apenas números"
    return True, ""

def validar_sku(sku):
    if len(sku) != 14:
        return False, "SKU deve ter exatamente 14 caracteres"
    if not sku.isdigit():
        return False, "SKU deve conter apenas números"
    return True, ""

# Função para foco automático corrigida
def auto_focus_input():
    components.html(f"""
    <script>
    function focusSkuInput() {{
        // Encontrar o campo pelo placeholder específico
        const inputs = Array.from(window.parent.document.querySelectorAll('input[type="text"]'));
        const targetInput = inputs.find(input => 
            input.placeholder === "Bipe o SKU e pressione Enter..." || 
            input.placeholder === "Digite o número do bulto..." ||
            input.placeholder === "Digite seu usuário:"
        );
        
        if (targetInput) {{
            // Destacar visualmente o campo com foco
            targetInput.classList.add('focused-input');
            
            // Focar sem selecionar o conteúdo
            targetInput.focus();
            
            // Remover destaque quando o campo perde foco
            targetInput.addEventListener('blur', () => {{
                targetInput.classList.remove('focused-input');
            }});
        }}
    }}
    
    // Focar imediatamente
    focusSkuInput();
    
    // Configurar um observador para quando o DOM for alterado
    const observer = new MutationObserver((mutations) => {{
        // Verificar se o campo de input foi adicionado
        mutations.forEach((mutation) => {{
            if (mutation.addedNodes.length) {{
                focusSkuInput();
            }}
        }});
    }});
    
    // Iniciar a observação
    observer.observe(window.parent.document.body, {{
        childList: true,
        subtree: true
    }});
    </script>
    """, height=0)

# Página de boas-vindas
if "inicio" not in st.session_state:
    st.session_state["inicio"] = False      

if not st.session_state["inicio"]:
    st.title("SISTEMA DE CONTROLE DE BACKSTOCK")
    if st.button("Iniciar"):
        with st.spinner("Carregando o sistema..."):
            import time
            time.sleep(2)
        st.success("Sistema carregado com sucesso! Vamos para a tela de usuário.")
        time.sleep(1)
        st.session_state["inicio"] = True
        st.rerun()

    st.image("https://f.hellowork.com/media/123957/1440_960/IDLOGISTICSFRANCE_123957_63809226079153822430064462.jpeg", use_container_width=True)
    st.stop()

# Cadastro obrigatório do usuário
if "user" not in st.session_state or not st.session_state["user"]:
    st.session_state["user"] = ""
    st.session_state["user_error"] = ""

if not st.session_state["user"]:
    st.title("Cadastro Obrigatório para continuar o acesso")
    
    # Campo de usuário com foco automático
    user = st.text_input("Digite seu usuário (max 24 caracteres):", 
                         key="user_input", 
                         placeholder="Digite seu usuário...",
                         max_chars=24)
    auto_focus_input()
    
    # Exibir erro se existir
    if st.session_state["user_error"]:
        st.markdown(f'<div class="error-message">{st.session_state["user_error"]}</div>', unsafe_allow_html=True)
    
    st.write(f"Usuário digitado: {user}")

    if user.strip():
        valido, mensagem = validar_usuario(user)
        if valido:
            st.session_state["user"] = user.strip()
            st.session_state["user_error"] = ""
            st.success(f"Usuário {user} cadastrado com sucesso!")
            st.rerun()
        else:
            st.session_state["user_error"] = mensagem
            st.rerun()
    else:
        st.warning("Por favor, digite um nome de usuário válido.")

    st.image("https://f.hellowork.com/media/123957/1440_960/IDLOGISTICSFRANCE_123957_63809226079153822430064462.jpeg", use_container_width=True)
    st.stop()

# Menu de navegação
selecao = option_menu(
    menu_title="BACKSTOCK",
    options=["Cadastro Bulto", "Tabela", "Home"],
    icons=["box", "table", "house"],
    menu_icon="cast",
    orientation="horizontal"
)

# Redireciona para tela de boas-vindas
if selecao == "Home":
    st.session_state["inicio"] = False
    st.session_state["user"] = ""
    st.session_state["bulto_cadastrado"] = False
    st.session_state.etapa = "bulto"
    st.session_state["user_error"] = ""
    st.rerun()

# Página de cadastro de bultos
if selecao == "Cadastro Bulto":
    # Etapa 1: Cadastro do bulto
    if st.session_state.etapa == "bulto":
        st.markdown("<h1 style='color:black; text-align: center;'>Cadastro de Bultos</h1>", unsafe_allow_html=True)
        st.markdown("<h2 style='color:black; text-align: center;'>Digite o número do bulto (24 números)</h2>", unsafe_allow_html=True)
        
        bulto = st.text_input("", 
                              key="bulto_input", 
                              placeholder="Digite o número do bulto...",
                              max_chars=40)
        auto_focus_input()
        
        # Validar bulto se foi digitado algo
        if bulto:
            valido, mensagem = validar_bulto(bulto)
            if valido:
                st.session_state["bulto_numero"] = bulto
                st.session_state["bulto_cadastrado"] = True
                st.session_state.etapa = "categoria"
                st.session_state["peca_reset_count"] = 0
                st.session_state["bulto_error"] = ""
                st.rerun()
            else:
                st.session_state["bulto_error"] = mensagem
                st.rerun()
        
        # Exibir erro se existir
        if "bulto_error" in st.session_state and st.session_state["bulto_error"]:
            st.markdown(f'<div class="error-message">{st.session_state["bulto_error"]}</div>', unsafe_allow_html=True)
    
    # Etapa 2: Seleção de categoria
    elif st.session_state.etapa == "categoria":
        st.markdown("<h1 style='color:black; text-align: center;'>Selecione a Categoria</h1>", unsafe_allow_html=True)
        st.markdown(f"<div class='big-font'>Bulto: {st.session_state['bulto_numero']}</div>", unsafe_allow_html=True)
        
        categorias = ["Ubicação", "Limpeza", "Tara Maior", "Costura", "Reetiquetagem"]
        cols = st.columns(2)
        
        for i, categoria in enumerate(categorias):
            col = cols[i % 2]
            with col:
                if st.button(categoria, key=f"cat_{categoria}", use_container_width=True):
                    st.session_state["categoria_selecionada"] = categoria
                    st.session_state.etapa = "sku"
                    st.rerun()
    
    # Etapa 3: Cadastro de SKUs
    elif st.session_state.etapa == "sku":
        st.markdown("<h1 style='color:black; text-align: center;'>Cadastro de Peças</h1>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"<div class='big-font'>Usuário: {st.session_state['user']}</div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='big-font'>Bulto: {st.session_state['bulto_numero']}</div>", unsafe_allow_html=True)
        with col3:
            st.markdown(f"<div class='big-font'>Categoria: {st.session_state['categoria_selecionada']}</div>", unsafe_allow_html=True)
        
        st.markdown(f"<div class='big-font'>Peças cadastradas: {st.session_state.get('peca_reset_count', 0)}</div>", unsafe_allow_html=True)
        
        # Botão para mudar de categoria
        if st.button("↩️ Mudar Categoria", key="mudar_categoria", use_container_width=True, type="secondary"):
            st.session_state.etapa = "categoria"
            st.rerun()
        
        # Campo para cadastro de SKU
        unique_key = f"sku_input_{st.session_state.get('peca_reset_count', 0)}"
        sku = st.text_input("Digite o SKU (14 números):", 
                            key=unique_key, 
                            placeholder="Bipe o SKU e pressione Enter...",
                            max_chars=40)
        
        # Foco automático otimizado
        auto_focus_input()
        
        # Exibir erro se existir
        if "sku_error" in st.session_state and st.session_state["sku_error"]:
            st.markdown(f'<div class="error-message">{st.session_state["sku_error"]}</div>', unsafe_allow_html=True)
        
        if sku:
            valido, mensagem = validar_sku(sku)
            if valido:
                novo_cadastro = {
                    "Usuário": st.session_state["user"],
                    "Bulto": st.session_state["bulto_numero"],
                    "SKU": sku,
                    "Categoria": st.session_state["categoria_selecionada"],
                    "Data/Hora": hora_brasil()
                }
                st.session_state["cadastros"].append(novo_cadastro)
                st.success(f"Peça '{sku}' cadastrada com sucesso!")
                st.session_state["peca_reset_count"] = st.session_state.get("peca_reset_count", 0) + 1
                st.session_state["sku_error"] = ""
                
                # Forçar rerun para limpar o campo e aplicar foco novamente
                st.rerun()
            else:
                st.session_state["sku_error"] = mensagem
                st.rerun()
        
        # Botão para finalizar bulto
        if st.button("✅ Finalizar Bulto", key="finalizar_bulto", use_container_width=True, type="primary"):
            if st.session_state.get("peca_reset_count", 0) > 0:
                # Filtrar apenas os cadastros do bulto atual
                bulto_atual = st.session_state["bulto_numero"]
                df_cadastros = pd.DataFrame([c for c in st.session_state["cadastros"] if c["Bulto"] == bulto_atual])
                
                if not df_cadastros.empty:
                    nome_arquivo = f"cadastro_bulto_{bulto_atual}_{datetime.now(pytz.timezone('America/Sao_Paulo')).strftime('%d-%m-%Y_%H-%M-%S')}.xlsx"
                    output = io.BytesIO()
                    df_cadastros.to_excel(output, index=False, engine='xlsxwriter')
                    dados_excel = output.getvalue()

                    try:
                        remetente = "automatistasidl@gmail.com"
                        senha = "ydlkjtswplqitwkf"
                        destinatario = "analista@idl.com"

                        msg = EmailMessage()
                        msg['Subject'] = f'Relatório - Bulto {bulto_atual}'
                        msg['From'] = remetente
                        msg['To'] = destinatario
                        msg.set_content(f'Segue em anexo a planilha do bulto finalizado: {bulto_atual}')
                        msg.add_attachment(dados_excel, maintype='application', subtype='vnd.openxmlformats-officedocument.spreadsheetml.sheet', filename=nome_arquivo)

                        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                            smtp.login(remetente, senha)
                            smtp.send_message(msg)

                        st.success("✅ Bulto finalizado e enviado com sucesso para o analista!")
                    except Exception as e:
                        st.error(f"❌ Erro ao enviar planilha: {e}")
                else:
                    st.warning("⚠️ Nenhuma peça cadastrada neste bulto para envio.")
            else:
                st.warning("⚠️ Nenhuma peça cadastrada neste bulto.")
            
            # Limpar estado do bulto atual
            st.session_state["bulto_cadastrado"] = False
            st.session_state["peca_reset_count"] = 0
            st.session_state.etapa = "bulto"
            st.rerun()

# Tabela de peças cadastradas
elif selecao == "Tabela":
    st.markdown("<h1 style='color:black; text-align: center;'>Tabela de Peças Cadastradas</h1>", unsafe_allow_html=True)

    if st.session_state["cadastros"]:
        df_cadastros = pd.DataFrame(st.session_state["cadastros"])
        st.dataframe(df_cadastros, use_container_width=True)
        
        nome_arquivo = f"cadastro_bultos_{datetime.now(pytz.timezone('America/Sao_Paulo')).strftime('%d-%m-%Y_%H-%M-%S')}.xlsx"
        output = io.BytesIO()
        df_cadastros.to_excel(output, index=False, engine='xlsxwriter')
        dados_excel = output.getvalue()

        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="📥 Baixar planilha Excel",
                data=dados_excel,
                file_name=nome_arquivo,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
        with col2:
            if st.button("✉️ Enviar planilha para analista", use_container_width=True):
                try:
                    remetente = "automatistasidl@gmail.com"
                    senha = "ydlkjtswplqitwkf"
                    destinatario = "analista@idl.com"

                    msg = EmailMessage()
                    msg['Subject'] = 'Relatório de Cadastro de Bultos'
                    msg['From'] = remetente
                    msg['To'] = destinatario
                    msg.set_content('Segue em anexo a planilha de cadastro de bultos.')
                    msg.add_attachment(dados_excel, maintype='application', subtype='vnd.openxmlformats-officedocument.spreadsheetml.sheet', filename=nome_arquivo)

                    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                        smtp.login(remetente, senha)
                        smtp.send_message(msg)

                    st.success("✅ Planilha enviada com sucesso para o analista!")
                except Exception as e:
                    st.error(f"❌ Erro ao enviar planilha: {e}")
        
        if st.button("🧹 Limpar todos os registros", type="secondary", use_container_width=True):
            st.session_state["cadastros"] = []
            st.success("Todos os registros foram limpos!")
            st.rerun()
    else:
        st.info("Nenhuma peça cadastrada até o momento.")

# Rodapé
st.markdown("""
    <div class="footer">
        Copyright © 2025 Direitos Autorais Desenvolvedor Rogério Ferreira
    </div>
""", unsafe_allow_html=True)
