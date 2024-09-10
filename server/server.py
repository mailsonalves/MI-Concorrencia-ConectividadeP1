import socket
import threading
import pickle
import json


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

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 65432))
    server.listen()
    print(f"Servidor ouvindo em {"local host"}:{65432}")
    try:
            while True:
                conn, client = server.accept() 
                thread = threading.Thread(target=service, args=(conn,client))
                thread.start()
    except Exception as e:
            print(f"Ocorreu um erro ao inicializar o serivdor {e}")

    def service(self,conn, cliente):
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
                                    
                            elif action_code == 201:  
                                conn.sendall(pickle.dumps(voos))
                            
                            elif action_code == 202:
                                users[user_info.id_passageiro].passagens.append(user_info)
                                for voo in voos.values():
                                    for num in range(len(voo)):
                                        if voo[num].id == user_info.id_voo:
                                            if (voo[num].vagas[user_info.assento] != True):
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