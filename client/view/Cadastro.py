import customtkinter as ctk 
from view.Menu import open_menu


# Configurando o tema e a aparência
ctk.set_appearance_mode("System")  # Modos: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # Temas: "blue", "green", "dark-blue"

def voltar(app):
    from view.Login import open_login_screen
    
    #Função que define o comportamento do botão voltar
    for widget in app.winfo_children():
        widget.destroy()
    #Aqui você pode adicionar o código que irá exibir a tela anterior, por exemplo:
    open_login_screen()
    
# Função de login
def cadastro(app):
    from cliente_main import client
    username = entry_username.get()
    password = entry_password.get()
    
    confirmar_password = entry_password_confirm.get()
    if (password == confirmar_password) and ((password != '') and (confirmar_password != '')):
       client._cadastro(username, password)
       voltar(app)
            
    else:
        label_result.configure(text="As senhas não coincidem ", text_color="red")
        

# Função para exibir a tela de login
def open_cadastro_screen(app):
 
    # Limpa a tela atual
    for widget in app.winfo_children():
        widget.destroy()

    # Frame para centralizar o conteúdo
    frame = ctk.CTkFrame(app, fg_color="transparent")
    frame.pack(expand=True)  # O frame expande para ocupar o espaço disponível

    # Título da tela de login
    label_title = ctk.CTkLabel(frame, text="Cadastre-se", font=("Arial", 20))
    label_title.pack(pady=20)

    global entry_username, entry_password, label_result,entry_password_confirm

    # Campo de entrada para usuário
    entry_username = ctk.CTkEntry(frame, placeholder_text="Usuário", width=300)
    entry_username.pack(pady=10)

    # Campo de entrada para senha
    entry_password = ctk.CTkEntry(frame, placeholder_text="Senha", show="*", width=300)
    entry_password.pack(pady=10)
    # Campo de entrada para confirmação de senha
    entry_password_confirm = ctk.CTkEntry(frame, placeholder_text="Confirme a senha", show="*", width=300)
    entry_password_confirm.pack(pady=10)


    # Botão de cadastro ()
    button_register = ctk.CTkButton(frame, text="Cadastrar", command=lambda: cadastro(app), width=300)
    button_register.pack(padx=10)
    
    frame_bottom = ctk.CTkFrame(app, fg_color="transparent")
    frame_bottom.pack(side="bottom", fill="x")

    # Botão de Voltar
    voltar_btn = ctk.CTkButton(frame_bottom, text="Voltar",  command=lambda: voltar(app))
    voltar_btn.grid(row=0, column=0, columnspan=2, pady=10, padx=5)


    # Label para exibir mensagens de erro ou sucesso
    label_result = ctk.CTkLabel(frame, text="")
    label_result.pack(pady=10)


