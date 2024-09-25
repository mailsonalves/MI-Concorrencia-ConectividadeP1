import socket
import pickle
import concurrent.futures
import threading
import time
from model.User import User
from model.Voo import Voo
from model.Passagem import Passagem

def simular_cliente(server_host, server_port, client_id):
    """
    Simula um cliente que se conecta ao servidor, faz login, solicita a lista de voos e tenta comprar uma passagem, solicitando o mesmo assento.

    Args:
        server_host (str): Endereço IP do servidor.
        server_port (int): Porta do servidor.
        client_id (int): Identificador único do cliente para fins de simulação.

    Returns:
        str: Log contendo as mensagens de status e latências das operações do cliente.
    """
    log = []  # Lista para armazenar logs do cliente
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Conecta ao servidor
            s.connect((server_host, server_port))
            
            # 1. Simula login (ação de código 100)
            login_data = {"username": f"admin{client_id}", "password_user": f"password{client_id}"}
            login_request = pickle.dumps((100, login_data))
            
            # Medir a latência do login
            start_time = time.perf_counter()  
            s.sendall(login_request)
            login_latency = (time.perf_counter() - start_time) * 1_000_000_000  # Latência em nanosegundos
            
            # Recebe resposta de login
            login_response = s.recv(4096)
            login_resposta = pickle.loads(login_response)
            
            user = login_resposta["user"]  # Informações do usuário logado
            
            if not login_resposta or not login_resposta.get("token"):
                # Loga a falha de login e encerra
                log_message = f"Cliente {user.name}: Falha no login. Latência: {login_latency:.2f} ns"
                log.append(log_message)
                return "\n".join(log)

            log_message = f"Cliente {user.name}: Login bem-sucedido para o usuário {user.name}. Latência de login: {login_latency:.2f} ns"
            log.append(log_message)

            # 2. Solicita a lista de voos disponíveis (ação de código 201)
            voo_request = pickle.dumps((201, ""))
            start_time = time.perf_counter()  # Medir a latência da solicitação de voos
            s.sendall(voo_request)
            voo_latency = (time.perf_counter() - start_time) * 1_000_000_000  # Latência em nanosegundos
            
            # Recebe a lista de voos
            voo_response = s.recv(4096)
            voos = pickle.loads(voo_response)
            
            if not voos:
                # Loga se não houver voos disponíveis
                log_message = f"Cliente {client_id}: Nenhum voo disponível. Latência para solicitar voos: {voo_latency:.2f} ns"
                log.append(log_message)
                return "\n".join(log)

            # 3. Seleciona um voo e tenta comprar uma passagem
            origem = next(iter(voos))  # Seleciona o primeiro trecho disponível
            voo_selecionado = voos[origem][1]  # Seleciona o primeiro voo da origem
            compra_passagem_data = Passagem(voo_selecionado.id, user.id_user, f"000.000.000-{client_id}")
            compra_passagem_data.assento = 'A1'  # Escolhe o assento A1
            
            compra_request = pickle.dumps((202, compra_passagem_data))
            start_time = time.perf_counter()  # Medir a latência da compra
            s.sendall(compra_request)
            compra_latency = (time.perf_counter() - start_time) * 1_000_000_000  # Latência em nanosegundos
            
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
        # Loga qualquer erro que ocorra
        log_message = f"Cliente {client_id}: Erro -> {e}"
        log.append(log_message)

    # Escreve os logs em um arquivo
    with open("client_logs.txt", "a") as log_file:
        log_file.write("\n".join(log) + "\n")
        log_file.write("\n")
        
    return "\n".join(log)

def testar_concorrencia(server_host, server_port, num_clientes):
    """
    Testa a concorrência de múltiplos clientes simulando requisições simultâneas a um servidor.

    Args:
        server_host (str): Endereço IP do servidor.
        server_port (int): Porta do servidor.
        num_clientes (int): Número de clientes simultâneos a serem simulados.

    Returns:
        None
    """
    resultados = []  # Armazenar resultados de todos os clientes
    threads = []  # Lista para armazenar as threads dos clientes
    inicio = time.time()  # Marca o início do teste

    # Cria uma barreira para sincronizar o início de todas as threads
    barreira = threading.Barrier(num_clientes)

    def thread_func(client_id):
        """Função executada por cada thread, responsável por simular um cliente."""
        try:
            barreira.wait()  # Espera até que todas as threads estejam prontas para começar
            resultado = simular_cliente(server_host, server_port, client_id)
            resultados.append(resultado)
            print(resultado)
        except Exception as e:
            print(f"Erro no cliente {client_id}: {e}")

    # Cria e inicia as threads
    for client_id in range(1, num_clientes + 1):
        t = threading.Thread(target=thread_func, args=(client_id,))
        t.start()
        threads.append(t)

    # Aguarda todas as threads finalizarem
    for t in threads:
        t.join()

    fim = time.time()  # Marca o fim do teste
    print(f"\nTeste de concorrência finalizado com {num_clientes} clientes.")
    print(f"Teste finalizado em {fim - inicio:.2f} segundos")


# Parâmetros do servidor
server_host = "127.0.0.1"  
server_port = 65432        

# Número de clientes simultâneos
num_clientes = 9

# Iniciar teste de concorrência
testar_concorrencia(server_host, server_port, num_clientes)
