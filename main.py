import streamlit as st
from páginas import *
from páginas.produtos import dashboard_produtos
from páginas.vendas import dashboard_vendas
from páginas.devolucoes import dashboard_devolucoes
from assets import *


# Lista de usuários permitidos
usuarios_autorizados = list(st.secrets['users'].keys())

# Lista de senhas correspondentes
senhas_autorizadas = list(st.secrets['users'].values())


def main():
    
    # Verifica se o usuário está autenticado
    if 'autenticado' not in st.session_state:
        st.session_state.autenticado = False

    if not st.session_state.autenticado:
        login_form()
    else:
        st.set_page_config(layout="wide")
        home()
        # Adicione aqui o código para a área restrita após o login.
        
    with open('assets/style.css') as f:
        st.markdown(f"<style>{f.read()} </style>", unsafe_allow_html=True)


def login_form():
    st.subheader("Faça o Login")

    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        # Verifica se o usuário e senha correspondem à lista permitida
        if autenticar_usuario(usuario, senha):
            st.success("Login bem-sucedido!")
            st.session_state.autenticado = True
            st.session_state.usuario_autenticado = usuario
            # Redireciona para a página após o login
            st.rerun()
        else:
            st.error("Usuário ou senha incorretos")


def autenticar_usuario(usuario, senha):
    # Verifica se o usuário e a senha correspondem às listas permitidas
    if usuario in usuarios_autorizados:
        index = usuarios_autorizados.index(usuario)
        if senhas_autorizadas[index] == senha:
            return True
    return False


def home():
    selection = st.sidebar.selectbox('Navegação', ['Produtos', 'Devoluções'])
    
    st.sidebar.image("assets/logo-livre-e-leve.png", width=150)

    if selection == "Produtos":
        dashboard_produtos()
    elif selection == "Vendas":
        dashboard_vendas()
    elif selection == "Devoluções":
        dashboard_devolucoes()


if __name__ == "__main__":
    main()