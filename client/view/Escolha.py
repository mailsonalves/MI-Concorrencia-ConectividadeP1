import customtkinter as ctk
from view.Confirmar_reserva import tela_confirmacao_reserva
import tkinter.messagebox as messagebox

# Função de pesquisa de voos
def pesquisar(app):
    from cliente_main import client

    origem = entry_origem.get()
    destino = entry_destino.get()

    # Limpa os campos de entrada após a pesquisa
    entry_origem.delete(0, ctk.END)
    entry_destino.delete(0, ctk.END)

    lista_voos = client.selecionar_voo(origem, destino)

    # Atualiza a interface com os resultados da pesquisa
    exibir_lista_voos(scrollbar, lista_voos, app)

def radioButton_event(selected_assento):
    global select_voo
    select_voo = selected_assento.get()
    return


# Função para selecionar voo e confirmar a compra
def selecionar_voo(app, voo_id):
    from cliente_main import client

    user = client.getUser(token)
    print(select_voo)
    if select_voo == '':
        # Exibe mensagem de erro se nenhum assento for selecionado
        messagebox.showerror("Erro", "Por favor, selecione um assento.")
    else:
        passagem = client.confirmar_compra(user, voos, voo_id, select_voo)
        print(f'esolha: {passagem}')
        tela_confirmacao_reserva(app, passagem)
        



# Função para exibir detalhes de cada voo
def exibir_detalhes_voo(frame, voo, app):
    

    # Criação de um frame para o voo
    voo_frame = ctk.CTkFrame(frame, fg_color="white")
    voo_frame.pack(fill="x", padx=10, pady=10, expand=True)

    # Exibe os detalhes do voo
    ctk.CTkLabel(voo_frame, text=f"Voo {voo.id}", font=("Arial", 14, "bold")).grid(row=0, column=0, sticky="w", padx=10, pady=2)
    ctk.CTkLabel(voo_frame, text=f"{voo.origem} para {voo.destino}", font=("Arial", 12)).grid(row=1, column=0, sticky="w", padx=10, pady=1)
    ctk.CTkLabel(voo_frame, text=f"Preço: R$ {voo.preco}", font=("Arial", 12)).grid(row=2, column=0, sticky="w", padx=10, pady=1)

    # Seção de seleção de assento
    ctk.CTkLabel(voo_frame, text="Selecione o assento:", font=("Arial", 12)).grid(row=3, column=0, sticky="w", padx=10, pady=1)
    selected_assento = ctk.StringVar(value="00")

    
    # Botões de seleção de assento
    radio_a1 = ctk.CTkRadioButton(voo_frame, text=list(voo.vagas.keys())[0], text_color="black", fg_color="#0377fc", value=list(voo.vagas.keys())[0], variable=selected_assento, command=lambda: radioButton_event(selected_assento))
    radio_a1.grid(row=4, column=0, padx=10, pady=1, sticky="w")

    # RadioButton para o segundo assento
    radio_a2 = ctk.CTkRadioButton(voo_frame, text=list(voo.vagas.keys())[1], text_color="black", fg_color="#0377fc", value=list(voo.vagas.keys())[1], variable=selected_assento, command=lambda: radioButton_event(selected_assento))
    radio_a2.grid(row=5, column=0, padx=10, pady=1, sticky="w")

    # Botão de Selecionar
    ctk.CTkButton(voo_frame, text="Selecionar", command=lambda: selecionar_voo(app, voo.id), width=200).grid(row=6 + len(voo.vagas.keys()), column=0, padx=10, pady=5)

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
        exibir_detalhes_voo(frame, lista_voos, app)

# Função para iniciar a interface gráfica
def exibir_listagem_voos(app, user_token):
    global entry_origem, entry_destino, scrollbar, token
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

    # Título
    ctk.CTkLabel(frame, text="Resultado da pesquisa", font=("Arial", 20)).pack(pady=5)

    # Campos de entrada "Origem" e "Destino"
    entry_frame = ctk.CTkFrame(frame, fg_color="transparent")
    entry_frame.pack(pady=5)

    entry_origem = ctk.CTkEntry(entry_frame, placeholder_text="Origem", width=150)
    entry_origem.grid(row=0, column=0, padx=10, pady=5)

    entry_destino = ctk.CTkEntry(entry_frame, placeholder_text="Destino", width=150)
    entry_destino.grid(row=0, column=1, padx=10, pady=5)

    # Botão de pesquisa
    ctk.CTkButton(entry_frame, text="Pesquisar", width=50, command=lambda: pesquisar(app)).grid(row=0, column=2, padx=10, pady=5)

    # Exibindo a lista de voos
    global voos
    voos = client.lista_de_voos()
    exibir_lista_voos(scrollbar, voos, app)
