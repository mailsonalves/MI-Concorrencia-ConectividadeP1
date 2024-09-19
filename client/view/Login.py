import customtkinter as ctk

# Configurando o tema e a aparência
ctk.set_appearance_mode("System")  # Modos: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # Temas: "blue", "green", "dark-blue"

# Função que será chamada ao clicar no botão de login
def login():
    username = entry_username.get()
    password = entry_password.get()
    
    # Lógica de autenticação simples (pode ser adaptada para banco de dados ou API)
    if username == "admin" and password == "1234":
        label_result.configure(text="Login bem-sucedido!", text_color="green")
    else:
        label_result.configure(text="Usuário ou senha incorretos", text_color="red")

# Criando a janela principal
app = ctk.CTk()
app.geometry("400x300")
app.title("Login")

# Criando um rótulo para o título
label_title = ctk.CTkLabel(app, text="Sistema de Login", font=("Arial", 20))
label_title.pack(pady=20)

# Criando o campo para inserir o nome de usuário
entry_username = ctk.CTkEntry(app, placeholder_text="Usuário")
entry_username.pack(pady=10)

# Criando o campo para inserir a senha
entry_password = ctk.CTkEntry(app, placeholder_text="Senha", show="*")
entry_password.pack(pady=10)

# Criando o botão de login
button_login = ctk.CTkButton(app, text="Login", command=login)
button_login.pack(pady=20)

# Rótulo para mostrar o resultado do login (sucesso/erro)
label_result = ctk.CTkLabel(app, text="")
label_result.pack(pady=10)

# Rodando a aplicação
app.mainloop()
