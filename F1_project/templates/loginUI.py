from views import View
import time

class LoginUI:
    def main():
        print("Entrar no Sistema")
        usuario = input("Informe o e-mail")
        senha = input("Informe a senha")
        if  == None:
                st.write("E-mail ou senha inválidos")
            else:    
                st.session_state["cliente_id"] = c["id"]
                st.session_state["cliente_nome"] = c["nome"]
                st.rerun()