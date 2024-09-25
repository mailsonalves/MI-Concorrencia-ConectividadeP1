from model.Voo import Voo
from model.User import User
import random

# Mapeia capitais brasileiras e seus destinos de voo
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

# Lista de nomes para os usuários
nomes = ["Alice", "Bruno", "Carla", "Daniel", "Eduarda", "Fernando", "Gabriela", "Henrique", "Isabela", "João"]

# Lista de preços de passagens
precos = [100, 150, 200, 250, 300]  # Valores dos preços

def gerar_voos(voos):
    """
    Gera voos entre capitais brasileiras e os armazena em um dicionário.

    Args:
        voos (dict): Dicionário que irá armazenar as listas de voos para cada capital de origem.

    Returns:
        None
    """
    for capital_origem, destinos in capitais_brasil.items():
        voo_array_temp = []  # Lista temporária para armazenar voos da capital de origem
        for capital_destino in destinos:
            # Cria um novo voo entre a capital de origem e o destino
            New_voo = Voo(capital_origem, capital_destino)
            number_random = random.randint(0, len(precos) - 1)  # Seleciona um preço aleatório
            New_voo.preco = precos[number_random]  # Atribui o preço ao voo
            voo_array_temp.append(New_voo)  # Adiciona o voo à lista temporária
        voos[capital_origem] = voo_array_temp  # Armazena a lista de voos no dicionário

def gerar_user(users):
    """
    Gera usuários e os armazena em um dicionário.

    Args:
        users (dict): Dicionário que irá armazenar os usuários gerados.

    Returns:
        None
    """
    for number in range(1, 10):
        username: str = 'admin'  # Nome base de usuário
        password: str = 'password'  # Senha base
        New_user: User = User(password, username)  # Cria um novo usuário
        users[New_user.id_user] = New_user  # Armazena o usuário no dicionário
        # Adiciona um número ao nome de usuário e senha para torná-los únicos
        users[New_user.id_user].username = users[New_user.id_user].username + str(number)
        users[New_user.id_user].password = users[New_user.id_user].password + str(number)
        users[New_user.id_user].name = nomes[number]  # Atribui um nome aleatório ao usuário

       
            