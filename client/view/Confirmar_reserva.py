import customtkinter as ctk
import tkinter.messagebox as messagebox

def voltar(app, token):
    from view.Escolha import exibir_listagem_voos
    for widget in app.winfo_children():
        widget.destroy()
    exibir_listagem_voos(app, token)

def confirmar_reserva(app, token, passagem):
    messagebox.showinfo("Confirmação de Reserva", f"Compra realizada com sucesso!\n Numero da passagem: {passagem.id}")
    print("Reserva confirmada!")
    voltar(app, token)

def cancelar_compra(app, token, passagem):
    from cliente_main import client
    remove = client.deletar_compra(voos, passagem)
    if remove:
        messagebox.showinfo("Cancelamento", "Compra cancelada com sucesso!")
        voltar(app, token)
    else:
        print('Falha ao cancelar')

def tela_confirmacao_reserva(app, passagem, token):
    from cliente_main import client
    print(passagem)
    voo = client.get_voo(passagem.id_voo)

    # Limpa a janela principal
    for widget in app.winfo_children():
        widget.destroy()

    # Frame principal para centralizar o conteúdo
    frame = ctk.CTkFrame(app, width=300, height=350, fg_color="white")
    frame.pack(pady=20, padx=60, expand=True)

    # Título
    label_title = ctk.CTkLabel(frame, text_color="black", text="Confirmar Reserva", font=("Arial", 18, "bold"))
    label_title.grid(row=0, column=0, columnspan=2, pady=(10, 20))

    # Detalhes da reserva
    ctk.CTkLabel(frame, text_color="black", text=f"Voo: {passagem.id_voo}", font=("Arial", 14)).grid(row=1, column=0, sticky="w", padx=20, pady=5)
    ctk.CTkLabel(frame, text_color="black", text=f"Origem: {voo.origem}", font=("Arial", 14)).grid(row=2, column=0, sticky="w", padx=20, pady=5)
    ctk.CTkLabel(frame, text_color="black", text=f"Destino: {voo.destino}", font=("Arial", 14)).grid(row=3, column=0, sticky="w", padx=20, pady=5)
    ctk.CTkLabel(frame, text_color="black", text=f"Assentos: {passagem.assento}", font=("Arial", 14)).grid(row=4, column=0, sticky="w", padx=20, pady=5)
    ctk.CTkLabel(frame, text_color="black", text=f"Preço Total: R$ {voo.preco}", font=("Arial", 14)).grid(row=5, column=0, sticky="w", padx=20, pady=5)

    # Botões de ação
    button_confirmar = ctk.CTkButton(frame, text="Confirmar Reserva", command=lambda: confirmar_reserva(app, token, passagem), width=300)
    button_confirmar.grid(row=6, column=0, columnspan=2, pady=2, padx=20)

    button_cancelar = ctk.CTkButton(frame, text="Cancelar Compra", command=lambda: cancelar_compra(app, token, passagem), width=300, fg_color="red", hover_color="#470a0a")
    button_cancelar.grid(row=7, column=0, columnspan=2, pady=2, padx=20)

    # Botão de Voltar
    voltar_btn = ctk.CTkButton(frame, text="Voltar", command=lambda: voltar(app, token))
    voltar_btn.grid(row=8, column=0, columnspan=2, pady=10, padx=20)

    global voos
    voos = client.lista_de_voos()

# Inicializando a aplicação
