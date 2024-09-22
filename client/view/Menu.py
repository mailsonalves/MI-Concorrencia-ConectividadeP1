# menu_functions.py
import customtkinter as ctk
from view.Escolha import exibir_listagem_voos
from view.Consultar_passagem import exibir_consulta_voos

app_global = ''
def open_menu(app, user_token):
    from cliente_main import client
    global app_global
    app_global = app
    user = client.getUser(user_token)
    #user = auth.get("user")
    #user_token = auth.get("token")
    # Limpa a tela atual antes de exibir o menu
    for widget in app.winfo_children():
        widget.destroy()

    # Frame para centralizar o conteúdo do menu
    frame = ctk.CTkFrame(app, fg_color="transparent")
    frame.pack(expand=True)

    # Título do menu
    label_title = ctk.CTkLabel(frame, text=f"Bem-vindo, {user.name} ", font=("Arial", 20))
    label_title.pack(pady=20)

    # Botão "Comprar Passagem"
    button_comprar = ctk.CTkButton(frame, text="Comprar Passagem", command=lambda: comprar_passagem(user_token), width=200)
    button_comprar.pack(pady=10)

    # Botão "Consultar Passagem"
    button_consultar = ctk.CTkButton(frame, text="Consultar Passagem", command=lambda: consultar_passagem(user_token), width=200)
    button_consultar.pack(pady=10)

    # Botão "Sair"
    button_sair = ctk.CTkButton(frame, text="Sair", command=app.quit, width=200)
    button_sair.pack(pady=10)

# Função para o botão "Comprar Passagem"
def comprar_passagem(user_token):
    exibir_listagem_voos(app_global,user_token)

# Função para o botão "Consultar Passagem"
def consultar_passagem(user_token):
    exibir_consulta_voos(app_global,user_token)
    
