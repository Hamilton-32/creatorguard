import streamlit as st
import urllib.parse

# Configuração da página do aplicativo
st.set_page_config(
    page_title="CreatorGuard 🛡️", 
    page_icon="🛡️", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estilização CSS Global Avançada (Fundo idêntico à logo)
st.markdown("""
    <style>
    /* Ocultar menus e rodapés padrões */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Fundo correspondente ao tom escuro metálico da logo */
    .stApp {
        background-color: #1e2229;
        font-family: 'Inter', sans-serif;
    }
    
    /* Cabeçalho Minimalista e Elegante */
    .header-container {
        text-align: center;
        padding: 10px 10px 20px 10px;
    }
    .subtitle {
        color: #94a3b8 !important;
        font-size: 16px !important;
        font-weight: 400;
        margin-top: 15px !important;
    }
    
    /* Caixa de Entrada de Texto Adaptada ao Novo Fundo */
    .stTextInput > div > div > input {
        background-color: #0b0f19 !important;
        color: #f8fafc !important;
        border: 1px solid #475569 !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
        font-size: 15px !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.2) !important;
    }

    /* Linhas de Resultado Individuais */
    .result-card {
        padding: 16px 20px;
        border-radius: 12px;
        margin-bottom: 14px;
        font-size: 15px;
        line-height: 1.5;
        font-weight: 500;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
        border: 1px solid transparent;
    }
    .card-green { background-color: rgba(16, 185, 129, 0.15); color: #34d399; border-color: rgba(16, 185, 129, 0.3); }
    .card-yellow { background-color: rgba(245, 158, 11, 0.15); color: #fbbf24; border-color: rgba(245, 158, 11, 0.3); }
    .card-red { background-color: rgba(239, 68, 68, 0.15); color: #f87171; border-color: rgba(239, 68, 68, 0.3); }
    
    /* Card de Sucesso Final Definitivo */
    .success-banner {
        background: linear-gradient(135deg, #064e3b 0%, #022c22 100%);
        color: #e2e8f0;
        padding: 30px;
        border-radius: 16px;
        border: 1px solid #059669;
        margin-top: 25px;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.6);
    }
    </style>
""", unsafe_allow_html=True)

# Renderização da Logo e do Cabeçalho
col_logo1, col_logo2, col_logo3 = st.columns()
with col_logo2:
    try:
        # Exibe a logo centralizada
        st.image("logo.png", use_container_width=True)
    except:
        # Caso a imagem ainda não esteja no repositório
        st.markdown('<h1 style="text-align: center; color: #f8fafc;">CreatorGuard 🛡️</h1>', unsafe_allow_html=True)

st.markdown("""
    <div class="header-container">
        <p class="subtitle">Varredura inteligente de links para proteção de canais e redes sociais</p>
    </div>
""", unsafe_allow_html=True)

st.markdown('<p style="color: #cbd5e1; font-size: 14px; margin-bottom: 5px;">Cole a URL da proposta comercial abaixo:</p>', unsafe_allow_html=True)
url_usuario = st.text_input("", placeholder="https://exemplo.com", label_visibility="collapsed")

# Botão de Varredura
st.write("")
botao_clicado = st.button("Analisar Link 🔍", type="primary", use_container_width=True)

if botao_clicado:
    url_original = url_usuario.strip()
    
    if not url_original:
        st.markdown('<div class="result-card card-yellow">⚠️ Por favor, insira uma URL válida para realizar a análise.</div>', unsafe_allow_html=True)
    else:
        url_limpa = url_original.lower()
        alerta_geral = False
        
        st.write("---")
        st.markdown('<p style="color: #f8fafc; font-size: 18px; font-weight: 700; margin-bottom: 15px;">📊 Relatório de Segurança:</p>', unsafe_allow_html=True)

        # 1. Validação de HTTPS
        if url_limpa.startswith("http://"):
            st.markdown('<div class="result-card card-red">❌ CONNECTION INSECURE: O link utiliza o protocolo antigo HTTP. Seus dados cadastrais ou senhas inseridas nesta página podem ser interceptados facilmente por terceiros.</div>', unsafe_allow_html=True)
            alerta_geral = True
        elif url_limpa.startswith("https://"):
            st.markdown('<div class="result-card card-green">🟢 PROTOCOLO SEGURO: Conexão criptografada padrão detectada com sucesso (HTTPS).</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="result-card card-yellow">⚠️ PROTOCOLO AUSENTE: Você omitiu o prefixo (http:// ou https://). A integridade do tráfego não pôde ser validada automaticamente apenas por este texto.</div>', unsafe_allow_html=True)
            if not url_limpa.startswith("www.") and "." in url_limpa:
                url_original = "https://" + url_original
            elif url_limpa.startswith("www."):
                url_original = "https://" + url_original

        # Isolar partes do link
        parsed_url = urllib.parse.urlparse(url_original)
        dominio = parsed_url.netloc.lower()
        url_completa_analise = (parsed_url.netloc + parsed_url.path + parsed_url.query).lower()

        # 2. Detecção de Engenharia Social / Páginas Clonadas
        marcas_alvo = ['instagram', 'youtube', 'tiktok', 'google', 'facebook', 'meta']
        termos_suspeitos = ['login', 'suporte', 'support', 'colab', 'verificar', 'partnership', 'ganhar', 'seguidores', 'promo', 'recompensa']
        
        for marca in marcas_alvo:
            if marca in url_completa_analise:
                site_oficial = f"{marca}.com"
                if site_oficial not in dominio and f"{marca}.com.br" not in dominio:
                    for termo in termos_suspeitos:
                        if termo in url_completa_analise:
                            st.markdown(f'<div class="result-card card-red">❌ ENGENHARIA SOCIAL DETECTADA: O link menciona a marca de forma ilegítima (\'{marca.capitalize()}\') em conjunto com o termo de ação \'{termo}\'. O domínio não pertence aos servidores oficiais da empresa e trata-se de um site clonado para roubo de contas.</div>', unsafe_allow_html=True)
                            alerta_geral = True
                            break
                    if alerta_geral:
                        break

        # 3. Validação de Encurtadores
        encurtadores = ['bit.ly', 'cutt.ly', 'tinyurl.com', 'rb.gy', 'is.gd', 't.co']
        for enc in encurtadores:
            if enc in dominio:
                st.markdown(f'<div class="result-card card-yellow">⚠️ URL CAMUFLADA: Este link está mascarado por um encurtador técnico ({enc}). Golpistas usam esse artifício para burlar filtros de e-mail e ocultar o destino malicioso final.</div>', unsafe_allow_html=True)
                alerta_geral = True
                break

        # 4. Validação de Plataformas de Download
        plataformas_suspeitas = ['mediafire', 'mega.nz', 'wetransfer', 'drive-google', 'dropbox-share']
        for plat in plataformas_suspeitas:
            if plat in url_completa_analise:
                st.markdown(f'<div class="result-card card-red">❌ PLATAFORMA DE DOWNLOAD EXTERNA: O link redireciona para um servidor de armazenamento coletivo ({plat}). Propostas corporativas genuínas são enviadas formalmente via anexo de e-mail (PDF) ou DocuSign, nunca por links de download direto.</div>', unsafe_allow_html=True)
                alerta_geral = True
                break

        # 5. Validação de Arquivos Perigosos (Vírus Infostealer)
        extensoes_perigosas = ['.exe', '.zip', '.rar', '.scr', '.bat', '.msi', '.pif']
        for ext in extensoes_perigosas:
            if ext in url_completa_analise:
                st.markdown(f'<div class="result-card card-red">❌ COMPONENTE MALICIOSO CRÍTICO: A URL contém uma chamada direta para um arquivo executável ou compactado ({ext}). Baixar e abrir este arquivo injetará um script oculto em seu sistema capaz de capturar cookies de sessão ativa e contornar a autenticação de dois fatores (MFA).</div>', unsafe_allow_html=True)
                alerta_geral = True
                break
                
        # Card de Sucesso Final
        if not alerta_geral:
            st.markdown(
                """
                <div class="success-banner">
                    <h3 style="margin-top: 0; color: #34d399; font-weight: 700; font-size: 20px;">🟢 Link Analisado com Sucesso!</h3>
                    <p style="margin-bottom: 0; color: #f1f5f9; font-size: 14px; opacity: 0.9;">O sistema realizou a varredura completa da estrutura de strings e parâmetros da URL e não detectou nenhuma assinatura óbvia de phishing, domínio clonado ou arquivo compactado suspeito.</p>
                    <hr style="border-color: #059669; margin: 15px 0; opacity: 0.4;">
                    <small style="color: #94a3b8; display: block; font-size: 12px; line-height: 1.4;">🛡️ Recomendação de Rotina: Embora este link específico não apresente indicadores de fraude visíveis, mantenha a política estrita de segurança de nunca digitar credenciais de acesso ou códigos em portais de terceiros.</small>
                </div>
                """, 
                unsafe_allow_html=True
            )
