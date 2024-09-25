# menu_functions.py
import customtkinter as ctk
from view.Escolha import exibir_listagem_voos
from view.Consultar_passagem import exibir_consulta_voos

# Variável global para armazenar a referência da aplicação
app_global = ''

def open_menu(app, user_token):
    """
    Função para abrir o menu principal da aplicação.

    Limpa a tela atual e exibe as opções disponíveis ao usuário,
    incluindo comprar passagem, consultar passagem e sair. 

    Args:
        app: A instância da aplicação.
        user_token: O token do usuário para autenticação.

    Returns:
        None
    """
    from cliente_main import client
    global app_global
    app_global = app

    # Obtém os dados do usuário usando o token
    user = client.getUser(user_token)

    # Limpa a tela atual antes de exibir o menu
    for widget in app.winfo_children():
        widget.destroy()

    # Frame para centralizar o conteúdo do menu
    frame = ctk.CTkFrame(app, fg_color="transparent")
    frame.pack(expand=True)

    # Título do menu com o nome do usuário
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

def comprar_passagem(user_token):
    """
    Função chamada ao clicar no botão "Comprar Passagem".

    Exibe a listagem de voos disponíveis para o usuário.

    Args:
        user_token: O token do usuário para autenticação.

    Returns:
        None
    """
    exibir_listagem_voos(app_global, user_token)

def consultar_passagem(user_token):
    """
    Função chamada ao clicar no botão "Consultar Passagem".

    Exibe a interface de consulta de passagens para o usuário.

    Args:
        user_token: O token do usuário para autenticação.

    Returns:
        None
    """
    exibir_consulta_voos(app_global, user_token)
