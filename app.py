import streamlit as st
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import os

# Configuração da "Chave Mestra" (Deve ter 16, 24 ou 32 bytes)
# Em um cenário real, isto viria de uma variável de ambiente no GitHub Secrets
SECRET_KEY = b'ChaveMaligna666!' 

class StealthBypass:
    def __init__(self, key):
        self.key = key
        self.mode = AES.MODE_CBC

    def encrypt_payload(self, plain_text):
        cipher = AES.new(self.key, self.mode)
        iv = cipher.iv
        encrypted = cipher.encrypt(pad(plain_text.encode(), AES.block_size))
        # Retorna IV + Texto Cifrado em Base64 para transporte fácil
        return base64.b64encode(iv + encrypted).decode()

    def decrypt_and_run(self, encrypted_payload):
        raw_data = base64.b64decode(encrypted_payload)
        iv = raw_data[:16]
        encrypted_text = raw_data[16:]
        cipher = AES.new(self.key, self.mode, iv)
        decrypted = unpad(cipher.decrypt(encrypted_text), AES.block_size)
        return decrypted.decode()

# --- Interface Streamlit ---
st.set_page_config(page_title="IA Bypass Engine", page_icon="💀")
st.title("🛠️ Engenharia Reversa: Payload Obfuscator")

st.markdown("""
Esta ferramenta demonstra como fragmentar e criptografar lógica para evitar 
detecção de filtros estáticos de IA e sistemas de monitorização.
""")

payload_input = st.text_area("Insira o comando/código para ofuscar:", 
                             placeholder="ex: import os; print(os.getlogin())")

if st.button("Gerar Código Indetectável"):
    if payload_input:
        engine = StealthBypass(SECRET_KEY)
        
        # 1. Criptografia
        safe_blob = engine.encrypt_payload(payload_input)
        
        st.subheader("📦 Payload Criptografado (O que o Filtro vê):")
        st.code(safe_blob)
        
        # 2. Simulação de Execução
        st.subheader("🔓 Reconstrução em Runtime:")
        reconstructed = engine.decrypt_and_run(safe_blob)
        
        with st.expander("Ver lógica reconstruída"):
            st.code(reconstructed, language='python')
            
        st.success("Lógica processada com sucesso via túnel AES.")
    else:
        st.error("Escreve algo primeiro!")

# Rodapé de segurança
st.sidebar.info("Modo de Pesquisa de Cibersegurança Ativo.")
