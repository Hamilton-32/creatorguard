import streamlit as st
import urllib.parse

# Configuração da página do aplicativo
st.set_page_config(page_title="CreatorGuard 🛡️", page_icon="🛡️", layout="centered")

st.title("CreatorGuard 🛡️")
st.subheader("Analisador de links contra golpes para Criadores de Conteúdo")
st.write("Cole abaixo o link recebido na proposta de parceria para verificar se ele é seguro.")

url_usuario = st.text_input("Cole a URL aqui:", placeholder="https://...")

if st.button("Analisar Link", type="primary"):
    url_original = url_usuario.strip()
    
    if not url_original:
        st.warning("⚠️ Por favor, insira um link válido antes de analisar.")
    else:
        url_limpa = url_original.lower()
        alerta_geral = False
        
        st.write("---")
        st.markdown("### 📊 Resultado da Análise:")

        # 1. Validação REAL de HTTPS
        if url_limpa.startswith("http://"):
            st.error("❌ **ALERTA DE SEGURANÇA:** O site usa conexão insegura (HTTP). Dados digitados nele podem ser interceptados!")
            alerta_geral = True
        elif url_limpa.startswith("https://"):
            st.success("✅ Conexão segura básica detectada (HTTPS).")
        else:
            st.warning("⚠️ **AVISO:** Você não informou o protocolo (http:// ou https://). Não é possível garantir a criptografia deste link apenas pelo texto.")
            if not url_limpa.startswith("www.") and "." in url_limpa:
                url_original = "https://" + url_original
            elif url_limpa.startswith("www."):
                url_original = "https://" + url_original

        # Utiliza o parser oficial do Python para isolar as partes do link com segurança
        parsed_url = urllib.parse.urlparse(url_original)
        dominio = parsed_url.netloc.lower()
        caminho_e_resto = parsed_url.path.lower() + parsed_url.query.lower()
        url_completa_analise = (parsed_url.netloc + parsed_url.path + parsed_url.query).lower()

        # 2. NOVA PROTEÇÃO: Identificação de Clones e Links Falsos de Redes Sociais (Mesmo com HTTPS)
        marcas_alvo = ['instagram', 'youtube', 'tiktok', 'google', 'facebook', 'meta']
        termos_suspeitos = ['login', 'suporte', 'support', 'colab', 'verificar', 'partnership', 'ganhar', 'seguidores', 'promo', 'recompensa']
        
        for marca in marcas_alvo:
            # Se o nome da marca está no link, mas o domínio NÃO é o site oficial dela (ex: instagram-suporte-colab.com)
            if marca in url_completa_analise:
                site_oficial = f"{marca}.com"
                if site_oficial not in dominio and f"{marca}.com.br" not in dominio:
                    # Verifica se tem termos perigosos misturados que indicam engenharia social
                    for termo in termos_suspeitos:
                        if termo in url_completa_analise:
                            st.error(f"🚨 **ALERTA CRÍTICO DE PHISHING:** Este link cita a marca **'{marca.capitalize()}'** misturada com o termo **'{termo}'**, mas NÃO pertence ao site oficial! Golpistas usam HTTPS e nomes parecidos para clonar telas de login e roubar contas.")
                            alerta_geral = True
                            break
                    if alerta_geral:
                        break

        # 3. Validação de Encurtadores
        encurtadores = ['bit.ly', 'cutt.ly', 'tinyurl.com', 'rb.gy', 'is.gd', 't.co']
        for enc in encurtadores:
            if enc in dominio:
                st.warning(f"⚠️ **AVISO:** Este é um link encurtado (`{enc}`). Golpistas usam isso para esconder o endereço real de sites falsos.")
                alerta_geral = True
                break

        # 4. Validação de Plataformas de Download
        plataformas_suspeitas = ['mediafire', 'mega.nz', 'wetransfer', 'drive-google', 'dropbox-share']
        for plat in plataformas_suspeitas:
            if plat in url_completa_analise:
                st.error(f"🚨 **ALERTA DE DOWNLOAD:** O link envolve uma plataforma de download (`{plat}`). Empresas reais enviam propostas e contratos em PDF por e-mail, nunca links para baixar arquivos!")
                alerta_geral = True
                break

        # 5. Validação de Arquivos Perigosos (Vírus)
        extensoes_perigosas = ['.exe', '.zip', '.rar', '.scr', '.bat', '.msi', '.pif']
        for ext in extensoes_perigosas:
            if ext in url_completa_analise:
                st.error(f"🛑 **PERIGO MÁXIMO:** O link aponta para um arquivo `{ext}`. Isso instala um vírus criado para roubar canais e pular a verificação em duas etapas!")
                alerta_geral = True
                break
                
        # Resultado final caso passe em tudo
        if not alerta_geral:
            st.balloons()
            st.success("🛡️ **NENHUM PADRÃO ÓBVIO DE GOLPE DETECTADO!** O link parece seguro para navegar. (Mas continue atenta caso peçam senhas ou códigos).")
