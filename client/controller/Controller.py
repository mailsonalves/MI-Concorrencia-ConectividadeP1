import socket
import pickle
from model.User import User
from view.View import View
import threading

lock = threading.Lock()

class Cliente:
    """
    Classe que representa um cliente que se conecta a um servidor para realizar operações de compra de passagens aéreas.

    Atributos:
    ----------
    _port : int
        A porta do servidor ao qual o cliente se conecta.
    _host : str
        O endereço do servidor.
    _s : socket.socket
        O socket usado para a conexão com o servidor.
    view : View
        Instância da classe View para interações com o usuário.

    Métodos:
    --------
    __init__(port: int, host: str) -> None
        Inicializa uma instância do cliente com a porta e o host fornecidos.

    start_client() -> None
        Inicia a conexão com o servidor e exibe o menu principal.

    __request(typeOperation: int, data: dict) -> Union[dict, bool]
        Envia uma solicitação ao servidor e aguarda a resposta.

    _cadastro() -> None
        Solicita ao usuário um nome de usuário e senha para registro.

    _login() -> Union[dict, bool]
        Solicita ao usuário suas credenciais e realiza o login.

    _selecionar_voo(user: User) -> None
        Permite que o usuário selecione um voo disponível.

    _confirmar_compra(user: User, voos: list, id_voo_selecionado: str) -> None
        Confirma a compra de uma passagem para um voo específico.

    _imprimir_passagens_user(user: User) -> None
        Imprime as passagens compradas pelo usuário.

    _menu() -> None
        Exibe o menu principal e processa as opções escolhidas pelo usuário.
    """

    def __init__(self, port, host) -> None:
        """
        Inicializa uma nova instância do cliente.

        Parâmetros:
        -----------
        port : int
            A porta do servidor ao qual o cliente se conecta.
        host : str
            O endereço do servidor.
        """
        self._port = port
        self._host = host
        self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.view = View()

    def start_client(self):
        from view.Login import open_login_screen

        """
        Inicia a conexão com o servidor e exibe o menu principal.
        """
        self._s.connect((self._host, self._port))
        open_login_screen()

    def __request(self, typeOperation, data):
        """
        Envia uma solicitação ao servidor e aguarda a resposta.

        Parâmetros:
        -----------
        typeOperation : int
            O tipo de operação a ser realizada no servidor.
        data : dict
            Os dados a serem enviados na solicitação.

        Retorna:
        --------
        Union[dict, bool]
            Retorna os dados desserializados recebidos do servidor ou False em caso de erro.
        """
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
        """
        Solicita ao usuário um nome de usuário e senha para registro.

        Retorna:
        --------
        None
        """
        while True:
            username, password = self.view.solicitar_username_senha()
            new_user = self.__request(
                101, {"username": username, "password_user": password}
            )
            if new_user:
                self.view.mostrar_mensagem("Usuário cadastrado.")
                break
            else:
                self.view.mostrar_mensagem("Usuário já existe!")
   
    def authenticate(self,username,password):
        """
        Solicita ao usuário suas credenciais e realiza o login.

        Retorna:
        --------
        Union[dict, bool]
            Retorna os dados do usuário e token em caso de sucesso, ou False em caso de falha.
        """
        #username, password = self.view.solicitar_username_senha()
        response = self.__request(
            100, {"username": username, "password_user": password}
        )

        if response != False:
            user = response.get("user")
            print(f"\nBem-vindo, {user.name}!\n")
            return response
        else:
            
            print("Login falhou. Verifique suas credenciais e tente novamente.")
            
            return False

    def _selecionar_voo(self, user: User):
        """
        Permite que o usuário selecione um voo disponível.

        Parâmetros:
        -----------
        user : User
            O usuário que está realizando a seleção do voo.

        Retorna:
        --------
        None
        """
        all_trechos = self.__request(201, "")
        origem, destino = self.view.solicitar_origem_destino(all_trechos)

        self.view.mostrar_voos(all_trechos[origem])
        id_voo = self.view.solicitar_id_voo()
        self._confirmar_compra(user, all_trechos[origem], id_voo)

    def _confirmar_compra(self, user, voos, id_voo_selecionado):
        """
        Confirma a compra de uma passagem para um voo específico.

        Parâmetros:
        -----------
        user : User
            O usuário que está comprando a passagem.
        voos : list
            Lista de voos disponíveis.
        id_voo_selecionado : str
            O ID do voo selecionado.

        Retorna:
        --------
        None
        """
        for voo in voos:
            if voo.id == id_voo_selecionado:
                escolha_assento, cpf = self.view.solicitar_assento_e_cpf(voo)
                passagem = user.comprar_passagem(voo, escolha_assento, cpf)
                if passagem and passagem != "Ocupado":
                    self.view.mostrar_mensagem(
                        f"Compra confirmada:\nID do Voo: {passagem.id_voo}\nID do Passageiro: {passagem.id_passageiro}\nCPF: {passagem.cpf}\nAssento: {passagem.assento}"
                    )
                    self.__request(202, passagem)
                    return
                elif passagem == "Ocupado":
                    self.view.mostrar_mensagem("Assento indisponível")
                    return
                else:
                    self.view.mostrar_mensagem("Voo lotado")
                    return

    def _imprimir_passagens_user(self, user):
        """
        Imprime as passagens compradas pelo usuário.

        Parâmetros:
        -----------
        user : User
            O usuário cujas passagens serão impressas.

        Retorna:
        --------
        None
        """
        all_trechos = self.__request(201, "")
        self.view.imprimir_passagem(user.passagens, all_trechos)

    def _menu(self):
        """
        Exibe o menu principal e processa as opções escolhidas pelo usuário.

        Retorna:
        --------
        None
        """
        while True:
            opcao = self.view.mostrar_menu_principal()
            token_user = 0
            if opcao == "1":
                response = self.authenticate()
                user = response.get("user")
                token = response.get("token")
                token_user = token
                if user:
                    while True:
                        self.view.mostrar_mensagem(
                            "[1] Comprar Passagem\n[2] Consultar Passagem\n[3] Voltar ao Menu"
                        )
                        opcao = input("Selecione uma opção: \n")
                        if opcao == "1":
                            self._selecionar_voo(user)
                        elif opcao == "2":
                            user = self.__request(102, token)
                            self._imprimir_passagens_user(user)
                        elif opcao == "3":
                            break

            elif opcao == "2":
                self._cadastro()

            elif opcao == "3":
                self.view.mostrar_mensagem("Encerrando conexão...")
                
                self._s.close()
                break
