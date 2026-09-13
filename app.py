import streamlit as st
import urllib.parse

# Configuração da página do aplicativo com tema e ícone
st.set_page_config(
    page_title="CreatorGuard 🛡️", 
    page_icon="🛡️", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estilização CSS Global para transformar o visual do Streamlit
st.markdown("""
    <style>
    /* Remover barras e menus padrões poluídos */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Customização do fundo e fontes principais */
    .stApp {
        background-color: #0f172a;
    }
    
    /* Caixa do Título Principal */
    .header-box {
        text-align: center;
        padding: 30px 10px;
        background: linear-gradient(135deg, #1e1b4b 0%, #0f172a 100%);
        border-radius: 16px;
        border: 1px solid #312e81;
        margin-bottom: 25px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
    }
    .main-title {
        color: #38bdf8 !important;
        font-size: 32px !important;
        font-weight: 800 !important;
        margin-bottom: 5px !important;
        letter-spacing: -0.5px;
    }
    .subtitle {
        color: #94a3b8 !important;
        font-size: 15px !important;
    }
    
    /* Estilização das linhas de resposta */
    .result-row {
        padding: 14px 18px;
        border-radius: 10px;
        margin-bottom: 12px;
        font-weight: 500;
        font-size: 15px;
        display: flex;
        align-items: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .row-green { background-color: #064e3b; color: #34d399; border-left: 5px solid #10b981; }
    .row-yellow { background-color: #451a03; color: #fbbf24; border-left: 5px solid #f59e0b; }
    .row-red { background-color: #7f1d1d; color: #f87171; border-left: 5px solid #ef4444; }
    </style>
""", unsafe_allow_html=True)

# Renderização do cabeçalho customizado lindo
st.markdown("""
    <div class="header-box">
        <h1 class="main-title">CreatorGuard 🛡️</h1>
        <p class="subtitle">A proteção inteligente contra golpes e vírus para Criadores de Conteúdo</p>
    </div>
""", unsafe_allow_html=True)

st.write("Cole abaixo a URL recebida por e-mail, Direct ou WhatsApp para iniciar a varredura automática:")

# Campo de texto integrado
url_usuario = st.text_input("", placeholder="https://exemplo.com")

# Centralizar botão e dar destaque
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    botao_clicado = st.button("Iniciar Varredura 🚀", type="primary", use_container_width=True)

if botao_clicado:
    url_original = url_usuario.strip()
    
    if not url_original:
        st.markdown('<div class="result-row row-yellow">⚠️ Por favor, insira um link válido antes de analisar.</div>', unsafe_allow_html=True)
    else:
        url_limpa = url_original.lower()
        alerta_geral = False
        
        st.write("---")
        st.markdown("### 📊 Relatório Técnico:")

        # 1. Validação REAL de HTTPS
        if url_limpa.startswith("http://"):
            st.markdown('<div class="result-row row-red">❌ ALERTA DE SEGURANÇA: O site usa conexão insegura (HTTP). Dados podem ser interceptados!</div>', unsafe_allow_html=True)
            alerta_geral = True
        elif url_limpa.startswith("https://"):
            st.markdown('<div class="result-row row-green">🟢 Conexão segura básica detectada (HTTPS).</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="result-row row-yellow">⚠️ ATENÇÃO: Você não informou o protocolo (http:// ou https://). Não há garantia de criptografia na análise textual.</div>', unsafe_allow_html=True)
            if not url_limpa.startswith("www.") and "." in url_limpa:
                url_original = "https://" + url_original
            elif url_limpa.startswith("www."):
                url_original = "https://" + url_original

        # Parser oficial
        parsed_url = urllib.parse.urlparse(url_original)
        dominio = parsed_url.netloc.lower()
        url_completa_analise = (parsed_url.netloc + parsed_url.path + parsed_url.query).lower()

        # 2. Proteção contra Engenharia Social / Clones
        marcas_alvo = ['instagram', 'youtube', 'tiktok', 'google', 'facebook', 'meta']
        termos_suspeitos = ['login', 'suporte', 'support', 'colab', 'verificar', 'partnership', 'ganhar', 'seguidores', 'promo', 'recompensa']
        
        for marca in marcas_alvo:
            if marca in url_completa_analise:
                site_oficial = f"{marca}.com"
                if site_oficial not in dominio and f"{marca}.com.br" not in dominio:
                    for termo in termos_suspeitos:
                        if termo in url_completa_analise:
                            st.markdown(f'<div class="result-row row-red">❌ ALERTA CRÍTICO DE PHISHING: O link cita a marca \'{marca.capitalize()}\' usando o termo \'{termo}\', mas NÃO pertence aos servidores oficiais! Trata-se de uma tentativa de clonagem de conta.</div>', unsafe_allow_html=True)
                            alerta_geral = True
                            break
                    if alerta_geral:
                        break

        # 3. Validação de Encurtadores
        encurtadores = ['bit.ly', 'cutt.ly', 'tinyurl.com', 'rb.gy', 'is.gd', 't.co']
        for enc in encurtadores:
            if enc in dominio:
                st.markdown(f'<div class="result-row row-yellow">⚠️ ATENÇÃO: Este é um link encurtado ({enc}) criado artificialmente para ocultar o destino real do endereço.</div>', unsafe_allow_html=True)
                alerta_geral = True
                break

        # 4. Validação de Plataformas de Download
        plataformas_suspeitas = ['mediafire', 'mega.nz', 'wetransfer', 'drive-google', 'dropbox-share']
        for plat in plataformas_suspeitas:
            if plat in url_completa_analise:
                st.markdown(f'<div class="result-row row-red">❌ ALERTA DE PLATAFORMA: O link exige downloads externos ({plat}). Empresas sérias enviam anexos contratuais corporativos diretos.</div>', unsafe_allow_html=True)
                alerta_geral = True
                break

        # 5. Validação de Arquivos Perigosos (Vírus)
        extensoes_perigosas = ['.exe', '.zip', '.rar', '.scr', '.bat', '.msi', '.pif']
        for ext in extensoes_perigosas:
            if ext in url_completa_analise:
                st.markdown(f'<div class="result-row row-red">❌ PERIGO MÁXIMO DETECTADO: A URL aponta para a extensão de vírus \'{ext}\'. Executar este arquivo compromete a segurança de todos os seus cookies de sessão.</div>', unsafe_allow_html=True)
                alerta_geral = True
                break
                
        # Bloco de Sucesso Final (Verdadeiro)
        if not alerta_geral:
            st.snow()
            st.markdown(
                """
                <div style="background-color: #064e3b; color: #34d399; padding: 25px; border-radius: 12px; border: 1px solid #059669; margin-top: 25px; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.4);">
                    <h3 style="margin-top: 0; color: #34d399; font-weight: 700;">🟢 Link Validado com Sucesso!</h3>
                    <p style="margin-bottom: 0; color: #e2e8f0; font-size: 14px;">Os algoritmos do sistema não mapearam nenhuma assinatura óbvia de phishing, encurtador malicioso ou vírus infostealer. A navegação básica parece segura.</p>
                    <hr style="border-color: #059669; margin: 15px 0;">
                    <small style="color: #94a3b8; display: block; font-size: 12px; line-height: 1.4;">🛡️ Diretriz de Segurança Geral: Mesmo com validação positiva, mantenha o protocolo de jamais preencher senhas administrativas ou códigos MFA fora dos portais de login oficiais.</small>
                </div>
                """, 
                unsafe_allow_html=True
            )
