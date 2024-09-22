import customtkinter as ctk
import tkinter.messagebox as messagebox

def voltar(app, token):
    from view.Escolha import exibir_listagem_voos
    
    # Função que define o comportamento do botão voltar
    for widget in app.winfo_children():
        widget.destroy()
    # Aqui você pode adicionar o código que irá exibir a tela anterior, por exemplo:
    exibir_listagem_voos(app, token)
# Função para confirmar reserva
def confirmar_reserva():
    messagebox.showinfo("Compra Realizada")
    print("Reserva confirmada!")
""" 
def cancelar_compra():
    exibir_listagem_voos()
"""
# Função para exibir a tela de confirmação de reserva
def tela_confirmacao_reserva(app, passagem, token):
    from cliente_main import client
    print(passagem)
    voo = client.get_voo(passagem.id_voo)
    # Limpa a janela principal
    for widget in app.winfo_children():
        widget.destroy()

    # Frame principal para centralizar o conteúdo
    frame = ctk.CTkFrame(app, width=400, height=300, fg_color="white")
    frame.pack(pady=20, padx=60, expand=True)

    # Título
    label_title = ctk.CTkLabel(frame,text_color="black", text="Confirmar Reserva", font=("Arial", 16, "bold"))
    label_title.grid(row=0, column=0, columnspan=2, pady=10)

    # Detalhes da reserva
    label_voo = ctk.CTkLabel(frame,text_color="black", text=f"Voo: {passagem.id_voo}", font=("Arial", 12))
    label_voo.grid(row=1, column=0, sticky="w", padx=10)

    label_origem = ctk.CTkLabel(frame,text_color="black", text=f"Origem: {voo.origem}", font=("Arial", 12))
    label_origem.grid(row=2, column=0, sticky="w", padx=10)

    label_destino = ctk.CTkLabel(frame,text_color="black", text=f"Destino: {voo.destino}", font=("Arial", 12))
    label_destino.grid(row=3, column=0, sticky="w", padx=10)


    label_assentos = ctk.CTkLabel(frame,text_color="black", text=f"Assentos: {passagem.assento}", font=("Arial", 12))
    label_assentos.grid(row=5, column=0, sticky="w", padx=10)

    label_preco_total = ctk.CTkLabel(frame,text_color="black", text=f"Preço Total: R$ {voo.preco}", font=("Arial", 12))
    label_preco_total.grid(row=6, column=0, sticky="w", padx=10)

    # Botão de confirmação
    button_confirmar = ctk.CTkButton(frame, text="Confirmar Reserva", command=confirmar_reserva, width=300)
    button_confirmar.grid(row=7, column=0, columnspan=2, pady=0, padx= 5)
    
    voltar_button = ctk.CTkButton(frame, text="Cancelar Compra", command=confirmar_reserva, width=300)
    voltar_button.grid(row=8, column=0, columnspan=2, pady=2, padx= 5)
    
    frame_bottom = ctk.CTkFrame(app, fg_color="transparent")
    frame_bottom.pack(side="bottom", fill="x")

    # Botão de Voltar
    voltar_btn = ctk.CTkButton(frame_bottom, text="Voltar", command=lambda: voltar(app, token))
    voltar_btn.grid(row=0, column=0, columnspan=2, pady=10, padx=5)

# Inicializando a aplicação

