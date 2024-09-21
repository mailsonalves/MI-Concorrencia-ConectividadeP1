from model.Voo import Voo
from model.User import User
import random

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
nomes = ["Alice", "Bruno", "Carla", "Daniel", "Eduarda", "Fernando", "Gabriela", "Henrique", "Isabela", "João"]
precos = [100, 150, 200, 250, 300]  # Lista de preços ou valores

def gerar_voos(voos):
    for capital_origem, destinos in capitais_brasil.items():
            voo_array_temp = []  
            for capital_destino in destinos:
                New_voo = Voo(capital_origem, capital_destino)  
                voo_array_temp.append(New_voo)  
            voos[capital_origem] = voo_array_temp

def gerar_user(users):
    for number in range(1,10):
            username: str = 'admin'
            password: str = 'password'
            New_user: User = User(password, username)
            users[New_user.id_user] = New_user
            users[New_user.id_user].username = users[New_user.id_user].username + str(number)
            users[New_user.id_user].password = users[New_user.id_user].password + str(number)
            users[New_user.id_user].name = nomes[number]
            number_random = random.randint(0, len(precos) - 1)  
            users[New_user.id_user].preco = precos[number_random]
            