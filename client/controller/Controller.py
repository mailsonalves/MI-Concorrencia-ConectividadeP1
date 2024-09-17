import socket
import pickle
from model.User import User
from view.View import View


class Cliente:
    def __init__(self, port, host) -> None:
        self._port = port
        self._host = host
        self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.view = View()

    def start_client(self):
        self._s.connect((self._host, self._port))
        self._menu()

    def __request(self, typeOperation, data):
        data_serialized = pickle.dumps((typeOperation, data))
        self._s.send(data_serialized)

        response = self._s.recv(4096)
        if not response:
            return False

        try:
            deserialized_data = pickle.loads(response)
            return deserialized_data
        except pickle.UnpicklingError:
            self.view.mostrar_mensagem("Erro ao desserializar os dados recebidos.")
            return None

    def _cadastro(self):
        while True:
            email, password = self.view.solicitar_email_senha()
            new_user = self.__request(
                101, {"username": email, "password_user": password}
            )
            if new_user:
                self.view.mostrar_mensagem("Usuário cadastrado.")
                break
            else:
                self.view.mostrar_mensagem("Usuário já existe!")

    def _login(self):
        email, password = self.view.solicitar_email_senha()
        user = self.__request(100, {"username": email, "password_user": password})

        if user:
            self.view.mostrar_mensagem(f"Bem-vindo, {user.username}!\n")
            return user
        else:
            self.view.mostrar_mensagem(
                "Login falhou. Verifique suas credenciais e tente novamente."
            )
            return False

    def _selecionar_voo(self, user: User):
        all_trechos = self.__request(201, "")
        origem, destino = self.view.solicitar_origem_destino(all_trechos)

        self.view.mostrar_voos(all_trechos[origem])
        id_voo = self.view.solicitar_id_voo()
        self._confirmar_compra(user, all_trechos[origem], id_voo)

    def _confirmar_compra(self, user, voos, id_voo_selecionado):
        for voo in voos:
            if voo.id == id_voo_selecionado:
                escolha_assento, cpf = self.view.solicitar_assento_e_cpf(voo)
                passagem = user.comprar_passagem(voo, escolha_assento, cpf)
                if passagem and passagem != "Ocupado":
                    self.view.mostrar_mensagem(
                        f"Compra confirmada:\nID do Voo: {passagem.id_voo}\nID do Passageiro: {passagem.id_passageiro}\nCPF: {passagem.cpf}\nAssento: {passagem.assento}"
                    )
                    self.__request(202, passagem)
                elif passagem == "Ocupado":
                    self.view.mostrar_mensagem("Assento indisponível")
                else:
                    self.view.mostrar_mensagem("Voo lotado")
                return

    def _menu(self):
        while True:
            opcao = self.view.mostrar_menu_principal()

            if opcao == "1":
                user = self._login()
                if user:
                    while True:
                        self.view.mostrar_mensagem(
                            "[1] Comprar Passagem\n[2] Consultar Passagem"
                        )
                        opcao = input("Selecione uma opção: \n")
                        if opcao == "1":
                            self._selecionar_voo(user)

            elif opcao == "2":
                self._cadastro()

            elif opcao == "3":
                self.view.mostrar_mensagem("Encerrando conexão...")
                self._s.close()
                break
