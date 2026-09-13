import streamlit as st

# Configuração da página do aplicativo
st.set_page_config(page_title="CreatorGuard 🛡️", page_icon="🛡️", layout="centered")

# Estilização e Título Principal
st.title("CreatorGuard 🛡️")
st.subheader("Analisador de links contra golpes para Criadores de Conteúdo")
st.write("Cole abaixo o link recebido na proposta de parceria para verificar se ele é seguro.")

# Campo de texto interativo para colar o link
url_usuario = st.text_input("Cole a URL aqui:", placeholder="https://...")

# Botão para iniciar a análise
if st.button("Analisar Link", type="primary"):
    if not url_usuario.strip():
        st.warning("⚠️ Por favor, insira um link válido antes de analisar.")
    else:
        url_limpa = url_usuario.lower().strip()
        alerta_geral = False
        
        st.write("---")
        st.markdown("### 📊 Resultado da Análise:")

        # 1. Validação HTTPS
        if not url_limpa.startswith("https://") and not url_limpa.startswith("http://"):
            url_limpa = "https://" + url_limpa

        if "https://" not in url_limpa:
            st.error("❌ **ALERTA DE SEGURANÇA:** O site não usa conexão segura (HTTPS). Dados digitados nele podem ser interceptados!")
            alerta_geral = True
        else:
            st.success("✅ Conexão segura básica detectada (HTTPS).")
            
        # 2. Validação de Encurtadores
        encurtadores = ['bit.ly', 'cutt.ly', 'tinyurl.com', 'rb.gy', 'is.gd', 't.co']
        for enc in encurtadores:
            if enc in url_limpa:
                st.warning(f"⚠️ **AVISO:** Este é um link encurtado (`{enc}`). Golpistas usam isso para esconder o endereço real de sites falsos.")
                alerta_geral = True
                break

        # 3. Validação de Plataformas de Download
        plataformas_suspeitas = ['mediafire', 'mega.nz', 'wetransfer', 'drive-google', 'dropbox-share']
        for plat in plataformas_suspeitas:
            if plat in url_limpa:
                st.error(f"🚨 **ALERTA CRÍTICO:** O link envolve uma plataforma de download (`{plat}`). Empresas reais enviam propostas e contratos em PDF por e-mail, nunca links para você baixar arquivos!")
                alerta_geral = True
                break

        # 4. Validação de Arquivos Perigosos (Vírus)
        extensoes_perigosas = ['.exe', '.zip', '.rar', '.scr', '.bat', '.msi', '.pif']
        for ext in extensoes_perigosas:
            if ext in url_limpa:
                st.error(f"🛑 **PERIGO MÁXIMO:** O link aponta para um arquivo `{ext}`. Isso é um vírus criado especificamente para roubar canais, pular a verificação em duas etapas e assumir o controle das suas redes sociais!")
                alerta_geral = True
                break
                
        # Resultado final caso passe em todos os testes
        if not alerta_geral:
            st.balloons()  # Solta balões na tela do tablet para comemorar!
            st.success("🛡️ **NENHUM PADRÃO ÓBVIO DE GOLPE DETECTADO!** O link parece seguro para navegar. (Mas continue atenta caso peçam senhas ou códigos).")
