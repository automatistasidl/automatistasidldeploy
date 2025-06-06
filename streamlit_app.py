import streamlit as st
import pandas as pd
import pytz
import requests
from io import StringIO
import smtplib
from email.message import EmailMessage
import io
from datetime import datetime
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components
import time

# Função para obter data/hora no fuso horário do Brasil
def hora_brasil():
    fuso_brasil = pytz.timezone('America/Sao_Paulo')
    return datetime.now(fuso_brasil).strftime("%d/%m/%Y %H:%M:%S")

# Função para validar o usuário na planilha do Google Sheets
def validar_usuario(codigo):
    try:
        # URL da planilha pública
        url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQT66XECK150fz-NTRkNAEtlmt1sjSnfCHScgYB812JXd7UHs2JadldU5jOnQaZG3MDA95eJdgH5PZE/pubhtml"
        
        # Carregar os dados
        response = requests.get(url)
        response.encoding = 'utf-8'
        csv_data = StringIO(response.text)
        df = pd.read_csv(csv_data)
        
        # Verificar se a planilha tem as colunas necessárias
        if 'Criptografia' not in df.columns or 'Usuário' not in df.columns:
            st.error("Estrutura da planilha inválida. Verifique as colunas.")
            return None
        
        # Normalizar os dados
        df['Criptografia'] = df['Criptografia'].astype(str).str.strip().str.lower()
        codigo = str(codigo).strip().lower()
        
        # Verificar se o código existe
        if codigo in df['Criptografia'].values:
            # Retornar o nome do usuário correspondente
            return df.loc[df['Criptografia'] == codigo, 'Usuário'].values[0]
        return None
    except Exception as e:
        st.error(f"Erro ao validar usuário: {str(e)}")
        return None

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
    </style>
""", unsafe_allow_html=True)

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
            input.placeholder === "Digite seu código de acesso:"
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
            time.sleep(2)
        st.success("Sistema carregado com sucesso! Vamos para a tela de usuário.")
        time.sleep(1)
        st.session_state["inicio"] = True
        st.rerun()

    st.image("https://f.hellowork.com/media/123957/1440_960/IDLOGISTICSFRANCE_123957_63809226079153822430064462.jpeg", use_container_width=True)
    st.stop()

# Cadastro obrigatório do usuário
if "user_code" not in st.session_state or not st.session_state["user_code"]:
    st.session_state["user_code"] = ""
    st.session_state["user_name"] = ""

if not st.session_state["user_code"]:
    st.title("Cadastro Obrigatório para continuar o acesso")

    # Campo de usuário com foco automático
    codigo_usuario = st.text_input("Digite seu código de acesso:", key="user_input", placeholder="Digite seu código de acesso...")

    auto_focus_input()

    if codigo_usuario.strip():
        with st.spinner("Validando código..."):
            nome_usuario = validar_usuario(codigo_usuario.strip())
        
        if nome_usuario:
            st.session_state["user_code"] = codigo_usuario.strip()
            st.session_state["user_name"] = nome_usuario
            st.success(f"Usuário validado: {nome_usuario}")
            time.sleep(1)
            st.rerun()
        else:
            st.error("❌ Código de acesso inválido. Por favor, tente novamente.")
    else:
        st.warning("Por favor, digite um código de acesso válido.")

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
    st.session_state["user_code"] = ""
    st.session_state["user_name"] = ""
    st.session_state["bulto_cadastrado"] = False
    st.session_state.etapa = "bulto"
    st.rerun()

# Página de cadastro de bultos
if selecao == "Cadastro Bulto":
    # Etapa 1: Cadastro do bulto
    if st.session_state.etapa == "bulto":
        st.markdown("<h1 style='color:black; text-align: center;'>Cadastro de Bultos</h1>", unsafe_allow_html=True)
        st.markdown("<h2 style='color:black; text-align: center;'>Digite o número do bulto</h2>", unsafe_allow_html=True)

        bulto = st.text_input("", key="bulto_input", placeholder="Digite o número do bulto...")

        auto_focus_input()

        if bulto:
            st.session_state["bulto_numero"] = bulto
            st.session_state["bulto_cadastrado"] = True
            st.session_state.etapa = "categoria"
            st.session_state["peca_reset_count"] = 0
            st.rerun()

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
            st.markdown(f"<div class='big-font'>Usuário: {st.session_state['user_name']}</div>", unsafe_allow_html=True)
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
        sku = st.text_input("Digite o SKU:", key=unique_key, placeholder="Bipe o SKU e pressione Enter...")

        # Foco automático otimizado
        auto_focus_input()

        if sku:
            novo_cadastro = {
                "Usuário": st.session_state["user_name"],
                "Bulto": st.session_state["bulto_numero"],
                "SKU": sku,
                "Categoria": st.session_state["categoria_selecionada"],
                "Data/Hora": hora_brasil()
            }
            st.session_state["cadastros"].append(novo_cadastro)
            st.success(f"Peça '{sku}' cadastrada com sucesso!")
            st.session_state["peca_reset_count"] = st.session_state.get("peca_reset_count", 0) + 1
            
            # Forçar rerun para limpar o campo e aplicar foco novamente
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
