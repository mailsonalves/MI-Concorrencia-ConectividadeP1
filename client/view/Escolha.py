import customtkinter as ctk
import random
import string

# Classe representando o voo
class Voo:
    def __init__(self, origem, destino, partida, chegada, preco):
        self.id_voo = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        self.origem = origem
        self.destino = destino
        self.partida = partida
        self.chegada = chegada
        self.preco = preco
        self.vagas = {'A1': False, 'A2': False}
        self.disponibilidade = any(not ocupada for ocupada in self.vagas.values())

# Função para exibir cada voo
def exibir_detalhes_voo(frame, voo):
    # Frame para cada voo (ajustando a largura para expandir)
    voo_frame = ctk.CTkFrame(frame, fg_color="white",)
    voo_frame.pack(fill="x", padx=10, pady=10, expand=True)

    # Exibe os detalhes do voo
    label_voo = ctk.CTkLabel(voo_frame,text_color="black", text=f"Voo {voo.id_voo}", font=("Arial", 14, "bold"))
    label_voo.grid(row=0, column=0, sticky="w", padx=10, pady=2)

    label_origem_destino = ctk.CTkLabel(voo_frame,text_color="black", text=f"{voo.origem} para {voo.destino}", font=("Arial", 12))
    label_origem_destino.grid(row=1, column=0, sticky="w", padx=10, pady=2)

    label_partida_chegada = ctk.CTkLabel(voo_frame,text_color="black", text=f"Partida: {voo.partida} | Chegada: {voo.chegada}", font=("Arial", 12))
    label_partida_chegada.grid(row=2, column=0, sticky="w", padx=10, pady=2)

    label_preco = ctk.CTkLabel(voo_frame,text_color="black", text=f"Preço: R$ {voo.preco}", font=("Arial", 12))
    label_preco.grid(row=3, column=0, sticky="w", padx=10, pady=2)

    # Botão de Selecionar com largura aumentada
    button_selecionar = ctk.CTkButton(voo_frame, text="Selecionar", command=lambda: print(f"Voo {voo.id_voo} selecionado!"), width=200)
    button_selecionar.grid(row=4, column=0, padx=10, pady=10)

# Função para exibir a lista de voos
def exibir_lista_voos(frame, lista_voos):
    # Exibindo todos os voos da lista
    for voo in lista_voos:
        exibir_detalhes_voo(frame, voo)

# Função para iniciar a interface gráfica
def exibir_listagem_voos(app):
    # Limpa a janela
    for widget in app.winfo_children():
        widget.destroy()
    frame = ctk.CTkFrame(app,fg_color="transparent")
    frame.pack(pady=10, fill="both", expand=True)
    
    # Criando um canvas para o scroll
    scrollbar = ctk.CTkScrollableFrame(app, width=400, fg_color="transparent")  # Aumentando a largura do scroll frame
    scrollbar.pack(pady=40, fill="both", expand=True)
    
    label_title = ctk.CTkLabel(frame, text="Resultado da pesquisa", font=("Arial", 20))
    label_title.pack(pady=5)

    entry_frame = ctk.CTkFrame(frame, fg_color="transparent")
    entry_frame.pack(pady=5)

    # Configurando os campos de entrada "Origem" e "Destino" lado a lado
    entry_origem = ctk.CTkEntry(entry_frame, placeholder_text="Origem", width=150)
    entry_origem.grid(row=0, column=0, padx=10, pady=5)

    entry_destino = ctk.CTkEntry(entry_frame, placeholder_text="Destino", width=150)
    entry_destino.grid(row=0, column=1, padx=10, pady=5)
    
    button_login = ctk.CTkButton(entry_frame, text="Pesquisar", width=50)
    button_login.grid(row=0, column=2, padx=10, pady=5)
    # Criando uma lista de voos de exemplo
    lista_voos = [
        Voo("Salvador", "Recife", "08:00", "10:00", 500),
        Voo("São Paulo", "Rio de Janeiro", "09:00", "11:00", 300),
        Voo("Brasília", "Fortaleza", "10:00", "12:00", 450),
        Voo("Curitiba", "Porto Alegre", "11:00", "13:00", 200),
        Voo("Manaus", "Belém", "12:00", "14:00", 600),
        Voo("Natal", "João Pessoa", "13:00", "15:00", 250),
        Voo("Recife", "Salvador", "16:00", "18:00", 500),
        Voo("Florianópolis", "Brasília", "17:00", "19:00", 400),
        Voo("Fortaleza", "Manaus", "18:00", "20:00", 350),
    ]

    # Exibindo a lista de voos
    exibir_lista_voos(scrollbar, lista_voos)