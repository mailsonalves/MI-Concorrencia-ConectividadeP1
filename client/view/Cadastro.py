import customtkinter as ctk 

# Configurando o tema e a aparência
ctk.set_appearance_mode("System")  # Modos: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # Temas: "blue", "green", "dark-blue"

def voltar(app):
    """
    Função que define o comportamento do botão 'Voltar'.
    Remove todos os widgets da tela atual e exibe a tela de login.
    """
    from view.Login import open_login_screen
    
    for widget in app.winfo_children():  # Remove todos os widgets da janela
        widget.destroy()
    open_login_screen()  # Exibe a tela de login

def cadastro(app):
    """
    Função de cadastro de usuário.
    Valida as informações de entrada e chama a função de cadastro do cliente.
    """
    from cliente_main import client
    username = entry_username.get()  # Obtém o nome de usuário
    password = entry_password.get()  # Obtém a senha
    name = entry_name.get()  # Obtém o nome completo
    confirmar_password = entry_password_confirm.get()  # Obtém a confirmação da senha
    
    # Verifica se as senhas coincidem e não estão vazias
    if (password == confirmar_password) and ((password != '') and (confirmar_password != '')):
        if (client.cadastro(username, password, name) == True):  # Tenta cadastrar o usuário
            label_result.configure(text="Usuário cadastrado", text_color="green")  # Mensagem de sucesso
        else:
            label_result.configure(text="Usuário já existe", text_color="red")  # Mensagem de erro
    else:
        label_result.configure(text="As senhas não coincidem ", text_color="red")  # Mensagem de erro

def open_cadastro_screen(app):
    """
    Função para exibir a tela de cadastro.
    Limpa a tela atual e cria os widgets necessários para o cadastro.
    """
    # Limpa a tela atual
    for widget in app.winfo_children():
        widget.destroy()

    # Frame para centralizar o conteúdo
    frame = ctk.CTkFrame(app, fg_color="transparent")
    frame.pack(expand=True)  # O frame expande para ocupar o espaço disponível

    # Título da tela de cadastro
    label_title = ctk.CTkLabel(frame, text="Cadastre-se", font=("Arial", 20))
    label_title.pack(pady=20)

    global entry_username, entry_password, label_result, entry_password_confirm, entry_name

    # Campo de entrada para nome de usuário
    entry_username = ctk.CTkEntry(frame, placeholder_text="Username", width=300)
    entry_username.pack(pady=10)
    
    # Campo de entrada para nome completo
    entry_name = ctk.CTkEntry(frame, placeholder_text="Nome", width=300)
    entry_name.pack(pady=10)

    # Campo de entrada para senha
    entry_password = ctk.CTkEntry(frame, placeholder_text="Senha", show="*", width=300)
    entry_password.pack(pady=10)
    
    # Campo de entrada para confirmação de senha
    entry_password_confirm = ctk.CTkEntry(frame, placeholder_text="Confirme a senha", show="*", width=300)
    entry_password_confirm.pack(pady=10)

    # Botão de cadastro
    button_register = ctk.CTkButton(frame, text="Cadastrar", command=lambda: cadastro(app), width=300)
    button_register.pack(padx=10)
    
    frame_bottom = ctk.CTkFrame(app, fg_color="transparent")  # Frame para os botões na parte inferior
    frame_bottom.pack(side="bottom", fill="x")

    # Botão de Voltar
    voltar_btn = ctk.CTkButton(frame_bottom, text="Voltar", command=lambda: voltar(app))
    voltar_btn.grid(row=0, column=0, columnspan=2, pady=10, padx=5)

    # Label para exibir mensagens de erro ou sucesso
    label_result = ctk.CTkLabel(frame, text="")
    label_result.pack(pady=10)
