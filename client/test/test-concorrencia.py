import socket
import pickle
import time
import concurrent.futures
from model.User import User
from model.Voo import Voo


def simular_cliente(server_host, server_port, client_id):
    """
    Função que simula um cliente enviando uma requisição ao servidor.

    Args:
        server_host (str): Endereço IP do servidor.
        server_port (int): Porta em que o servidor está ouvindo.
        client_id (int): Identificador do cliente para logs.
    
    Retorna:
        str: Resposta do servidor ou mensagem de erro.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Conecta ao servidor
            s.connect((server_host, server_port))
            
            # Dados para envio (por exemplo, autenticação com um código de ação fictício)
            request_data = pickle.dumps((100, {"username": f"admin{client_id}", "password_user": f"password{client_id}"}))
            
            # Envia a requisição
            s.sendall(request_data)
            
            # Recebe a resposta do servidor
            response = s.recv(4096)
            resposta = pickle.loads(response)
            return f"Cliente {client_id}: Resposta do servidor -> {resposta}"
    
    except Exception as e:
        return f"Cliente {client_id}: Erro -> {e}"

def testar_concorrencia(server_host, server_port, num_clientes):
    """
    Função para testar a concorrência de múltiplos clientes se conectando simultaneamente ao servidor.

    Args:
        server_host (str): Endereço IP do servidor.
        server_port (int): Porta em que o servidor está ouvindo.
        num_clientes (int): Número de clientes que serão simulados.

    """
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_clientes) as executor:
        futures = [
            executor.submit(simular_cliente, server_host, server_port, client_id + 1)
            for client_id in range(num_clientes - 1)
        ]
        for future in concurrent.futures.as_completed(futures):
            print(future.result())

# Parâmetros do servidor
server_host = "127.0.0.1"  # Substitua pelo IP do seu servidor
server_port = 65432         # Substitua pela porta do seu servidor

# Número de clientes simultâneos
num_clientes = 10

# Iniciar teste de concorrência
testar_concorrencia(server_host, server_port, num_clientes)
