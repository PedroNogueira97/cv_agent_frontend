"""
CV Agent — Interface Streamlit (Frontend Decoupled & JWT Secured)
Consome a API FastAPI de forma segura via JWT.
"""

import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# ── Configuração da página ──────────────────────────────────────────
st.set_page_config(
    page_title="CV Agent — Production Ready",
    page_icon="🛡️",
    layout="wide",
)

API_URL = os.getenv("API_URL", "http://localhost:8000")

# ── Helpers de API ──────────────────────────────────────────────────
def get_auth_headers():
    if "token" in st.session_state:
        return {"Authorization": f"Bearer {st.session_state.token}"}
    return {}

def api_register(username, email, password):
    try:
        response = requests.post(f"{API_URL}/auth/register", json={
            "username": username,
            "email": email,
            "password": password
        })
        if response.status_code == 200:
            return True, "Cadastrado com sucesso!"
        return False, response.json().get("detail", "Erro desconhecido")
    except Exception as e:
        return False, str(e)

def api_login(username, password):
    try:
        response = requests.post(f"{API_URL}/auth/login", json={
            "username": username,
            "password": password
        })
        if response.status_code == 200:
            return True, response.json()["access_token"], username
        
        try:
            error_detail = response.json().get("detail", "Erro de login")
        except:
            error_detail = f"Erro {response.status_code}: {response.text[:100]}"
            
        return False, error_detail, None
    except Exception as e:
        return False, str(e), None

def api_get_profile():
    try:
        response = requests.get(f"{API_URL}/profile/", headers=get_auth_headers())
        if response.status_code == 200:
            return response.json()
        return {}
    except Exception:
        return {}

def api_save_profile(data):
    try:
        response = requests.post(f"{API_URL}/profile/", 
                                json=data, 
                                headers=get_auth_headers())
        return response.status_code == 200
    except Exception:
        return False

def api_chat(prompt, session_id="default"):
    try:
        response = requests.post(f"{API_URL}/chat/", 
                                json={"prompt": prompt, "session_id": session_id}, 
                                headers=get_auth_headers())
        if response.status_code == 200:
            return response.json()["response"]
        else:
            return f"❌ Erro na API ({response.status_code}): {response.json().get('detail', 'Desconhecido')}"
    except Exception as e:
        return f"❌ Erro de conexão: {str(e)}"

# ── Gerenciamento de Estado de Autenticação ─────────────────────────
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = None
if "token" not in st.session_state:
    st.session_state.token = None

def login_ui():
    st.title("🛡️ Login Seguro — CV Agent")
    
    tab1, tab2 = st.tabs(["Login", "Cadastro"])
    
    with tab1:
        with st.form("login_form"):
            user = st.text_input("Usuário")
            pw = st.text_input("Senha", type="password")
            submit = st.form_submit_button("Entrar", use_container_width=True)
            if submit:
                success, result, username = api_login(user, pw)
                if success:
                    st.session_state.authenticated = True
                    st.session_state.token = result
                    st.session_state.username = username
                    st.rerun()
                else:
                    st.error(result)
                    
    with tab2:
        with st.form("register_form"):
            new_user = st.text_input("Novo Usuário")
            new_email = st.text_input("E-mail")
            new_pw = st.text_input("Nova Senha", type="password")
            confirm_pw = st.text_input("Confirme a Senha", type="password")
            register = st.form_submit_button("Cadastrar", use_container_width=True)
            if register:
                if not new_email or "@" not in new_email:
                    st.error("Por favor, insira um e-mail válido.")
                elif new_pw != confirm_pw:
                    st.error("As senhas não coincidem.")
                elif len(new_pw) < 6:
                    st.error("A senha deve ter pelo menos 6 caracteres.")
                else:
                    success, msg = api_register(new_user, new_email, new_pw)
                    if success:
                        st.success(msg)
                    else:
                        st.error(msg)

# ── Fluxo Principal ─────────────────────────────────────────────────
if not st.session_state.authenticated:
    login_ui()
    st.stop()

# ── Inicialização do session_state (pós-login) ──────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

if "user_data" not in st.session_state:
    st.session_state.user_data = api_get_profile()

if "profile_saved" not in st.session_state:
    st.session_state.profile_saved = bool(st.session_state.user_data.get("nome"))

# ── Sidebar — Formulário de perfil ──────────────────────────────────
with st.sidebar:
    st.header(f"👤 Perfil: {st.session_state.username}")
    if st.button("Sair", use_container_width=True):
        st.session_state.clear()
        st.rerun()

    st.divider()
    st.caption("Preencha seus dados para análise.")

    with st.form("profile_form"):
        nome = st.text_input("Nome completo", value=st.session_state.user_data.get("nome", ""))
        email = st.text_input("Email", value=st.session_state.user_data.get("email", ""))
        telefone = st.text_input("Telefone", value=st.session_state.user_data.get("telefone", ""))
        linkedin = st.text_input("LinkedIn (URL)", value=st.session_state.user_data.get("linkedin", ""))
        github = st.text_input("GitHub (URL)", value=st.session_state.user_data.get("github", ""))

        st.divider()

        formacao = st.text_area("Formação Acadêmica", value=st.session_state.user_data.get("formacao", ""), height=100)
        stack = st.text_area("Stack Técnica", value=st.session_state.user_data.get("stack", ""), height=100)
        projetos = st.text_area("Projetos", value=st.session_state.user_data.get("projetos", ""), height=120)
        experiencia = st.text_area("Experiência Profissional", value=st.session_state.user_data.get("experiencia", ""), height=150)
        idiomas = st.text_area("Idiomas", value=st.session_state.user_data.get("idiomas", ""), height=80)
        cursos = st.text_area("Cursos e Certificações", value=st.session_state.user_data.get("cursos", ""), height=100)

        submitted = st.form_submit_button("💾  Salvar Perfil", use_container_width=True)

        if submitted:
            user_data = {
                "nome": nome, "email": email, "telefone": telefone, "linkedin": linkedin, "github": github,
                "formacao": formacao, "stack": stack, "projetos": projetos, "experiencia": experiencia,
                "idiomas": idiomas, "cursos": cursos,
            }
            if api_save_profile(user_data):
                st.session_state.user_data = user_data
                st.session_state.profile_saved = True
                st.success("✅ Perfil salvo!")
            else:
                st.error("❌ Erro ao salvar perfil (Token expirado?)")

# ── Área principal — Chat ───────────────────────────────────────────
st.title("📄 CV Agent")
st.markdown(f"Bem-vindo! **Sessão Segura Ativa**.")

st.divider()

# Exibir histórico
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input do chat
if prompt := st.chat_input("Deseja analisar alguma vaga agora?"):
    if not st.session_state.profile_saved:
        st.warning("⚠️ Preencha seu perfil antes de conversar.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analisando com IA..."):
            assistant_message = api_chat(prompt)

        st.markdown(assistant_message)

    st.session_state.messages.append({"role": "assistant", "content": assistant_message})
