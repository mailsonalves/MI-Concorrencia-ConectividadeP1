import socket
import pickle
import concurrent.futures
from model.User import User
from model.Voo import Voo
from model.Passagem import Passagem


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
            
            
            # 1. Simula login (ação de código 100)
            login_data = {"username": f"admin{client_id}", "password_user": f"password{client_id}"}
            login_request = pickle.dumps((100, login_data))
            s.sendall(login_request)
            
            # Recebe resposta de login
            login_response = s.recv(4096)
            login_resposta = pickle.loads(login_response)
            
            if not login_resposta or not login_resposta.get("token"):
                return f"Cliente {client_id}: Falha no login."

            user = login_resposta["user"]
            print(f"Cliente {client_id}: Login bem-sucedido para o usuário {user.name}.")

            # 2. Solicita a lista de voos disponíveis (ação de código 201)
            voo_request = pickle.dumps((201, ""))
            s.sendall(voo_request)
            
            # Recebe a lista de voos
            voo_response = s.recv(4096)
            voos = pickle.loads(voo_response)
            
            if not voos:
                return f"Cliente {client_id}: Nenhum voo disponível."

            # 3. Seleciona um voo e tenta comprar uma passagem
            origem = next(iter(voos))  # Seleciona o primeiro trecho disponível
            voo_selecionado = voos[origem][1]  # Seleciona o primeiro voo da origem
            compra_passagem_data = Passagem(voo_selecionado.id,user.id_user, f"000.000.000-{client_id}")
            compra_passagem_data.assento = 'A1'
        

            compra_request = pickle.dumps((202, compra_passagem_data))
            s.sendall(compra_request)
            
            # Recebe resposta da tentativa de compra
            compra_response = s.recv(4096)
            compra_resposta = pickle.loads(compra_response)

            if compra_resposta:
                return f"Cliente {user.name}: Compra realizada com sucesso para o voo {voo_selecionado.id}."
            else:
                return f"Cliente {user.name}: Falha na compra da passagem."

    except Exception as e:
        return f"Cliente {client_id}: Erro -> {e}"

def testar_concorrencia(server_host, server_port, num_clientes):
    """
    Função para testar a concorrência de múltiplos clientes realizando login e compra de passagem simultaneamente.

    Args:
        server_host (str): Endereço IP do servidor.
        server_port (int): Porta em que o servidor está ouvindo.
        num_clientes (int): Número de clientes que serão simulados.

    """
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_clientes) as executor:
        # Simula múltiplos clientes realizando login e compra simultaneamente
        futures = [
            executor.submit(simular_cliente, server_host, server_port, client_id + 1)
            for client_id in range(num_clientes)
        ]
        
        # Exibe os resultados conforme os clientes finalizam as operações
        for future in concurrent.futures.as_completed(futures):
            print(future.result())

# Parâmetros do servidor
server_host = "127.0.0.1"  
server_port = 65432        

# Número de clientes simultâneos
num_clientes = 10

# Iniciar teste de concorrência
testar_concorrencia(server_host, server_port, num_clientes)