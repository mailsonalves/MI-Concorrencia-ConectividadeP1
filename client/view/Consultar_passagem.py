import customtkinter as ctk
def radioButton_event(selected_assento):
    global select_voo
    select_voo = selected_assento.get()
    return


# Função para selecionar voo e confirmar a compra
def selecionar_voo(app, voo_id):
    from cliente_main import client

    user = client.getUser(token)
    
def voltar(app, token):
    from view.Menu import open_menu
    
    # Função que define o comportamento do botão voltar
    for widget in app.winfo_children():
        widget.destroy()
    # Aqui você pode adicionar o código que irá exibir a tela anterior, por exemplo:
    open_menu(app, token)
# Função para exibir detalhes de cada voo
def exibir_detalhes_voo(frame, voo, app):
    

    # Criação de um frame para o voo
    voo_frame = ctk.CTkFrame(frame, fg_color="white")
    voo_frame.pack(fill="x", padx=10, pady=10, expand=True)

    # Exibe os detalhes do voo
    ctk.CTkLabel(voo_frame, text_color="black", text=f"Voo {voo[0].id}", font=("Arial", 14, "bold")).grid(row=0, column=0, sticky="w", padx=10, pady=2)
    ctk.CTkLabel(voo_frame, text_color="black",text=f"{voo[0].origem} para {voo[0].destino}", font=("Arial", 12)).grid(row=1, column=0, sticky="w", padx=10, pady=1)
    ctk.CTkLabel(voo_frame, text_color="black",text=f"Preço: R$ {voo[0].preco}", font=("Arial", 12)).grid(row=2, column=0, sticky="w", padx=10, pady=1)

    # Seção de seleção de assento
    ctk.CTkLabel(voo_frame, text_color="black",text=f"Assento: {voo[1].assento}", font=("Arial", 12)).grid(row=3, column=0, sticky="w", padx=10, pady=1)

    # Botão de Selecionar
    ctk.CTkButton(voo_frame, text="Deletar",hover_color="#470a0a", fg_color="red",command=lambda: selecionar_voo(app, voo.id), width=200).grid(row=4 , column=0, padx=10, pady=5)


# Função para exibir a lista de voos
def exibir_lista_voos(frame, lista_voos, app):
    # Limpa os itens anteriores
    for widget in frame.winfo_children():
        widget.destroy()

    # Exibe cada voo da lista
    if isinstance(lista_voos, list):
        for voo in lista_voos:
            exibir_detalhes_voo(frame, voo, app)
    else:
        exibir_detalhes_voo(frame, lista_voos[0], app)

# Função para iniciar a interface gráfica
def exibir_consulta_voos(app, user_token):
    global scrollbar, token
    token = user_token
    from cliente_main import client

    # Limpa a janela
    for widget in app.winfo_children():
        widget.destroy()

    frame = ctk.CTkFrame(app, fg_color="transparent")
    frame.pack(pady=10, fill="both", expand=True)

    # Criando um frame rolável
    scrollbar = ctk.CTkScrollableFrame(app, width=400, fg_color="transparent")
    scrollbar.pack(pady=5, fill="both", expand=True)
    
    frame_bottom = ctk.CTkFrame(app, fg_color="transparent")
    frame_bottom.pack(side="bottom", fill="x")

    # Botão de Voltar
    voltar_btn = ctk.CTkButton(frame_bottom, text="Voltar",  command=lambda: voltar(app, token))
    voltar_btn.grid(row=0, column=0, columnspan=2, pady=10, padx=5)
    # Título
    ctk.CTkLabel(frame, text="Suas Passagens", font=("Arial", 20)).pack(pady=5)

    # Exibindo a lista de voos
    global voos
    voos = client.lista_de_voos()
    user = client.getUser(token)
    voos_user = user.listar_passsagens(user.passagens, voos)
    print(voos_user)
    exibir_lista_voos(scrollbar, voos_user, app)
