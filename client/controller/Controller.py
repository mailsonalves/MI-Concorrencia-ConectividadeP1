import socket
import pickle
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

    def cadastro( self, username, password, name):
        """
        Solicita ao usuário um nome de usuário e senha para registro.

        Retorna:
        --------
        None
        """
        new_user = self.__request(101, {"username": username, "password_user": password, "name": name}
        )
        if new_user == True:
            print("Usuário cadastrado.")
            return True
        else:
            print("Usuário já existe!")
            return False
   
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

    def lista_de_voos(self):
        all_trechos = self.__request(201, "")  # all_trechos é um dicionário cujos valores são listas

        # Inicializando uma lista para armazenar todos os valores combinados
        combined_list = []

        # Iterando sobre os valores de all_trechos e adicionando todos à lista combinada
        for trechos in all_trechos.values():
            combined_list.extend(trechos)

        return combined_list

        
        
    
    def selecionar_voo(self, origem, destino):
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
        try:
            for voo in all_trechos[origem]:
                if voo.destino == destino:
                    return voo
            else:
                return False
        except KeyError:
            return False


    def confirmar_compra(self, user, voos, id_voo_selecionado, assento):
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
                passagem = user.comprar_passagem(voo, assento, cpf = '5465654654')
                if passagem and passagem != "Ocupado":
                    print(f"Compra confirmada")
                    self.__request(202, passagem)
                    return passagem
                elif passagem == "Ocupado":
                    print("Assento indisponível")
                    return False
                else:
                    print("Voo lotado")
                    return "Ocupado"
                
    def deletar_compra(self, voos, passagem):
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
            if voo.id == passagem.id_voo:
                    self.__request(203, passagem)
                    return True
        return False

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

    
    def getUser(self, token):
        return self.__request(102, token)
        
    
                        
    def get_voo(self, id_voo):
        voos = self.__request(201, "")
        for voo in voos.values():
                for voo_list in voo:
                    if voo_list.id == id_voo:
                        return voo_list
        return False