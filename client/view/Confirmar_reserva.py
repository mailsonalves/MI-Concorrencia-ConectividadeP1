import customtkinter as ctk
import tkinter.messagebox as messagebox

def voltar(app, token, passagem):
    """
    Função para voltar à tela de listagem de voos após confirmação ou cancelamento de reserva.
    A tela atual é destruída e a função de exibir listagem de voos é chamada.
    """
    from view.Escolha import exibir_listagem_voos  # Importa a função de exibição de voos
    for widget in app.winfo_children():  # Remove todos os widgets da janela atual
        widget.destroy()
    cancelar_compra(app, token, passagem, True)  # Chama a função de cancelamento (opcional, pode ser ajustada)
    exibir_listagem_voos(app, token)  # Exibe a tela de listagem de voos

def confirmar_reserva(app, token, passagem):
    """
    Função que exibe a mensagem de sucesso ao confirmar a reserva e, em seguida, retorna à tela de listagem.
    """
    messagebox.showinfo("Confirmação de Reserva", f"Compra realizada com sucesso!\nNúmero da passagem: {passagem.id}")
    print("Reserva confirmada!")
    voltar(app, token, passagem)  # Chama a função para retornar à listagem de voos

def cancelar_compra(app, token, passagem, voltar):
    """
    Função que cancela a compra de uma passagem. 
    Se o cancelamento for bem-sucedido, exibe uma mensagem de confirmação e retorna à listagem de voos.
    """
    from cliente_main import client  # Importa o cliente para manipulação de dados
    voos = client.lista_de_voos()  # Obtém a lista de voos disponíveis
    remove = client.deletar_compra(voos, passagem)  # Tenta deletar a compra
    if remove and voltar == False:  # Se a compra foi cancelada com sucesso
        messagebox.showinfo("Cancelamento", "Compra cancelada com sucesso!")
        voltar(app, token, passagem)  # Retorna à listagem de voos

def tela_confirmacao_reserva(app, passagem, token):
    """
    Tela de confirmação de reserva. Exibe os detalhes do voo e as opções para confirmar ou cancelar a compra.
    """
    from cliente_main import client  # Importa o cliente para manipulação de dados
    print(passagem)  # Exibe a passagem atual no console (para depuração)
    voo = client.get_voo(passagem.id_voo)  # Obtém os detalhes do voo baseado no ID da passagem

    # Limpa a janela principal (remove todos os widgets atuais)
    for widget in app.winfo_children():
        widget.destroy()

    # Cria o frame principal para centralizar o conteúdo na janela
    frame = ctk.CTkFrame(app, width=300, height=350, fg_color="white")
    frame.pack(pady=20, padx=60, expand=True)

    # Título da tela de confirmação
    label_title = ctk.CTkLabel(frame, text_color="black", text="Confirmar Reserva", font=("Arial", 18, "bold"))
    label_title.grid(row=0, column=0, columnspan=2, pady=(10, 20))

    # Exibição dos detalhes da reserva
    ctk.CTkLabel(frame, text_color="black", text=f"Voo: {passagem.id_voo}", font=("Arial", 14)).grid(row=1, column=0, sticky="w", padx=20, pady=5)
    ctk.CTkLabel(frame, text_color="black", text=f"Origem: {voo.origem}", font=("Arial", 14)).grid(row=2, column=0, sticky="w", padx=20, pady=5)
    ctk.CTkLabel(frame, text_color="black", text=f"Destino: {voo.destino}", font=("Arial", 14)).grid(row=3, column=0, sticky="w", padx=20, pady=5)
    ctk.CTkLabel(frame, text_color="black", text=f"Assentos: {passagem.assento}", font=("Arial", 14)).grid(row=4, column=0, sticky="w", padx=20, pady=5)
    ctk.CTkLabel(frame, text_color="black", text=f"Preço Total: R$ {voo.preco}", font=("Arial", 14)).grid(row=5, column=0, sticky="w", padx=20, pady=5)

    # Botão para confirmar a reserva
    button_confirmar = ctk.CTkButton(frame, text="Confirmar Reserva", command=lambda: confirmar_reserva(app, token, passagem), width=300)
    button_confirmar.grid(row=6, column=0, columnspan=2, pady=2, padx=20)

    # Botão para cancelar a compra
    button_cancelar = ctk.CTkButton(frame, text="Cancelar Compra", command=lambda: cancelar_compra(app, token, passagem, False), width=300, fg_color="red", hover_color="#470a0a")
    button_cancelar.grid(row=7, column=0, columnspan=2, pady=2, padx=20)

    # Botão de voltar para a listagem de voos
    voltar_btn = ctk.CTkButton(frame, text="Voltar", command=lambda: voltar(app, token, passagem))
    voltar_btn.grid(row=8, column=0, columnspan=2, pady=10, padx=20)

    # Carrega a lista de voos
    global voos  # Variável global para armazenar a lista de voos
    voos = client.lista_de_voos()  # Chama o cliente para obter a lista de voos

# Inicializando a aplicação
