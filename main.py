import streamlit as st
from produtos import dashboard

# Lista de usuários e senhas permitidos
usuarios_autorizados = {'igor':'igor123', 'josimar':'josimar123', 'kayene': 'kayene123'}



def main():
    
    # Verifica se o usuário está autenticado
    if 'autenticado' not in st.session_state:
        st.session_state.autenticado = False

    if not st.session_state.autenticado:
        login_form()
    else:
        dashboard()
        # Adicione aqui o código para a área restrita após o login.
        
    #with open('style.css') as f:
        #st.markdown(f"<style>{f.read()} </style>", unsafe_allow_html=True)

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
    # Verifica se o usuário e a senha correspondem à lista permitida
    return usuario in usuarios_autorizados and usuarios_autorizados[usuario] == senha

if __name__ == "__main__":
    main()