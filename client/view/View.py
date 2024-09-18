class View():
    def mostrar_menu_principal(self):
        print("\n------| MENU PRINCIPAL |------")
        print("[1] Login")
        print("[2] Cadastre-se")
        print("[3] Sair")
        return input("Selecione uma opção: \n")

    def solicitar_username_senha(self):
        username = input("Informe seu username: \n")
        password = input("Informe sua senha: \n")
        return username, password

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
            print("-" * 60)

    def solicitar_origem_destino(self, all_trechos):
        # Exibe todas as capitais disponíveis com seus respectivos índices
        for num, capital in enumerate(all_trechos):
            print(f"[{num}] - {capital}")
        
        # Solicita o índice da origem
        origem_index = int(input("Digite o número da cidade de onde você quer partir: \n"))
        origem = list(all_trechos.keys())[origem_index]
        
        # Exibe todos os destinos disponíveis a partir da origem escolhida
        for num, trecho in enumerate(all_trechos[origem]):
            print(f'[{num}] - {trecho.destino}')
        
        # Solicita o índice do destino
        destino_index = int(input("Digite o número do destino: \n"))
        destino = all_trechos[origem][destino_index].destino
        
        print("-" * 60)
        return origem, destino

    def solicitar_id_voo(self):
        id = input('Selecione o ID do voo: \n')
        print("-" * 60)
        return id
    

    def solicitar_assento_e_cpf(self, voo):
        for num, assetos in enumerate(voo.vagas.keys()):
            print(f'[{num}] - {assetos}')
        escolha_assento = int(input('Escolha o assento: '))
        escolha_assento = list(voo.vagas.keys())[escolha_assento]
        cpf = input('Digite seu cpf: ')
        print("-" * 60)
        return escolha_assento, cpf

    def imprimir_passagem(self, passagens_de_voos: list, voos: dict):
        for passagem in passagens_de_voos:
            for voo in voos.values():
                for voo_user in voo:
                    if voo_user.id == passagem.id_voo:
                        print("-" * 60)
                        print(f'ID: {passagem.id_voo}')
                        print(f'CPF: {passagem.cpf}')
                        print(f'Origem: {voo_user.origem}')
                        print(f'Destino: {voo_user.destino}')
                        print(f'Assento: {passagem.assento}')
                        print("-" * 60)