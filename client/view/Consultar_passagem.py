import customtkinter as ctk

def radioButton_event(selected_assento):
    """
    Função chamada ao selecionar um assento.
    Armazena o assento selecionado na variável global 'select_voo'.
    """
    global select_voo
    select_voo = selected_assento.get()
    return

def deletar_voo(app, passagem):
    """
    Função para deletar um voo selecionado.
    Chama a função de deleção do cliente e atualiza a lista de voos na interface.
    """
    from cliente_main import client  # Importa o cliente para manipulação de dados
    remove = client.deletar_compra(voos, passagem)  # Tenta deletar a passagem
    if remove:
        print('Deletado com sucesso')
        exibir_consulta_voos(app, token)  # Atualiza a página após a remoção
    else:
        print('Falha ao remover')  # Mensagem de erro caso a remoção falhe

def voltar(app, token):
    """
    Função que define o comportamento do botão 'Voltar'.
    Remove todos os widgets atuais e exibe a tela anterior (menu).
    """
    from view.Menu import open_menu  # Importa a função para abrir o menu
    
    for widget in app.winfo_children():  # Remove todos os widgets da janela
        widget.destroy()
    open_menu(app, token)  # Exibe a tela anterior

def exibir_detalhes_voo(frame, voo, app):
    """
    Função para exibir os detalhes de um voo específico em um frame.
    """
    # Criação de um frame para o voo
    voo_frame = ctk.CTkFrame(frame, fg_color="white")
    voo_frame.pack(fill="x", padx=10, pady=10, expand=True)

    # Exibe os detalhes do voo
    ctk.CTkLabel(voo_frame, text_color="black", text=f"Voo {voo[0].id}", font=("Arial", 14, "bold")).grid(row=0, column=0, sticky="w", padx=10, pady=2)
    ctk.CTkLabel(voo_frame, text_color="black", text=f"{voo[0].origem} para {voo[0].destino}", font=("Arial", 12)).grid(row=1, column=0, sticky="w", padx=10, pady=1)
    ctk.CTkLabel(voo_frame, text_color="black", text=f"Preço: R$ {voo[0].preco}", font=("Arial", 12)).grid(row=2, column=0, sticky="w", padx=10, pady=1)

    # Exibe o assento selecionado
    ctk.CTkLabel(voo_frame, text_color="black", text=f"Assento: {voo[1].assento}", font=("Arial", 12)).grid(row=3, column=0, sticky="w", padx=10, pady=1)

    # Botão para deletar a passagem
    ctk.CTkButton(voo_frame, text="Deletar", hover_color="#470a0a", fg_color="red", command=lambda: deletar_voo(app, voo[1]), width=200).grid(row=4, column=0, padx=10, pady=5)

def exibir_lista_voos(frame, lista_voos, app):
    """
    Função para exibir a lista de voos em um frame.
    Limpa itens anteriores e exibe cada voo na lista.
    """
    for widget in frame.winfo_children():  # Limpa os itens anteriores
        widget.destroy()

    if isinstance(lista_voos, list):  # Verifica se é uma lista
        for voo in lista_voos:
            exibir_detalhes_voo(frame, voo, app)  # Exibe detalhes de cada voo
    else:
        exibir_detalhes_voo(frame, lista_voos[0], app)  # Exibe detalhes de um único voo

def exibir_consulta_voos(app, user_token):
    """
    Função para exibir a consulta de voos do usuário.
    Limpa a janela e exibe a lista de passagens.
    """
    global scrollbar, token
    token = user_token  # Armazena o token do usuário
    from cliente_main import client  # Importa o cliente para manipulação de dados

    # Limpa a janela atual
    for widget in app.winfo_children():
        widget.destroy()

    frame = ctk.CTkFrame(app, fg_color="transparent")  # Cria um frame principal
    frame.pack(pady=10, fill="both", expand=True)

    # Criando um frame rolável
    scrollbar = ctk.CTkScrollableFrame(app, width=400, fg_color="transparent")
    scrollbar.pack(pady=5, fill="both", expand=True)
    
    frame_bottom = ctk.CTkFrame(app, fg_color="transparent")  # Frame para os botões na parte inferior
    frame_bottom.pack(side="bottom", fill="x")

    # Botão de Voltar
    voltar_btn = ctk.CTkButton(frame_bottom, text="Voltar", command=lambda: voltar(app, token))
    voltar_btn.grid(row=0, column=0, columnspan=2, pady=10, padx=5)
    
    # Título da tela
    ctk.CTkLabel(frame, text="Suas Passagens", font=("Arial", 20)).pack(pady=5)

    # Exibindo a lista de voos do usuário
    global voos
    voos = client.lista_de_voos()  # Obtém a lista de voos disponíveis
    user = client.getUser(token)  # Obtém informações do usuário
    voos_user = user.listar_passsagens(user.passagens, voos)  # Filtra as passagens do usuário
    
    if voos_user:  # Se o usuário possui passagens
        exibir_lista_voos(scrollbar, voos_user, app)  # Exibe a lista de passagens
    else:
        # Mensagem caso não haja passagens
        ctk.CTkLabel(scrollbar, text="Você ainda não possui passagens.", font=("Arial", 20, "bold"), text_color="red").pack(pady=20)
