import customtkinter as ctk 
from view.Menu import open_menu
from view.Cadastro import open_cadastro_screen
import time

# Configurando o tema e a aparência
ctk.set_appearance_mode("System")  # Modos: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # Temas: "blue", "green", "dark-blue"

# Função de login
def login():
    from cliente_main import client
    username = entry_username.get()
    password = entry_password.get()
    if((username != '') and {password != ''}):
        auth = client.authenticate( username,password)
        # Lógica de autenticação simples (pode ser adaptada para validação real)
        if auth != False:
            label_result.configure(text="Login bem-sucedido!", text_color="green")
            user_token = auth.get("token")
            open_menu(app,user_token)  # Chama a função para abrir o dashboard
        else:
            label_result.configure(text="Usuário ou senha incorretos", text_color="red")
    else:
        label_result.configure(text="Preencha os campos", text_color="red")
        

# Função para exibir a tela de login
def open_login_screen():
    # Limpa a tela atual
    if app.winfo_exists():
        for widget in app.winfo_children():
            widget.destroy()

    # Frame para centralizar o conteúdo
    frame = ctk.CTkFrame(app, fg_color="transparent")
    frame.pack(expand=True)  # O frame expande para ocupar o espaço disponível

    # Título da tela de login
    label_title = ctk.CTkLabel(frame, text="Login do Usuário", font=("Arial", 20))
    label_title.pack(pady=20)

    global entry_username, entry_password, label_result

    # Campo de entrada para usuário
    entry_username = ctk.CTkEntry(frame, placeholder_text="Usuário", width=300)
    entry_username.pack(pady=10)
    

    # Campo de entrada para senha
    entry_password = ctk.CTkEntry(frame, placeholder_text="Senha", show="*", width=300)
    entry_password.pack(pady=10)

    # Botão de login
    button_login = ctk.CTkButton(frame, text="Entrar", command=login, width=300)
    button_login.pack(padx=10, pady=10)

    # Botão de cadastro (com função ainda não implementada)
    button_register = ctk.CTkButton(frame, text="Cadastrar", fg_color="transparent", text_color="#0377fc", hover_color="#2a2d30", command=lambda: open_cadastro_screen(app), width=300)
    button_register.pack(padx=10)

    # Label para exibir mensagens de erro ou sucesso
    label_result = ctk.CTkLabel(frame, text="")
    label_result.pack(pady=10)

# Criando a janela principal
app = ctk.CTk()
app.geometry("600x400")

app.title("Sistema de Reservas de Voo")

# Inicializando a tela de login
open_login_screen()

# Rodando a aplicação
app.mainloop()
