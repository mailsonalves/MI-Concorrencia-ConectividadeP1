import socket
import threading
import pickle
import json
import secrets
import concurrent.futures
from model.Passagem import Passagem
from model.Voo import Voo
from model.User import User
from seed import gerar_user,gerar_voos

lock = threading.Lock()
voos = {}
passagem = {}
users = {}
sessions_activate = {}

class Servidor():
    def __init__(self, port, host) -> None:
        self._port = port
        self._host = host
        self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        gerar_voos(voos)
        gerar_user(users)

        
    def start_server(self):
        self._s.bind((self._host, self._port))
        self._s.listen()
        print(f"Servidor ouvindo em {self._host}:{self._port}")
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor: #Limita a quantiadade de thread
                while True:
                    conn, client = self._s.accept() 
                    executor.submit(self._service, conn, client)
           

        except Exception as e:
            print(f"Ocorreu um erro ao inicializar o serivdor {e}")

                
    def _service(self,conn, cliente):
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
                                username = user_info.get('username')
                                password_user = user_info.get('password_user')
                                for user in users.values():
                                    if user.username == username and user.password == password_user:
                                        session_token = secrets.token_hex(16)
                                        sessions_activate[session_token] = user.id_user
                                        conn.sendall(pickle.dumps({'token': session_token, 'user': user}))
                                        break
                                else:
                                    
                                    conn.sendall(pickle.dumps(False))
                            
                            elif action_code == 102:
                                token = user_info
                                user = users[sessions_activate[token]]
                                conn.sendall(pickle.dumps(user))
                                
                                    
                            elif action_code == 101:
                                for user in users.values():  
                                    if user_info.get('username') == user.username:
                                        conn.sendall(pickle.dumps(False))
                                    else:
                                        with lock:
                                            new_user = User(user_info.get('username'), user_info.get('password'))
                                            users[new_user.id_user] = new_user
                                            conn.sendall(pickle.dumps(True))
                                    
                            elif action_code == 201:  
                                conn.sendall(pickle.dumps(voos))
                            
                            elif action_code == 202:
                                with lock:
                                    for voo in voos.values():
                                        for num in range(len(voo)):
                                            if voo[num].id == user_info.id_voo:
                                                if (voo[num].vagas[user_info.assento] != True):
                                                    users[user_info.id_passageiro].passagens.append(user_info)
                                                    voo[num].vagas[user_info.assento] = True
                                                    conn.sendall(pickle.dumps(True))
                                                    print(f'Compra realizada, Cliente -> [{self._host}] :[{self._port}]')
                                                    break
                                                else:
                                                    conn.sendall(pickle.dumps(False))
                                                    print('assento ocupado')
                                                    break

                                        
                                
                        except pickle.UnpicklingError:
                            print("Erro ao desserializar os dados recebidos.")
                    
                    else:
                        print("Recebido um tipo inesperado de dado.")
                except ConnectionResetError:
                    print(f"Erro de conexão com {cliente}: A conexão foi resetada.")

                    break
                    