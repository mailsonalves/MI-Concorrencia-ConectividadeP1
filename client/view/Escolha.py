import customtkinter as ctk
from view.Confirmar_reserva import tela_confirmacao_reserva
import tkinter.messagebox as messagebox

def formatar_string(text: str):
    """Formata a string para título e remove espaços em branco."""
    return text.title().strip()

# Função de pesquisa de voos
def pesquisar(app, token):
    from cliente_main import client

    origem = entry_origem.get()
    destino = entry_destino.get()

    origem = formatar_string(origem)
    destino = formatar_string(destino)
    
    # Limpa os campos de entrada após a pesquisa
    entry_origem.delete(0, ctk.END)
    entry_destino.delete(0, ctk.END)

    lista_voos = client.selecionar_voo(origem, destino)
    
    # Atualiza a interface com os resultados da pesquisa
    for widget in scrollbar.winfo_children():
        widget.destroy()  # Limpa resultados anteriores
    
    if lista_voos:
        exibir_lista_voos(scrollbar, lista_voos, app, token)
    else:
        # Mensagem caso não haja passagens
        ctk.CTkLabel(scrollbar, text="Voo não encontrado", font=("Arial", 20, "bold"), text_color="red").pack(pady=20)

def radioButton_event(selected_assento):
    """Atualiza a seleção do assento."""
    global select_voo
    select_voo = selected_assento.get()

# Função para selecionar voo e confirmar a compra
def selecionar_voo(app, voo_id, token):
    from cliente_main import client

    user = client.getUser(token)
    
    if select_voo.strip() == "":
        # Exibe mensagem de erro se nenhum assento for selecionado
        messagebox.showerror("Erro", "Por favor, selecione um assento.")
    else:
        passagem = client.confirmar_compra(user, voos, voo_id, select_voo)
        if passagem and passagem != 'Ocupado':
            tela_confirmacao_reserva(app, passagem, token)
        else:
            messagebox.showerror("Erro", "Assento ocupado, tente outro!")

# Função para exibir detalhes de cada voo
def exibir_detalhes_voo(frame, voo, app, token):
    """Exibe os detalhes do voo e opções de assento."""
    voo_frame = ctk.CTkFrame(frame, fg_color="white")
    voo_frame.pack(fill="x", padx=10, pady=10, expand=True)

    # Exibe os detalhes do voo
    ctk.CTkLabel(voo_frame, text_color="black", text=f"Voo {voo.id}", font=("Arial", 14, "bold")).grid(row=0, column=0, sticky="w", padx=10, pady=2)
    ctk.CTkLabel(voo_frame, text_color="black", text=f"{voo.origem} para {voo.destino}", font=("Arial", 12)).grid(row=1, column=0, sticky="w", padx=10, pady=1)
    ctk.CTkLabel(voo_frame, text_color="black", text=f"Preço: R$ {voo.preco}", font=("Arial", 12)).grid(row=2, column=0, sticky="w", padx=10, pady=1)

    # Seção de seleção de assento
    ctk.CTkLabel(voo_frame, text_color="black", text="Selecione o assento:", font=("Arial", 12)).grid(row=3, column=0, sticky="w", padx=10, pady=1)
    selected_assento = ctk.StringVar(value=" ")

    # Botões de seleção de assento
    for idx, vaga in enumerate(voo.vagas.keys()):
        ctk.CTkRadioButton(voo_frame, text=vaga, text_color="black", fg_color="#0377fc", value=vaga, variable=selected_assento,
                           command=lambda: radioButton_event(selected_assento)).grid(row=4 + idx, column=0, padx=10, pady=1, sticky="w")

    # Botão de Selecionar
    ctk.CTkButton(voo_frame, text="Selecionar", command=lambda: selecionar_voo(app, voo.id, token), width=200).grid(row=5 + len(voo.vagas.keys()), column=0, padx=10, pady=5)

# Função para exibir a lista de voos
def exibir_lista_voos(frame, lista_voos, app, token):
    """Exibe a lista de voos disponíveis."""
    # Limpa os itens anteriores
    for widget in frame.winfo_children():
        widget.destroy()

    if isinstance(lista_voos, list):
        for voo in lista_voos:
            if not all(voo.vagas.values()):  # Verifica se há assentos disponíveis
                exibir_detalhes_voo(frame, voo, app, token)
    else:
        if not all(lista_voos.vagas.values()):  # Caso único de voo
            exibir_detalhes_voo(frame, lista_voos, app, token)
        else:
            ctk.CTkLabel(scrollbar, text="Esse voo já alcançou a lotação máxima", font=("Arial", 20, "bold"), text_color="red").pack(pady=20)

def voltar(app, token):
    """Define o comportamento do botão 'Voltar'."""
    from view.Menu import open_menu
    
    for widget in app.winfo_children():
        widget.destroy()
    open_menu(app, token)

# Função para iniciar a interface gráfica
def exibir_listagem_voos(app, user_token):
    """Configura e exibe a tela de pesquisa de voos."""
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
    ctk.CTkLabel(frame, text="Pesquise seu voo", font=("Arial", 20)).pack(pady=5)

    # Campos de entrada "Origem" e "Destino"
    entry_frame = ctk.CTkFrame(frame, fg_color="transparent")
    entry_frame.pack(pady=5)

    entry_origem = ctk.CTkEntry(entry_frame, placeholder_text="Origem", width=150)
    entry_origem.grid(row=0, column=0, padx=10, pady=5)

    entry_destino = ctk.CTkEntry(entry_frame, placeholder_text="Destino", width=150)
    entry_destino.grid(row=0, column=1, padx=10, pady=5)
    
    frame_bottom = ctk.CTkFrame(app, fg_color="transparent")
    frame_bottom.pack(side="bottom", fill="x")

    # Botão de Voltar
    voltar_btn = ctk.CTkButton(frame_bottom, text="Voltar", command=lambda: voltar(app, token))
    voltar_btn.grid(row=0, column=0, columnspan=2, pady=10, padx=5)

    # Botão de pesquisa
    ctk.CTkButton(entry_frame, text="Pesquisar", width=50, command=lambda: pesquisar(app, token)).grid(row=0, column=2, padx=10, pady=5)
    ctk.CTkButton(entry_frame, text="Reload", width=50, command=lambda: exibir_lista_voos(scrollbar, voos, app, token)).grid(row=0, column=3, padx=1, pady=5)
    
    # Exibindo a lista de voos
    global voos
    voos = client.lista_de_voos()
    if voos:
        exibir_lista_voos(scrollbar, voos, app, token)
    else:
        # Mensagem caso não haja passagens
        ctk.CTkLabel(scrollbar, text="Não foi possível achar voos", font=("Arial", 20, "bold"), text_color="red").pack(pady=20)
