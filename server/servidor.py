import socket
import threading
import pickle
import json
import concurrent.futures
from model.Passagem import Passagem
from model.Voo import Voo
from model.User import User

voos = {}
passagem = {}

capitais_brasil = {
    "Brasília": ["São Paulo", "Rio de Janeiro", "Salvador", "Belo Horizonte", "Curitiba"],
    "São Paulo": ["Rio de Janeiro", "Brasília", "Salvador", "Belo Horizonte", "Porto Alegre", "Curitiba", "Recife"],
    "Rio de Janeiro": ["São Paulo", "Brasília", "Salvador", "Belo Horizonte", "Porto Alegre", "Recife"],
    "Salvador": ["Brasília", "São Paulo", "Rio de Janeiro", "Recife", "Fortaleza", "Belo Horizonte"],
    "Belo Horizonte": ["São Paulo", "Rio de Janeiro", "Brasília", "Salvador", "Curitiba"],
    "Curitiba": ["São Paulo", "Belo Horizonte", "Porto Alegre", "Brasília"],
    "Porto Alegre": ["São Paulo", "Rio de Janeiro", "Curitiba", "Brasília"],
    "Recife": ["Salvador", "Fortaleza", "São Paulo", "Rio de Janeiro", "Brasília"],
    "Fortaleza": ["Salvador", "Recife", "Brasília"],

}
users = {
    
}

class Servidor():
    def __init__(self, port, host) -> None:
        self._port = port
        self._host = host
        self.__allclients = {}
        self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        for capital_origem, destinos in capitais_brasil.items():
            voo_array_temp = []  
            for capital_destino in destinos:
                New_voo = Voo(capital_origem, capital_destino)  
                voo_array_temp.append(New_voo)  
            voos[capital_origem] = voo_array_temp
        for number in range(1,10):
            username: str = 'admin'
            password: str = 'password'
            New_user: User = User(password, username)
            users[New_user.id_user] = New_user
            users[New_user.id_user].username = users[New_user.id_user].username + str(number)
            users[New_user.id_user].password = users[New_user.id_user].password + str(number)

        
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
                                        conn.sendall(pickle.dumps(user))
                                        break
                                else:
                                    conn.sendall(pickle.dumps(False))
                                    
                            elif action_code == 101:
                                for user in users.values():  
                                    if user_info.get('username') == user.username:
                                        conn.sendall(pickle.dumps(False))
                                    else:
                                        new_user = User(user_info.get('username'), user_info.get('password'))
                                        users[new_user.id_user] = new_user
                                        conn.sendall(pickle.dumps(True))
                                    
                            elif action_code == 201:  
                                conn.sendall(pickle.dumps(voos))
                            
                            elif action_code == 202:
                                for voo in voos.values():
                                    for num in range(len(voo)):
                                        if voo[num].id == user_info.id_voo:
                                            if (voo[num].vagas[user_info.assento] != True):
                                                users[user_info.id_passageiro].passagens.append(user_info)
                                                voo[num].vagas[user_info.assento] = True
                                                print('compra realizada')
                                            else:
                                                print('assento ocupado')

                                        
                                
                        except pickle.UnpicklingError:
                            print("Erro ao desserializar os dados recebidos.")
                    
                    else:
                        print("Recebido um tipo inesperado de dado.")
                except ConnectionResetError:
                    print(f"Erro de conexão com {cliente}: A conexão foi resetada.")
                    
                    del self.__allclients[cliente]
                    break
                    