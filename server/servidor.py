import socket
import threading
import pickle
import json
import secrets
import concurrent.futures
from model.User import User
from seed import gerar_user, gerar_voos

lock = threading.Lock()
voos = {}
passagem = {}
users = {}
sessions_activate = {}


class Servidor:
    """
    Classe responsável por implementar o servidor de reserva de passagens aéreas.

    Atributos:
        _port (int): Porta na qual o servidor será executado.
        _host (str): Endereço IP do host onde o servidor será executado.
        _s (socket): Objeto socket utilizado para estabelecer conexões.
    """

    def __init__(self, port: int, host: str) -> None:
        """
        Inicializa o servidor com a porta e host especificados.

        Args:
            port (int): Porta na qual o servidor vai ouvir as conexões.
            host (str): Endereço IP do servidor.
        """
        self._port = port
        self._host = host
        self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        gerar_voos(voos)
        gerar_user(users)

    def start_server(self):
        """
        Inicia o servidor, ouvindo as conexões de clientes e criando um pool de threads 
        para lidar com múltiplos clientes simultaneamente.
        """
        self._s.bind((self._host, self._port))
        self._s.listen()
        print(f"Servidor ouvindo em {self._host}:{self._port}")
        try:
            with concurrent.futures.ThreadPoolExecutor(
                max_workers=10
            ) as executor:  # Limita a quantidade de threads
                while True:
                    conn, client = self._s.accept()
                    executor.submit(self._service, conn, client)

        except Exception as e:
            print(f"Ocorreu um erro ao inicializar o servidor: {e}")

    def _service(self, conn, cliente) -> None:
        """
        Método responsável por lidar com a comunicação de um cliente específico.

        Args:
            conn (socket): Objeto socket para se comunicar com o cliente.
            cliente (tuple): Endereço do cliente.
        """
        with conn:
            print(f"Conectado por {cliente}")
            while True:
                try:
                    data = conn.recv(4096)
                    if not data:
                        break
                    if isinstance(data, bytes):
                        try:
                            deserialized_data = pickle.loads(data)
                            action_code = deserialized_data[0]
                            user_info = deserialized_data[1]

                            if action_code == 100:
                                """
                                Autentica o usuário com base no username e senha fornecidos.
                                
                                Args:
                                    user_info (dict): Contém "username" e "password_user".
                                
                                Resposta:
                                    Envia um token de sessão se a autenticação for bem-sucedida.
                                    Caso contrário, retorna False.
                                """
                                username = user_info.get("username")
                                password_user = user_info.get("password_user")
                                for user in users.values():
                                    if (
                                        user.username == username
                                        and user.password == password_user
                                    ):
                                        session_token = secrets.token_hex(16)
                                        sessions_activate[session_token] = user.id_user
                                        conn.sendall(
                                            pickle.dumps(
                                                {"token": session_token, "user": user}
                                            )
                                        )
                                        break
                                else:
                                    conn.sendall(pickle.dumps(False))

                            elif action_code == 102:
                                """
                                Verifica a sessão ativa de um usuário com base no token.

                                Args:
                                    token (str): Token de sessão do usuário.

                                Resposta:
                                    Retorna o objeto do usuário associado ao token.
                                """
                                token = user_info
                                user = users[sessions_activate[token]]
                                conn.sendall(pickle.dumps(user))

                            elif action_code == 101:
                                """
                                Registra um novo usuário no sistema.

                                Args:
                                    user_info (dict): Contém "username" e "password" do novo usuário.

                                Resposta:
                                    Retorna True se o usuário for criado com sucesso, 
                                    ou False se o username já estiver em uso.
                                """
                                for user in users.values():
                                    if user_info.get("username") == user.username:
                                        conn.sendall(pickle.dumps(False))
                                    else:
                                        with lock:
                                            new_user = User(
                                                user_info.get("username"),
                                                user_info.get("password"),
                                            )
                                            users[new_user.id_user] = new_user
                                            conn.sendall(pickle.dumps(True))

                            elif action_code == 201:
                                """
                                Envia a lista de voos disponíveis.

                                Resposta:
                                    Retorna o dicionário contendo os voos disponíveis.
                                """
                                conn.sendall(pickle.dumps(voos))

                            elif action_code == 202:
                                """
                                Realiza a compra de uma passagem para um voo específico.

                                Args:
                                    user_info (Passagem): Objeto Passagem contendo detalhes da compra.

                                Resposta:
                                    Retorna True se a compra for realizada com sucesso,
                                    ou False se o assento já estiver ocupado.
                                """
                                with lock:
                                    for voo in voos.values():
                                        for num in range(len(voo)):
                                            if voo[num].id == user_info.id_voo:
                                                if (
                                                    voo[num].vagas[user_info.assento]
                                                    != True
                                                ):
                                                    users[
                                                        user_info.id_passageiro
                                                    ].passagens.append(user_info)
                                                    voo[num].vagas[
                                                        user_info.assento
                                                    ] = True
                                                    conn.sendall(pickle.dumps(True))
                                                    print(
                                                        f"Compra realizada, Cliente -> [{self._host}] :[{self._port}]"
                                                    )
                                                    break
                                                else:
                                                    conn.sendall(pickle.dumps(False))
                                                    print("Assento ocupado")
                                                    break

                        except pickle.UnpicklingError:
                            print("Erro ao desserializar os dados recebidos.")

                    else:
                        print("Recebido um tipo inesperado de dado.")
                except ConnectionResetError:
                    print(f"Erro de conexão com {cliente}: A conexão foi resetada.")
                    break
