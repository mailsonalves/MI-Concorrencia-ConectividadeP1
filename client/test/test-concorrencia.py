import socket
import pickle
import concurrent.futures
import time
from model.User import User
from model.Voo import Voo
from model.Passagem import Passagem

def simular_cliente(server_host, server_port, client_id):
    log = []  # Lista para armazenar logs do cliente
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Conecta ao servidor
            s.connect((server_host, server_port))
            
            # 1. Simula login (ação de código 100)
            login_data = {"username": f"admin{client_id}", "password_user": f"password{client_id}"}
            login_request = pickle.dumps((100, login_data))
            
            start_time = time.perf_counter()  # Início da medição de latência
            s.sendall(login_request)
            login_latency = (time.perf_counter() - start_time) * 1_000_000_000  # Medida de latência em nanosegundos
            
            # Recebe resposta de login
            login_response = s.recv(4096)
            login_resposta = pickle.loads(login_response)
            
            if not login_resposta or not login_resposta.get("token"):
                log_message = f"Cliente {client_id}: Falha no login. Latência: {login_latency:.2f} ns"
                log.append(log_message)
                return "\n".join(log)

            user = login_resposta["user"]
            log_message = f"Cliente {client_id}: Login bem-sucedido para o usuário {user.name}. Latência de login: {login_latency:.2f} ns"
            log.append(log_message)

            # 2. Solicita a lista de voos disponíveis (ação de código 201)
            voo_request = pickle.dumps((201, ""))
            start_time = time.perf_counter()  # Início da medição de latência
            s.sendall(voo_request)
            voo_latency = (time.perf_counter() - start_time) * 1_000_000_000  # Medida de latência em nanosegundos
            
            # Recebe a lista de voos
            voo_response = s.recv(4096)
            voos = pickle.loads(voo_response)
            
            if not voos:
                log_message = f"Cliente {client_id}: Nenhum voo disponível. Latência para solicitar voos: {voo_latency:.2f} ns"
                log.append(log_message)
                return "\n".join(log)

            # 3. Seleciona um voo e tenta comprar uma passagem
            origem = next(iter(voos))  # Seleciona o primeiro trecho disponível
            voo_selecionado = voos[origem][1]  # Seleciona o primeiro voo da origem
            compra_passagem_data = Passagem(voo_selecionado.id, user.id_user, f"000.000.000-{client_id}")
            compra_passagem_data.assento = 'A1'
        
            compra_request = pickle.dumps((202, compra_passagem_data))
            start_time = time.perf_counter()  # Início da medição de latência
            s.sendall(compra_request)
            compra_latency = (time.perf_counter() - start_time) * 1_000_000_000  # Medida de latência em nanosegundos
            
            # Recebe resposta da tentativa de compra
            compra_response = s.recv(4096)
            compra_resposta = pickle.loads(compra_response)

            if compra_resposta:
                log_message = f"Cliente {user.name}: Compra realizada com sucesso para o voo {voo_selecionado.id}. Latência de compra: {compra_latency:.2f} ns"
                log.append(log_message)
            else:
                log_message = f"Cliente {user.name}: Falha na compra da passagem. Latência de compra: {compra_latency:.2f} ns"
                log.append(log_message)

    except Exception as e:
        log_message = f"Cliente {client_id}: Erro -> {e}"
        log.append(log_message)

    # Escreve os logs em um arquivo
    with open("client_logs.txt", "a") as log_file:
        log_file.write("\n".join(log) + "\n")

    return "\n".join(log)

def testar_concorrencia(server_host, server_port, num_clientes):
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_clientes) as executor:
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
