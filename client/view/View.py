class View():
    def mostrar_menu_principal(self):
        print("\n--- MENU PRINCIPAL ---")
        print("[1] Login")
        print("[2] Cadastre-se")
        print("[3] Sair")
        return input("Selecione uma opção: \n")

    def solicitar_email_senha(self):
        email = input("Informe seu username: \n")
        password = input("Informe sua senha: \n")
        return email, password

    def mostrar_mensagem(self, mensagem):
        print(mensagem)

    def mostrar_voos(self, voos):
        for voo in voos:
            if voo.disponibilidade == True:
                print(f'ID: {voo.id}')
                print(f'Origem: {voo.origem}')
                print(f'Destino: {voo.destino}')
                print(f'Vagas disponíveis:')
                for  assetos,disponibilidade in voo.vagas.items():
                    print(f'[{"Dispnivel" if disponibilidade == False else "Ocupado"}] - {assetos}')
            print("-" * 50)

    def solicitar_origem_destino(self, all_trechos):
        for num, capital in enumerate(all_trechos):
            print(f"[{num}] - {capital}")
        origem = input("Digite de onde você quer partir: \n")
        
        for num in range(len(all_trechos[origem])):
            print(f'[{num}] - {all_trechos[origem][num].destino}')
        destino = input("Digite para onde você quer ir: \n")
        print("-" * 50)
        return origem, destino

    def solicitar_id_voo(self):
        id = input('Selecione o ID do voo: \n')
        print("-" * 50)
        return id
    

    def solicitar_assento_e_cpf(self, voo):
        for num, assetos in enumerate(voo.vagas.keys()):
            print(f'[{num}] - {assetos}')
        escolha_assento = input('Escolha o assento: ')
        cpf = input('Digite seu cpf: ')
        print("-" * 50)
        return escolha_assento, cpf

    def imprimir_passagem(self, passagens_de_voos: list, voos: dict):
        for passagem in passagens_de_voos:
            for voo in voos.values():
                for voo_user in voo:
                    if voo_user.id == passagem.id_voo:
                        print(f'ID: {passagem.id_voo}')
                        print(f'CPF: {passagem.cpf}')
                        print(f'Origem: {voo_user.origem}')
                        print(f'Destino: {voo_user.destino}')
                        print(f'Assento: {passagem.assento}')
                        print("-" * 50)